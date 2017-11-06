#!/usr/bin/env python
#
#Author: Mijian Xu at NJU
#
#Revision History:
#   2014/11/06
#   2015/01/05
#   2015/02/11
#   2015/04/29
#   2015/05/01
#   2015/09/26
#   2015/11/06
#   2017/09/11
#

import argparse
import datetime
import getopt
import os
import re
import sys
import time
from obspy import taup
from bqmail import distaz
from bqmail.util import sendmail, generatemsg
try:
    import configparser
    config = configparser.ConfigParser()
except:
    import ConfigParser
    config = ConfigParser.ConfigParser()


def Usage():
    print('Usage:')
    print('python bqmai_oldl.py -Nnetwork -Sstation -b -Bsec_begin/sec_end [-Cchannel] [-Plat/lon/phase] [-Llocation] [-cdatetimefile] [-Fformat] [-Mmagmin/magmax] head.cfg')
    print('-N   -- Network.')
    print('-S   -- Station.')
    print('-b   -- Limit to events occurring on or after the specified start time.\n'
          '        Date and time format: YYYY-MM-DDThh:mm:ss (e.g., 1997-01-31T12:04:32)\n'
          '                              YYYY-MM-DD (e.g., 1997-01-31)')
    print('-e   -- Limit to events occurring on or before the specified end time\n'
          '        with the same date and time format as \"-b\".')
    print('-B   -- Time before/after origal time of events in seconds.')
    print('-C   -- Channel (e.g., ?H?, HHZ, BH?). Default: BH?')
    print('-P   -- specify the lat/lon of station and require data by phase. e.g., 20/100/SKS')
    print('-L   -- Location identifier.')
    print('-c   -- Directory of date time file. format: "2015,01,04,1,0,0 2015,01,04,10,0,0"')
    print('-F   -- File format (SEED or miniseed). Default: SEED')
    print('-M   -- Magnitude range.')
    print('head.cfg   -- Config file.')
    print('Example: bqmail -NCB -SNJ2 -b2015-2-3 -e2015-4-3 -P32.05/118.85/P -B-200/1000 head.cfg')
    print('         bqmail -NIC -SBJT -b2015-2-3T00:12:23 -e2015-4-3 -B-100/600 -L10 -Fminiseed head.cfg')

def getargs():
    parser = argparse.ArgumentParser(description='Script for sending mail via BREQ fast\n'
                                                 'python bqmai_oldl.py -Nnetwork -Sstation -b -Bsec_begin/sec_end [-Cchannel] [-Plat/lon/phase] [-Llocation] [-cdatetimefile] [-Fformat] [-Mmagmin/magmax] head.cfg')
    parser.add_argument('-N', dest='network', help='Network')
    parser.add_argument('-S', dest='station', help='Station')
    parser.add_argument('-b', dest='starttime', help='Limit to events occurring on or after the specified start time.\n'
                                                     'Date and time format: YYYY-MM-DDThh:mm:ss (e.g., 1997-01-31T12:04:32)\n'
                                                     '                      YYYY-MM-DD (e.g., 1997-01-31)')
    parser.add_argument('-e', dest='endtime', help='Limit to events occurring on or before the specified end time\n'
                                                   'with the same date and time format as \"-b\".')
    parser.add_argument('-B', dest='timerange', help='Time before/after origal time of events in seconds.')
    parser.add_argument('-C', dest='chan', help='Channel (e.g., ?H?, HHZ, BH?). Default: BH?')
    parser.add_argument('head', type=str, help='Config file')