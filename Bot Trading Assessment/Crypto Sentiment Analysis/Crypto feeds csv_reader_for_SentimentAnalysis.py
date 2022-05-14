import csv
with open('Crypto feeds.csv') as csv_file:
    csv_reader=csv.reader(csv_file)

    next(csv_reader,None) # Remove any headers

    feeds=[] # Create an emppty list

    for row in csv_reader:
            print(feeds.append(row[0]))
        
#headlines={'source':[],'title':[],'pubDate':[]}

