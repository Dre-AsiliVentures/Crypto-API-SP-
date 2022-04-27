#!/usr/local/bin/python2.7

from datetime import datetime
import sys, csv, re
import smtplib
from tabulate import tabulate
import pandas as pd
import json

class UtilityBelt(object):
    
    def __init__(self, iterable):
        self.iterable = iterable

    def write_data(self, filename, headers=None, mode=None):
        """writes data to a CSV"""
        if not mode:
            headers = headers if headers else []
            with open(filename, 'w') as f:
                writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
                if headers:
                        [writer.writerow(headers)]
                if isinstance(self.iterable, dict):
                    # [[writer.writerow(row) for row in i] for i in self.iterable]
                    [f.write('{0},{1}\n'.format(key, value)) for key, value in self.iterable.items()]
                elif any(isinstance(el, list) for el in self.iterable):
                    [writer.writerow(row) for row in self.iterable]
                elif any(isinstance(el, tuple) for el in self.iterable):
                    [writer.writerow(row) for row in self.iterable]
                else:
                    [writer.writerow([row]) for row in self.iterable]
            return None
        else:
            headers = headers if headers else []
            with open(filename, mode) as f:
                writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
                if headers:
                        [writer.writerow(headers)]
                if isinstance(self.iterable, dict):
                    # [[writer.writerow(row) for row in i] for i in self.iterable]
                    [f.write('{0},{1}\n'.format(key, value)) for key, value in self.iterable.items()]
                elif any(isinstance(el, list) for el in self.iterable):
                    [writer.writerow(row) for row in self.iterable]
                elif any(isinstance(el, tuple) for el in self.iterable):
                    [writer.writerow(row) for row in self.iterable]
                else:
                    [writer.writerow([row]) for row in self.iterable]
            return None

    def progress(self, startint, starttime, bar=None):
        """
        useage:
        iterable = range(1, 100)
        starttime = datetime.now()
        startint = ub(iterable).start()
        for i in iterable:
            time.sleep(.1)
            ub(iterable).progress(startint, starttime, bar=True)
            
        Progress: 8.081% | Timer: 0:00:00.827 | ########
        """
        try:
            sys.stdout.write('\r')
            start = startint.next()
            percentage = (100.0/len(self.iterable))*start
            timer = datetime.now() - starttime
            timer = str(timer)[:-3]
            if bar:
                sys.stdout.write("Progress: %.3f%% | Timer: %s | %-s" % (percentage, timer, '#'*start))
                sys.stdout.flush()
            else:
                sys.stdout.write("%-s %.3f%% | Timer: %s | %s" % ('===>', percentage, timer, start))
                sys.stdout.flush()
        except StopIteration:
            pass

    def start(self):
        return iter((range(1,len(self.iterable)+2)))
    
    @staticmethod
    def read_csv(path, col=None, all=True, return_headers=None):
        with open(path, 'rb') as zips:
            reader = csv.reader(zips)
            headers = reader.next()
            headers = filter(None, headers)
            if return_headers:
                return headers
            column = {}
            all_list = []
            for h in headers:
                column[h] = []
            for row in reader:
                all_list.append(row)
                for h, v in zip(headers, row):
                    column[h].append(v)
            if col:
                all = False
                return column[col]
            else:
                return all_list
        return None
            
    @staticmethod    
    def return_headers(path):
        headers = UtilityBelt.read_csv(path, return_headers=True)
        return headers
        
    @staticmethod
    def send_email(TO, FROM, subject, text):

        gmail_user = "tmthyjames@gmail.com"
        gmail_pwd = "mywhoqixnlwztref"
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), subject, text)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587) 
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
        except Exception as e:
            print e

    def remove(self, pattern):
        iterable = [re.sub(pattern, '', x) for x in self.iterable]
        return iterable
    
    def view_rows(self, n=None, tabs=None, headers=None):
        nrows = []
        for i in self.iterable[:n]:
            nrows.append(i)
        if tabs:
            print tabulate(nrows) if not headers else tabulate(nrows, headers=headers, tablefmt="orgtbl")
            return self.iterable
        else:
            return nrows
    
    def has_none(self, list2):
        nothere = []
        for i in self.iterable:
            if i not in list2:
                nothere.append(i)
        return nothere
    
    def length(self):
        length = []
        for i in self.iterable:
            if isinstance(i, type(None)):
                val = len(str(i))
            else:
                val = len(i)
            length.append(val)
        return max(length), min(length)
    
    def scale_length(self):
        length = [len(re.sub('(.*)\.','',str(x))) for x in self.iterable]
        return max(length)
    
    def types(self):
        TYPES = []
        for i in self.iterable:
            try:
                val = int(i)
                TYPES.append(type(val))
            except:
                try:
                    val = float(i)
                    TYPES.append(type(val))
                except:
                    val = type(i)
                    TYPES.append(val)
        TYPES = [re.sub('<type |>|\'', '', str(i)) for i in TYPES]
        return list(set(TYPES))

    @staticmethod
    def deets(path, headers):

        tab_headers = ['headers','type','length','scale']
        deets = []
        for head in headers:
            this = UtilityBelt.read_csv(path, col=head)
            length = UtilityBelt(this).length()
            types = UtilityBelt(this).types()
            if 'float' in str(types):
                scale = UtilityBelt(this).scale_length()
            else:
                scale = 'not a float'
            deets.append([head, types, length, scale])
        print tabulate(deets, headers=tab_headers, tablefmt="orgtbl")
        return None

    @staticmethod
    def csv_to_geojson(inpath, outpath, write=True):
        # Read in raw data from csv
        rawData = csv.reader(open(inpath, 'rb'), dialect='excel')

        # the template. where data from the csv will be formatted to geojson
        template = \
            """{"type":"Feature",
            "properties":{
                "ZIPCODE":"%s","CITY":"%s","STATE":"%s","AQI":"%s","DATE":"%s","HOUR":"%s","LAT":"%s","LON":"%s"},
                    "geometry":{
                        "type":"Point",
                        "coordinates":[%s,%s]}
                        },"""
        # the head of the geojson file
        output = '''{"type":"FeatureCollection",\n\t"features":[
        '''

        # loop through the csv by row skipping the first
        iter = 0
        for row in rawData:
            iter += 1
            if iter >= 2:
                zipcode = row[0]
                city = row[1]
                state = row[2]
                aqi = row[3]
                date = row[4]
                hour = row[5]
                lat = row[6]
                lon = row[7]
                output += template % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[7], row[6])

        # the tail of the geojson file
        output += ''']}'''
        output = re.sub('},\n\]}|},\]}', '}\n]}', output)
        # opens a geoJSON file to write the output to
        if write:
            outFileHandle = open(outpath, "w")
            outFileHandle.write(output)
            outFileHandle.close()
        else:
            return output

    @staticmethod
    def csv_to_json(inpath="inpath", outpath="None", return_as_list=None): 
        fn = inpath
        headers = ub.return_headers(fn)
        as_string = ', '.join([i for i in headers if re.search('zip', i, flags=re.IGNORECASE)]) if headers else None
        df = pd.read_csv(fn, converters={as_string: lambda x: str(x)}, skiprows=0 if headers else 2)
        myJSON = df.to_json(path_or_buf = None, orient = 'records', date_format = 'epoch', double_precision = 10, 
                            force_ascii = True, date_unit = 'ms', default_handler = None) 
        myJSON = json.loads(myJSON)
        if outpath:
            with open(outpath, 'w') as outfile:
                json.dump(myJSON, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
        
        if return_as_list:
            df = df.values.tolist()
            return df
        else:
            return myJSON

