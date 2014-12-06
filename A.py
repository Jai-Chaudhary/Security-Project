__author__ = 'Jai Chaudhary'

import logging
logging.basicConfig(filename='logs/densityestimation.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
import numpy as np
import argparse
import code.utils as utils
from config import TRIP_DATA_1,TRAIN_DATA,F_FIELDS,S_FIELDS
import matplotlib.pyplot as plt

# from sklearn.neighbors.kde import KernelDensity
# from sklearn.grid_search import GridSearchCV


DEFAULT_DATASET = 'train_data.csv'
DATASETS = [ DEFAULT_DATASET]

DEFAULT_MODEL = 'gaussian-kernel'
MODELS = [ DEFAULT_MODEL]


def EstimateDensity(dataset, model):
	example_data = np.array([[row[1]] + row[-2:] for row in utils.load_csv_lazy(TRAIN_DATA, S_FIELDS,F_FIELDS,row_filter=utils.distance_filter)], dtype = float)
	#example_data = example_data[:,:]
	# plt.scatter(example_data[:,-2:-1], example_data[:,-1])
	#params = {'bandwidth': np.logspace(-10, 1, 1)}
	#grid = GridSearchCV(KernelDensity(kernel='gaussian', metric="haversine"), params)
	#grid.fit(example_data[:,-2:])
	#kde = grid.best_estimator_
	# kde = KernelDensity(kernel='gaussian', metric="haversine", bandwidth=0.0002)
	# kde.fit(example_data[:,-2:])
	# kernel = stats.gaussian_kde(example_data[:,-2:])
	
	xmin = float(min(example_data[:,-2:-1])[0])
	xmax = float(max(example_data[:,-2:-1])[0])
	ymin = float(min(example_data[:,-1:])[0])
	ymax = float(max(example_data[:,-1:])[0])
	
	# print xmin,xmax,ymin,ymax
	# X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
	# print x, y
	res = 1000
	freq1Pass = np.zeros((res, res), dtype=np.int)
	freq3Pass = np.zeros((res, res), dtype=np.int)
	freqTotalPass = np.ones((res, res), dtype=np.int) * 0.00000001

	for data in example_data:
		xindex = (res - 1) - ((xmax - data[1] ) * (res - 1) / (xmax - xmin))
		yindex =  (ymax - data[2] ) * (res - 1) / (ymax - ymin) 
		if (data[0] == 1):
			freq1Pass[yindex][xindex] += 1
			freqTotalPass[yindex][xindex] += 1
		elif (data[0] == 3):
			freq3Pass[yindex][xindex] += 1
			freqTotalPass[yindex][xindex] += 1
		else:
			freqTotalPass[yindex][xindex] += 1

	prob1Pass = np.divide(freq1Pass, freqTotalPass)
	prob3Pass = np.divide(freq3Pass, freqTotalPass)
	# print X, Y
	#positions = np.vstack([X.ravel(), Y.ravel()]).T
	#print positions
	#Z = np.reshape(kde.score_samples(positions), X.shape)
	#levels = np.logspace(Z.min(), Z.max(), 10)

	#CS = plt.contourf(X, Y, Z, cmap=plt.cm.bone)
	#CS2 = plt.contour(CS, levels=levels,
    #                    colors = 'r',
    #                    hold='on', norm=matplotlib.colors.LogNorm())
	#plt.scatter(example_data[:,-2:-1], example_data[:,-1])
	plt.imshow(freqTotalPass, hold='on').set_cmap('cool')
	
	#plt.imshow(prob1Pass, hold='on').set_cmap('binary')
	#plt.imshow(prob3Pass, hold='on').set_cmap('binary')
	plt.show()







def main():
	parser = argparse.ArgumentParser( description = 'Density Estimation and Plot' )
	parser.add_argument( 'dataset'     , nargs = '?', type = str, default = False, help = 'Dataset File' )
	parser.add_argument( 'model'       , nargs = '?', type = str, default = DEFAULT_MODEL  , choices = MODELS  , help = 'Model type' )
	args = parser.parse_args()
	EstimateDensity( args.dataset, args.model )

if __name__ == '__main__':
	main()
