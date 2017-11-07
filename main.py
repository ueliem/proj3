import csv
import numpy as np

class Transcript:
    def __init__(self):
        self.name = None
        self.length = None
        self.effectiveLength = None
        self.tpm = None
        self.numReads = None

transcripts = {}

def main():
    # http://salmon.readthedocs.io/en/latest/file_formats.html#quantification-file
    with open("quant.sf") as qsf:
        # http://salmon.readthedocs.io/en/latest/file_formats.html#unique-and-ambiguous-count-file
        with open("ambig_info.tsv") as amb:
            qsfReader = csv.reader(qsf, dialect="excel-tab")
            ambReader = csv.reader(amb, dialect="excel-tab")
            next(reader, None) # skip header line
            # load basic transcript info line by line
            for line1, line2 in zip (qsfReader, ambReader):
                t = Transcript()
                t.name = line1[0]
                t.length = line1[1]
                t.effectiveLength = line1[2]
                t.tpm = line1[3]
                t.numReads = line1[4]
                t.uniquelyMappedCount = line2[0]
                t.ambiguouslyMappedCount = line2[1]
                transcripts[t.name] = t

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

    tsLengths = [v.length for k, v in transcripts.items()]
    avgLength = np.mean(tsLengths)
    sigmaLength = np.std(tsLengths)
            
    upperBnd = avgLength + 2 * sigmaLength
    lowerBnd = avgLength - 2 * sigmaLength
    tvLength = map (lambda x: x > upperBnd or x < lowerBnd, tsLengths)


if __name__ == "__main__": main()

