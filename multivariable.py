"""
Multi variable linear regression, in-memory and chunked
"""
import logging
logging.basicConfig(filename='logs/multi.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
import datetime
import code.utils as utils
from code.distance import get_distance
import numpy
from config import S_FIELDS,F_FIELDS,EXAMPLE_DATA,TRIP_DATA_1,TRIP_DATA_2

def derive_filter(rows,tolerance = 4.0):
    """
    Generates a custom filter function  on trip_distance alone
    :param trip_dist_mean:
    :param trip_dist_std:
    :param tolerance:
    :return:

    !IMPORTANT Filters are always applied before transformers!
    """
    distances = numpy.array([row[2] for row in rows]) # InMemory
    trip_dist_mean = numpy.mean(distances)
    trip_dist_std = numpy.std(distances)
    logging.debug("Dervied mean "+str(trip_dist_mean))
    logging.debug("Dervied std "+str(trip_dist_std))
    def custom_filter(row):
        if row[1] != 0.0 and row[2] != 0.0 and row[3] != 0.0 and row[4] != 0.0 and row[5] != 0.0 and row[6] != 0.0: # filters out rows with zero elements
            plong,plat,dlong,dlat=row[-4:]
            if 100 > get_distance(plat,plong,dlat,dlong) > 0 and ((row[2] - trip_dist_mean) / trip_dist_std) < tolerance:
                return True
        return False
    return custom_filter

def derive_scale_transform(rows,indexes):
    """
    Generates tran
    :param rows:
    :param indexes:
    :return:
    """
    min_values,max_values = {},{}
    first = True
    for row in rows:
        row[0] = int(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S" ).strftime("%s"))
        for index in indexes:
            if not first:
                max_values[index] = max(max_values[index],row[index])
                min_values[index] = min(min_values[index],row[index])
            else:
                max_values[index] = row[index]
                min_values[index] = row[index]
        first = False
    logging.debug("scale values min "+str(min_values))
    logging.debug("scale values max "+str(max_values))
    def custom_transform(row):
        try:
            row[0] = int(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S" ).strftime("%s"))
            for index in indexes:
                row[index] = (row[index] - min_values[index]) / (max_values[index]-min_values[index])
            return row
        except:
            logging.exception("Scaling error")
            raise ValueError
    return custom_transform




if __name__ == '__main__':
    models = []
    features = (0,2,3,4)
    target = 1

    # Derive a filter from example data
    mean_dev_filter = derive_filter(utils.load_csv_lazy(EXAMPLE_DATA,S_FIELDS,F_FIELDS))

    # Generate a scale transformer using only indexes which are used as features, use filter derived previously
    scale_transform = derive_scale_transform(utils.load_csv_lazy(EXAMPLE_DATA,S_FIELDS,F_FIELDS,row_filter=mean_dev_filter),features)

    # now example_data is a loadCSV is a generator
    example_data = [row for row in utils.load_csv_lazy(EXAMPLE_DATA,S_FIELDS,F_FIELDS, row_filter = mean_dev_filter, row_tranformer=scale_transform)]
    logging.debug("inspection for transformation "+str(example_data[-3:]))

    # now trip_data_1 and trip_data_2 is a loadCSV is a generator
    trip_data_1 = utils.load_csv_lazy(TRIP_DATA_1,S_FIELDS,F_FIELDS, row_filter = mean_dev_filter, row_tranformer = scale_transform)
    trip_data_2 = utils.load_csv_lazy(TRIP_DATA_2,S_FIELDS,F_FIELDS, row_filter = mean_dev_filter, row_tranformer = scale_transform)

    x, y, x_test, y_test = [],[],[],[]
    for i,row in enumerate(example_data):
        utils.split(target,features,row,x,y,x_test,y_test,i,4)
    x, y, x_test, y_test = map(numpy.array,[x, y, x_test, y_test])

    model = utils.linear_regression(x,y)
    models.append(("Model trained on example training data",model))

    print "\nEvaluation on training data"
    utils.evaluate(models,x,y)

    print "\nEvaluation on test data"
    utils.evaluate(models,x_test,y_test)

    # following line is not required but recommended to stop un-intended reuse
    x, y, x_test, y_test = [],[],[],[]

    x_buf,y_buf = [],[]
    for i,row in enumerate(trip_data_1):
        utils.split(target,features,row,x_buf,y_buf)
        if i and i % 10**7 == 0: # process in chunks of 10 Million at time (For less than 8GB RAM use 1 Million)
            x_buf,y_buf = map(numpy.array,[x_buf,y_buf])
            logging.info("buffer sizes "+str((len(x_buf))))
            model = utils.linear_regression(x_buf,y_buf)
            print "\nEvaluation on "+str(len(x_buf))+" trips from trip_data_1.csv"
            models.append(("Model trained on "+str(len(x_buf))+" trips from trip_data_1.csv",model))
            utils.evaluate(models,x_buf,y_buf)
            # clear the buffer
            x_buf,y_buf = [],[]

    x_buf,y_buf = map(numpy.array,[x_buf,y_buf])
    model = utils.linear_regression(x_buf,y_buf)
    print "\nEvaluation on "+str(len(x_buf))+" trips from trip_data_1.csv"
    models.append(("Model trained on "+str(len(x_buf))+" trips from trip_data_1.csv",model))
    utils.evaluate(models,x_buf,y_buf)
    # clear the buffer
    x_buf,y_buf = [],[]


    x_buf,y_buf = [],[]
    for i,row in enumerate(trip_data_2):
        utils.split(target,features,row,x_buf,y_buf)
        if i and i % 10**7 == 0: # process in chunks of 10 Million at time (For less than 8GB RAM use 1 Million)
            x_buf,y_buf = map(numpy.array,[x_buf,y_buf])
            print "\nEvaluation on "+str(len(x_buf))+" trips from trip_data_2.csv"
            utils.evaluate(models,x_buf,y_buf)
            # clear the buffer
            x_buf,y_buf = [],[]

    x_buf,y_buf = map(numpy.array,[x_buf,y_buf])
    print "\nEvaluation on "+str(len(x_buf))+" trips from trip_data_2.csv"
    utils.evaluate(models,x_buf,y_buf)
    # clear the buffer
    x_buf,y_buf = [],[]
