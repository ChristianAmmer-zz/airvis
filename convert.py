import csv
import json
import sys
import dateutil.parser
import datetime
import math

# DHT Columns
# 5 ... Date
# 6 ... Temperature
# 7 ... Humidity

# SDS Columns
# 5 ... Date
# 6 ... PM10
# 9 ... PM2.5

def datehmw(dt):
  if dt.minute % 30 or dt.second:
    return dt + datetime.timedelta(
      minutes = 30 - dt.minute % 30,
      seconds = -(dt.second % 60))
  else:
    return dt

def parseCSV(filename, rownum):
  sdscsv = open(filename, 'r')
  reader = csv.reader(sdscsv, delimiter=';')
  reader.next() # skip header
  hmw = {}
  for row in reader:
    key = datehmw(dateutil.parser.parse(row[5]))
    if key in hmw:
      hmw[key][0] += 1
      hmw[key][1] += float(row[rownum])
    else:
      hmw[key] = [1, float(row[rownum])]
  for key, val in sorted(hmw.items()):
    print '[Date.UTC({}, {}, {}, {}, {}), {}],'.format(key.year, key.month, key.day, key.hour, key.minute, val[1] / val[0])

print '$(\'#container1\').highcharts({ xAxis: { type: \'datetime\' }, series: ['
print '{name: \'PM10\', data: ['
parseCSV('{}_sds011_sensor_11518.csv'.format(sys.argv[1]), 6)

print ']},'
print '{ name: \'PM2.5\', data: ['
parseCSV('{}_sds011_sensor_11518.csv'.format(sys.argv[1]), 9)
print ']}]});'
print '\n'

print '$(\'#container2\').highcharts({ xAxis: { type: \'datetime\' }, series: ['
print '{name: \'Temp\', data: ['
parseCSV('{}_dht22_sensor_11519.csv'.format(sys.argv[1]), 6)

print ']},'
print '{ name: \'Humidity\', data: ['
parseCSV('{}_dht22_sensor_11519.csv'.format(sys.argv[1]), 7)
print ']}]});'
print '\n'
