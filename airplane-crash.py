import csv

with open('/Users/nsclass/Documents/airplane-crash.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
