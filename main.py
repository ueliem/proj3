import csv
import numpy as np
import bootstrap

class Transcript:
    def __init__(self):
        self.name = None
        self.length = None
        self.effectiveLength = None
        self.tpm = None
        self.numReads = None
        self.uniquelyMappedCount = None
        self.ambiguouslyMappedCount = None
        self.lowerBnd = None
        self.upperBnd = None

def findOutliers(l):
    avg = np.mean(l)
    sigma = np.std(l)
    upperBnd = avg + 2 * sigma
    lowerBnd = avg - 2 * sigma
    return map (lambda x: True if x > upperBnd or x < lowerBnd else False, l)

def isOutlier(t):
    if t.tpm < t.lowerBnd or t.tpm > t.upperBnd:
        return True
    else:
        return False

transcripts = {}

def main():
    # http://salmon.readthedocs.io/en/latest/file_formats.html#quantification-file
    with open("quant.sf") as qsf:
        # http://salmon.readthedocs.io/en/latest/file_formats.html#unique-and-ambiguous-count-file
        # with open("ambig_info.tsv") as amb:
            qsfReader = csv.reader(qsf, dialect="excel-tab")
            # ambReader = csv.reader(amb, dialect="excel-tab")
            next(qsfReader, None) # skip header line
            # load basic transcript info line by line
            for line1, (lowerBnd, upperBnd) in zip (qsfReader, bootstrap.bs()):
            # for line1, line2, lowerBnd, upperBnd in zip (qsfReader, ambReader, bootstrap.bs()):
                t = Transcript()
                t.name = line1[0]
                t.length = int(line1[1])
                t.effectiveLength = float(line1[2])
                t.tpm = float(line1[3])
                t.numReads = float(line1[4])
                # t.uniquelyMappedCount = line2[0]
                # t.ambiguouslyMappedCount = line2[1]
                t.lowerBnd = lowerBnd
                t.upperBnd = upperBnd
                transcripts[t.name] = t
                print "t"

    # http://salmon.readthedocs.io/en/latest/file_formats.html#equivalence-class-file
    #with open("eq_classes.txt") as eqc:
        # reader = csv.reader(eqc, dialect="excel-tab")
        # N = int(next(reader)[0])
        # M = int(next(reader)[0])
        # names = reader[:N] # take N transcript names
        # eq_classes = reader[:M] # take M equivalence classes
# 
            # transcriptCount = eq_classes[0]
            # scripts = eq_classes[1:-2]
            # fragmentCount = eq_classes[-1]

    # tsTPM = [v.tpm for k, v in transcripts.items()]
    # tvTPM = findOutliers(tsLengths)

    outliers = []
    nonOutliers = []

    print "Filtering outliers..."

    for k, ts in transcripts.items():
        if isOutlier(ts):
            outliers.append(ts)
        else:
            nonOutliers.append(ts)

    # tsTPM = [v.tpm for k, v in transcripts.items()]
    print len(outliers), len(nonOutliers)

if __name__ == "__main__": main()

