__author__ = 'Jai Chaudhary'

__author__ = 'Jai Chaudhary'


import logging
logging.basicConfig(filename='logs/oneNNBasic.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
import argparse
import code.utils as utils
from config import TRIP_DATA_1,TRAIN_DATA,F_FIELDS,S_FIELDS

def oneNN(trainOn, testOn):
	trainX = np.array([row[-4:] for row in utils.load_csv_lazy(TRAIN_DATA, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
	trainY = np.array([row[2] for row in utils.load_csv_lazy(TRAIN_DATA, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
	nbrs = KNeighborsRegressor(n_neighbors=1, algorithm='brute').fit(trainX[:trainOn], trainY[:trainOn])
	print "Train Complete"
	testX = np.array([row[-4:] for row in utils.load_csv_lazy(TRIP_DATA_1, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
	testY = np.array([row[2] for row in utils.load_csv_lazy(TRIP_DATA_1, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
	print utils.metrics(nbrs, testX[:testOn], testY[:testOn])

def main():
	parser = argparse.ArgumentParser( description = '1-Nearest Neighbour to predict trip_time' )
	parser.add_argument( 'trainOn' , nargs = '?', type = int, default = 500000, help = 'Number of data points to train on' )
	parser.add_argument( 'testOn' , nargs = '?', type = int, default = 100000, help = 'Number of data points to test on' )
	args = parser.parse_args()
	print args.trainOn, args.testOn
	oneNN( args.trainOn, args.testOn )

if __name__ == '__main__':
	main()
