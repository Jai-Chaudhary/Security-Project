import numpy,math,datetime,logging
from sklearn import linear_model
from distance import get_distance
# logging.basicConfig(filename='logs/utils.log',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def metrics(model,x,y):
    """
    compute ols and rmse
    :param y:
    :param yhat:
    :return ols and rmse:
    """
    yhat = model.predict(x)
    ols = sum(numpy.square((y-yhat)))
    rmse = (ols/len(y))**0.5
    corr = numpy.corrcoef(y,yhat)
    absME = sum(numpy.absolute(y-yhat))/len(y)
    return absME ,rmse,corr

def evaluate(model_list,x,y):
    for description,model in model_list:
        print "\t",description,"OLS, RMSE and Correlation coefficient",metrics(model,x,y),"Model",model.coef_,model.intercept_


def split(target, features, row, x, y, x_test=None, y_test=None, i= None, nth = None):
    """
    :param target: index of expected
    :param features: list of indexes
    :param row:
    :param x:
    :param y:
    :param x_test:
    :param y_test:
    :param i:
    :param nth:
    """

    if nth and i % nth == 0:
        x_test.append([row[feature] for feature in features])
        y_test.append(row[target])
    else:
        x.append([row[feature] for feature in features])
        y.append(row[target])


def tls(model,x,y):
    pass


def linear_regression(x,y):
    """
    :param x:
    :param y:
    :return linear regression model object:
    """
    model = linear_model.LinearRegression()
    model.fit(x, y)
    return model


def itransformer(row):
    """
    identity transformer returns same
    :param row:
    :return True:
    """
    return row

def ifilter(row):
    """
    identity filter always returns True
    :param row:
    :return True:
    """
    return True


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

def load_csv_lazy(fname,str_fields,float_fields,exclude_first=True,row_filter=ifilter,row_tranformer=itransformer):
    """
    np.genfromtxt is a good alternative, not sure if it can act as a generator. pandas frames are also a good alternative.
    :param fname:
    :param exclude_first:
    :return:
    """
    error_count = 0
    excluded_count = 0
    for count,line in enumerate(file(fname)):
        if not exclude_first:
            try:
                if count and count % 10**6 == 0:
                    logging.debug("Loaded "+str(count))
                    logging.debug("error_count : "+str(error_count))
                    logging.debug("excluded_count : "+str(excluded_count))
                entries = line.strip().split(',')
                row = [entries[f] for f in str_fields] + [float(entries[f]) for f in float_fields]
                if row_filter(row):
                    row = row_tranformer(row)
                    yield row
                else:
                    excluded_count += 1
            except:
                error_count += 1
        else:
            exclude_first = False
    logging.debug("count : "+str(count))
    logging.debug("error_count : "+str(error_count))
    logging.debug("excluded_count : "+str(excluded_count))