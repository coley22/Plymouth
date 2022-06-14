import csv

with open('HBEF_lapse_rates.csv') as infile:
    reader = csv.reader(infile)
    for row in reader:
        # header=next(reader)
        print(row[1])
