import csv, time
import numpy as np

def bs():
    with open("quant_bootstraps.tsv") as qb:
        print "Bootstrapping..."
        qbReader = csv.reader(qb, dialect="excel-tab")
        headers = next(qbReader)
        count = 0
        data = [np.asarray(map(float, line)) for line in qbReader]
            # data = np.concatenate(data, np.asarray(map(float, line)))
            # count = count + 1

        data = np.asarray(data)
        # print type(data)
        # print data

        print len(headers)
        for i in range (0, len(headers)):
            # print i
            col = np.copy(data[:, i])
            col_mean = np.mean(col)
            ls = [np.mean(np.random.choice(col, 200, replace=True)) for j in range (0, 100)]
            star_means = np.asarray(sorted(ls))
            lowerBnd = np.percentile(star_means, 2.5)
            upperBnd = np.percentile(star_means, 97.5)
            yield lowerBnd, upperBnd
            # time.sleep(1)

def main():
    for lowerBnd, upperBnd in bs():
        print lowerBnd, upperBnd

if __name__ == "__main__": main()

