__author__ = 'Jai Chaudhary'
"""
Generates train_data.csv from trip_data_2.csv by selecting every 30th trip
"""
from config import TRIP_DATA_2,TRAIN_DATA

if __name__ == '__main__':
    fout = open(TRAIN_DATA,'w')
    count = 0
    for i,line in enumerate(file(TRIP_DATA_2)):
        if i%30 == 0:
            fout.write(line)
            count += 1
    fout.close()
    print i,count