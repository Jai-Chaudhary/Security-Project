from matplotlib import pyplot as plt
import pylab

def plot_freq(data, title):
	xs, ys = range(len(data)), data
	
	plt.clf()
	plt.xlabel("Day")
	plt.ylabel("Trips")
	plt.plot(xs, ys)
	plt.title(title)
	#plt.show()

	pylab.savefig("../figures/{}.png".format(title))

def date_as_daynum(date):
	days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	month, day = int(date[5:7]), int(date[8:10])

	# magic (- 1 b/c 0 start index)
	try: return sum(days[:month-1]) + day - 1
	except: return None 

def process_csv(csv_num):
	data = open("../data/filtered/filtered{}.csv".format(csv_num))
	bins = [0] * 365
	
	for row in data.read().split('\n'):
		vals = row.split(',')
		
		try:
			day = date_as_daynum(vals[5])
			if day: bins[day] += 1
		except:
			continue

	banks = ["JPM", "BARC1", "BARC2", "CITI", "GS", "MS", "CS", "DB", 
             "UBS1", "UBS2", "BOA", "LAZ", "BNP", "SOCG", "WAC", "MAQ"]
	data.close()
	plot_freq(bins, "FrequenciesFor{}".format(banks[csv_num-1]))

if __name__ == "__main__":
	for csv_num in range(1, 17):
		process_csv(csv_num)
