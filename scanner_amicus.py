__author__ = 'thomros'

import argparse
import logging
from lxml import etree

argparser = argparse.ArgumentParser(
    description='Scan an LAC Amicus and save record to a the open data scanner database'
)
argparser.add_argument('-f', '--file', action='store', default='', dest='source',
                       help='Amicus XML file name')
argparser.add_argument('-l', '--log', action='store', default='', dest='log_filename', help='Log to file')

args = argparser.parse_args()

if args.log_filename != '':
    logging.basicConfig(filename=args.log_filename, level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

if args.source == '':
  print("No source file provided")
  exit()

try:
  event_types = ("end",)
  parser = etree.XMLPullParser(event_types,  remove_comments=True, recover=True)
  with open(args.source, mode='rt') as amstream:
    for line in amstream:
      parser.feed(line)
      for action, elem in parser.read_events():
        if elem.tag == 'record':
          print("%s: %s" % (action, elem.tag))
          #elem.clear()
  parser.close()

except Exception, e:
    logging.error(e)

