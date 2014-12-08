from matplotlib import pyplot as plt
import pylab

vodafone = [40.712784, -74.005941]
verizon = [40.710813, -74.001181]
omc = [40.752347, -73.984061]
virgin = [43.052563, -74.346557]
aa = [40.746334, -73.982464]
silverlake = [40.763861, -73.974794]
publis = [40.750086, -73.987218]
TFS = [40.681878, -74.311915]

targets = [vodafone, verizon, omc, virgin, aa, silverlake, publis, TFS]
names = ['vodafone', 'verizon', 'omc', 'virgin', 'aa', 'silverlake', 'publis', 'TFS']
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def plot_freq(data, title, bank, month):
	plt.clf()
	ax = plt.subplot(111)
	
	for name, target in zip(names, data):
		startday, endday = sum(days[:month]), sum(days[:month+1])
		ys = target[startday:endday]
		xs = range(len(ys))
		ax.plot(xs, ys, label=name)

	plt.xlabel("Day")
	plt.ylabel("Trips")
	plt.title(title)

	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

	pylab.savefig("../figures/{}/{}.png".format(bank, title))

def date_as_daynum(date):
	month, day = int(date[5:7]), int(date[8:10])

	# magic (- 1 b/c 0 start index)
	try: return sum(days[:month-1]) + day - 1
	except: return None 

def in_range(lat, lon, delta):
	for i, target in enumerate(targets):
		if abs(target[0]-lat) <= delta and abs(target[1]-lon) <= delta:
			return i
	return -1

def process_csv(csv_num):
	data = open("../data/filtered/filtered{}.csv".format(csv_num))
	bins = [[0] * 365 for _ in range(len(targets))]
	delta = 0.001
	
	for row in data.read().split('\n'):
		vals = row.split(',')
		
		try:
			lon, lat = map(float, vals[-2:])	# end lat / lon
			target = in_range(lat, lon, delta)
			
			if target >= 0:
				day = date_as_daynum(vals[5])
				if day: bins[target][day] += 1
		except:
			continue

	data.close()

	banks = ["JPM", "BARC1", "BARC2", "CITI", "GS", "MS", "CS", "DB", 
             "UBS1", "UBS2", "BOA", "LAZ", "BNP", "SOCG", "WAC", "MAQ"]
	bank = banks[csv_num-1]
	for month in range(12):
		plot_freq(bins, "FrequenciesFor{}_{}".format(bank, month+1), bank, month)

if __name__ == "__main__":
	for csv_num in range(1, 17):
		process_csv(csv_num)