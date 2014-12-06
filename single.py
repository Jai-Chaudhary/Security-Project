"""
Single variable linear regression, in-memory and chunked
"""
import logging
logging.basicConfig(filename='logs/single.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
from config import TRIP_DATA_1,TRIP_DATA_2,EXAMPLE_DATA,F_FIELDS,S_FIELDS
import code.utils as utils
from code.distance import get_distance
import numpy




def distance_filter(row):
    """
    :param row:
    :return row:
    """
    if row[1] != 0.0 and row[2] != 0.0 and row[3] != 0.0 and row[4] != 0.0 and row[5] != 0.0 and row[6] != 0.0: # filters out rows with zero elements
        plong,plat,dlong,dlat=row[-4:]
        if 100 > get_distance(plat,plong,dlat,dlong) > 0: # one of the many cool features of python
            return True
    return False






if __name__ == '__main__':
    models = []

    features = [2]
    target = 1
    # rows is stored in memory
    example_data = [row for row in utils.load_csv_lazy(EXAMPLE_DATA,S_FIELDS,F_FIELDS,row_filter=distance_filter)]

    #  rows is a loadCSV is a generator
    trip_data_1 = utils.load_csv_lazy(TRIP_DATA_1,S_FIELDS,F_FIELDS,row_filter=distance_filter)

    #  rows is a loadCSV is a generator
    trip_data_2 = utils.load_csv_lazy(TRIP_DATA_2,S_FIELDS,F_FIELDS,row_filter=distance_filter)


    x, y, x_test, y_test = [],[],[],[]
    for i,row in enumerate(example_data):
        utils.split(target,features,row,x,y,x_test,y_test,i,4)
    x, y, x_test, y_test = map(numpy.array,[x, y, x_test, y_test])
    model = utils.linear_regression(x,y)
    models.append(("Model trained on training example data",model))

    print "\nEvaluation on training data"
    utils.evaluate(models,x,y)

    print "\nEvaluation on test data"
    utils.evaluate(models,x_test,y_test)

    # following line is not required but recommended to stop un-intended reuse
    x, y, x_test, y_test = [],[],[],[]

    # Test previous model and train using trip_data_1
    x_buf,y_buf = [],[]
    for i,row in enumerate(trip_data_1):
        utils.split(target,features,row,x_buf,y_buf)
        if i and i % 10**8 == 0: # process in chunks of 1 Million at time on machines will less than 6GB RAM, (possible to process entire data on a MacBook Pro with 8GB RAM set change to 10**8)
            x_buf,y_buf = map(numpy.array,[x_buf,y_buf])
            model = utils.linear_regression(x_buf,y_buf)
            models.append(("Model trained on "+str(len(x_buf))+"trips from trip_data_1.csv",model))
            print "\nEvalutation on",i,"th chunk"
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
        if i and i % 10**8 == 0: # process in chunks of 1 Million at time (For less than 8GB RAM)
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
