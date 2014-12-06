__author__ = 'Jai Chaudhary'

import logging
logging.basicConfig(filename='logs/normalizedoneNN.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
import argparse
import code.utils as utils
from config import TRIP_DATA_1,TRAIN_DATA,F_FIELDS,S_FIELDS
from datetime import datetime
from sklearn.grid_search import GridSearchCV


def derive_normalizer(records):
    normalize_u = np.mean(records, axis=0) 
    normalize_s = np.std(records, axis=0)
    def normalizer(records):
        try:
            return np.divide(np.subtract(records, normalize_u * np.ones(records.shape, dtype=np.float)), normalize_s * np.ones(records.shape, dtype=np.float)) 
        except:
            logging.exception("Scaling error")
            raise ValueError
    return normalizer

def datestring_to_seconds_from_midnight(dateStr):
    datetimeObj = datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
    return datetimeObj.hour * 3600 + datetimeObj.minute * 60 + datetimeObj.second

def oneNN(trainOn, testOn):
    trainX = np.array([[datestring_to_seconds_from_midnight(row[0])] + row[-5:] for row in utils.load_csv_lazy(TRAIN_DATA, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
    normalizer = derive_normalizer(trainX)
    trainX = normalizer(trainX)
    
    trainY = np.array([row[2] for row in utils.load_csv_lazy(TRAIN_DATA, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
    kspace = {'n_neighbors' : np.linspace(2, 3)}
    grid_nbrs = GridSearchCV(KNeighborsRegressor(algorithm='brute'),kspace, scoring='mean_squared_error' )
    grid_nbrs.fit(trainX[:trainOn], trainY[:trainOn])
    print "Train Complete"
    print "K = ", grid_nbrs.best_params_
    testX = np.array([[datestring_to_seconds_from_midnight(row[0])] + row[-5:] for row in utils.load_csv_lazy(TRIP_DATA_1, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
    testX = normalizer(testX)
    
    testY = np.array([row[2] for row in utils.load_csv_lazy(TRIP_DATA_1, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
    
    print utils.metrics(grid_nbrs, testX[:testOn], testY[:testOn])

def main():
    parser = argparse.ArgumentParser( description = '1-Nearest Neighbour to predict trip_time' )
    parser.add_argument( 'trainOn' , nargs = '?', type = int, default = 500000, help = 'Number of data points to train on' )
    parser.add_argument( 'testOn' , nargs = '?', type = int, default = 100000, help = 'Number of data points to test on' )
    args = parser.parse_args()
    oneNN( args.trainOn, args.testOn )

if __name__ == '__main__':
    main()
