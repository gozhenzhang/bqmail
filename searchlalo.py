#!/usr/bin/env python
#
#
#

import distaz, math
import urllib.request as rq
import os
import re
import sys, getopt
import glob

def Usage():
    print('Usage: python searchlalo.py -Rlon1/lon2/lat1/lat2 -Dlon/lat/dis1/dis2 -Yyear1/mon1/day1/year2/mon2/day2 -Cchannel -K')
    print('-R   -- Search range.')
    print('-D   -- Search by distance.')
    print('-Y   -- Date range')
    print('-C   -- Channel (e.g., BHZ)')
    print('-K   -- Output Google Earth kml file.')
    

try:
    opts,args = getopt.getopt(sys.argv[1:], "hR:D:KO:Y:C:")
except:
    print('arguments are not found!')
    Usage()
    sys.exit(1)

iskml = 0
islalo = 0
isyrange = 0
ischan = 0
for op, value in opts:
    if op == "-R":
        lat_lon = value
        islalo = 1
    elif op == "-K":
        iskml = 1
    elif op == "-D":
        lat_lon = value
    elif op == "-Y":
        yrange = value
        isyrange = 1
    elif op == "-C":
        chan = value
        ischan = 1
    elif op == "-h":
        Usage()
        sys.exit(1)
    else:
        Usage()
        sys.exit(1)
        
lat_lon_split = lat_lon.split('/')    
if islalo:
    lon1 = lat_lon_split[0]
    lon2 = lat_lon_split[1]
    lat1 = lat_lon_split[2]
    lat2 = lat_lon_split[3]
    lalo = lon1+'_'+lon2+'_'+lat1+'_'+lat2
else:
    lon = lat_lon_split[0]
    lat = lat_lon_split[1]
    dis1 = float(lat_lon_split[2])
    dis2 = float(lat_lon_split[3])
#    print(lon,lat,dis)
#    [lat1,lon1] = distaz.latlon_from(float(lat),float(lon),225,dis*math.sqrt(2))
#    [lat2,lon2] = distaz.latlon_from(float(lat),float(lon),45,dis*math.sqrt(2))
#    print(lon1,lon2,lat1,lat2)
    lon1 = str(0)
    lat1 = str(-90)
    lon2 = str(0)
    lat2 = str(90)
    lalo = lon+'_'+lat+'_'+lat_lon_split[2]
   
if isyrange:
    yrange_sp = yrange.split("/")
    year1 = yrange_sp[0]
    mon1 = yrange_sp[1]
    day1 = yrange_sp[2]
    year2 = yrange_sp[3]
    mon2 = yrange_sp[4]
    day2 = yrange_sp[5]
    if ischan:
        url = 'http://ds.iris.edu/cgi-bin/xmlstationinfo?minlat='+lat1+'&maxlat='+lat2+'&minlon='+lon1+'&maxlon='+lon2+'&timewindow='+year1+'/'+mon1+'/'+day1+'-'+year2+'/'+mon2+'/'+day2+'&chan='+chan
    else:
         url = 'http://ds.iris.edu/cgi-bin/xmlstationinfo?minlat='+lat1+'&maxlat='+lat2+'&minlon='+lon1+'&maxlon='+lon2+'&timewindow='+year1+'/'+mon1+'/'+day1+'-'+year2+'/'+mon2+'/'+day2
elif ischan:
    url = 'http://ds.iris.edu/cgi-bin/xmlstationinfo?minlat='+lat1+'&maxlat='+lat2+'&minlon='+lon1+'&maxlon='+lon2+'&chan='+chan
else:
    url = 'http://ds.iris.edu/cgi-bin/xmlstationinfo?minlat='+lat1+'&maxlat='+lat2+'&minlon='+lon1+'&maxlon='+lon2
    
response = rq.urlopen(url)
html = str(response.read())
find_re = re.compile(r'<station\s.+?"\s/>',re.DOTALL)

    
for info in find_re.findall(html):
    sta_info = re.split('\w+="|"\s+?\w+="|"\s/>',info)
    if sta_info == []:
        continue
    network = sta_info[1]
    staname = sta_info[2]
    stlat = sta_info[4]
    stlon = sta_info[5]
    if sta_info[-2] == 'No archive data':
        continue
    yrange1 = sta_info[-5]
    yrange2 = sta_info[-4]
    if not islalo:
        delta = distaz.distaz(float(lat),float(lon),float(stlat),float(stlon))
        if dis1 < delta.delta < dis2:
            print(network+' '+staname+' '+stlat+' '+stlon+' '+yrange1+' '+yrange2)
    else:
        print(network+' '+staname+' '+stlat+' '+stlon+' '+yrange1+' '+yrange2)


        

if iskml:
    google = open('Station_'+lalo+'.kml','w+')
    google.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.google.com/earth/kml/2.0"><NetworkLink><name>Selected stations</name><description>Station List</description><Link><href>http://www.iris.edu/cgi-bin/kmlstationinfo?minlat='+lat1+'&amp;maxlat='+lat2+'&amp;minlon='+lon1+'&amp;maxlon='+lon2+'&amp;kmz=1</href><refreshMode>onInterval</refreshMode><refreshInterval>86400</refreshInterval></Link></NetworkLink></kml>')
    
