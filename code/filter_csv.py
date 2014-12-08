import csv

JPM = [40.755800, -73.975400]
BARC1 = [40.760636, -73.983037]
BARC2 = [40.753521, -73.976569]
CITI = [40.721186, -74.010499]
GS - [40.7148257, -74.0149859] 
MS = [40.760057, -73.985418]
CS = [40.741509, -73.986628]
DB =  [40.706389, -74.007778]
UBS1 = [41.048747, -73.542035]
UBS2 = [40.760989, -73.980183]
BOA = [40.755278, -73.984167]
LAZ = [40.758943, -73.979356]
BNP = [40.761899, -73.982246]
SOCG = [40.754885, -73.974871]
WAC = [40.758723,  -73.978118] 
MAQ = [40.763598, -73.978951]

banks = [JPM, BARC1, BARC2, CITI, GS, MS, CS, DB, UBS1, UBS2, BOA, LAZ, BNP,
         SOCG, WAC, MAQ]

def in_range(lat, lon, banklat, banklon, delta):
	return abs(lat - banklat) <= delta and abs(lon - banklon) <= delta

if __name__ == "__main__":
# TODO - parse all taxi csv files (gonna take a shit-ton of time)
	f = open("Add Path Here!")
	cs = [open("filtered{}.csv".format(i+1), "wb") for i in range(len(banks))]
	wrs = [csv.writer(c) for c in cs]
	
	delta = 0.001
	slat, slon = 0.0, 0.0

	line = f.readline()
	while line:
		vals = line.strip().split(',')

		try: 
			slon, slat = map(float, vals[-4:-2])	# start lat / lon
		except: line = f.readline()

		for i, bank in enumerate(banks):
			if in_range(slat, slon, bank[0], bank[1], delta):
				wrs[i].writerow(vals)
				break

		line = f.readline()

	for c in cs: c.close()
	f.close()