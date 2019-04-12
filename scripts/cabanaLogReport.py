#
# This script generate report for each canbus message:
#      * frequency (in hz).
#      * bytes that doesnt change.
# usage:
# 1. place cabana log files in logs/
# 2. run: python cabanaLogReport.py
# 3. a new report.txt should now in logs/

import os
import csv
import glob

IN_FOLDER = "logs"


def get_avg_freq(bus_messages):
  first = None
  last = None
  last_time = None
  time_diff = []
  for time_val in bus_messages:
    time = time_val['time']

    if first is None:
      first = time
    if last_time is not None:
      diff = time - last_time
      time_diff.append(diff)

    last_time = time
    last = time

  if len(time_diff):
    # print len(time_diff)
    avg = round(sum(time_diff) / len(time_diff), 2)
    freq = str(int(round(1 / avg, 0))) + ' hz'
  else:
    avg = 'NaN'
    freq = 'NaN'
  return avg, freq, first, last


def get_mask(bus_messages):
  mask = None
  for time_val in bus_messages:
    val = time_val['val']
    split_val = list(val)
    if mask is None:
      mask = split_val
    else:
      count = len(split_val)
      for i in range(0, count):
        if mask[i] != '-' and mask[i] != split_val[i]:
          mask[i] = '-'
  return ''.join(mask)


def process_file(f):
  print "reading %s..." % f
  busVal = {}
  with open(f, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # skip the headers
    for row in reader:
      if row:
        time = row[0]
        addr = row[1]
        hexAddr = hex(int(addr)).lstrip('0x')
        bus = row[2]
        val = row[3]
        busAddr = "%s:%s" % (bus, hexAddr)
        if not busAddr in busVal:
          busVal[busAddr] = []
        busVal[busAddr] += [{'time': float(time), 'val': val}]

  report = f + ".report.txt"
  print "generating freq report: %s..." % report
  with open(report, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['busAddr', 'addr', 'avg', 'freq', 'first', 'last', 'duration', 'count', 'mask'])
    for busAddr in busVal:
      avg, freq, first, last = get_avg_freq(busVal[busAddr])
      mask = get_mask(busVal[busAddr])
      bus_addr = busAddr.split(':')

      writer.writerow([
        busAddr,
        int(bus_addr[1], 16),
        avg,
        freq,
        first,
        last,
        round(last - first, 2),
        len(busVal[busAddr]),
        mask
       ])


os.chdir(os.path.join('.', IN_FOLDER))
for f in glob.glob("*.csv"):
    process_file(f)
