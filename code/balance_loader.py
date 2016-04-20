import urllib
import urllib2
import requests
import json
from pprint import pprint
import time
#haetaan verkossa liikkuvat paketit
def getMetric():
    response = requests.get('http://192.168.2.102:8008/metric/ALL/ifinucastpkts/json')
    
    data = response.json()
    
    #print pprint(data)
    for i in data:
        metric = i['metricValue']
    print metric
    time.sleep(1)
    if metric >= 100:
        print "verkossa liikennetta"
    
while True:
    getMetric()
    
