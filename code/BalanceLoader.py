import httplib
import json
import urllib
import urllib2
import requests
import json
from pprint import pprint
import time
import datetime
import os.path


def loadBalance():
    pushed = False
    
    #haetaan verkossa liikkuvat paketit yhden sekuntin intervallilla.
    while True:
        response = requests.get('http://192.168.2.102:8008/metric/ALL/ifinucastpkts/json')
        data = response.json()
        
        
        for i in data:
            metric = i['metricValue']
        print metric
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(1)
        
        if metric >= 1000:
            
            if pushed == False:
                pusher.set(flow1_1)
                pusher.set(flow1_2)
                pusher.set(flow1_3)
                pusher.set(flow2_1)
                pusher.set(flow2_2)
                pusher.set(flow3_1)
                pusher.set(flow3_2)
                pusher.set(flow4_1)
                pusher.set(flow4_2)
                pusher.set(flow4_3)
                print "Kuorman jako otettu kayttoon"
                pushed = True
                if os.path.isfile("rulelog.txt"):
                    file = open("rulelog.txt","a")
                    file.write(timestamp+" Flow rules PUSHED\n")
                    file.close()
                else:
                    file = open("rulelog.txt","w")
                    file.write(timestamp+" Flow rules PUSHED and file created\n")
                    file.close()
            if pushed == True and metric >=1000:
                print "jako kaytossa"
        if pushed == True and metric <=1000:
            pusher.remove('application/json',flow1_1)
            pusher.remove('application/json',flow1_2)
            pusher.remove('application/json',flow1_3)
            pusher.remove('application/json',flow2_1)
            pusher.remove('application/json',flow2_2)
            pusher.remove('application/json',flow3_1)
            pusher.remove('application/json',flow3_2)
            pusher.remove('application/json',flow4_1)
            pusher.remove('application/json',flow4_2)
            pusher.remove('application/json',flow4_3)
            pushed = False
            print "Kuormanjako poistettu"
            file = open("rulelog.txt","a")
            file.write(timestamp+" Flow rules DELETED\n")
            file.close()
def setValues():
    pushed = False
class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server
    
    def get(self,data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
        
    def set(self,data):
        ret = self.rest_call(data,'POST')
        return ret[0] == 200
        
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
        
    def rest_call(self,data,action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret
        
pusher = StaticFlowPusher('192.168.2.104')
#ohjataan 1 porttiin tuleva data kaikkiin portteihin. all metodilla
flow1_1 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"flow_mod_1_1",
    "cookie":"0",
    "priority":"32768",
    "in_port":"1",
    "set_ipv4_src":"10.0.0.1",
    "set_ipv4_dst":"10.0.0.2",
    "active":"true",
    "actions":"output=2"
    }
flow1_2 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"flow_mod_1_2",
    "cookie":"0",
    "priority":"32768",
    "in_port":"2",
    "set_ipv4_src":"10.0.0.2",
    "set_ipv4_dst":"10.0.0.1",
    "active":"true",
    "actions":"output=1"
    }
flow1_3 = {
    'switch':"00:00:00:00:00:00:00:01",
    "name":"flow_mod_1_3",
    "cookie":"0",
    "priority":"32768",
    "in_port":"3",
    "set_ipv4_src":"10.0.0.2",
    "set_ipv4_dst":"10.0.0.1",
    "active":"true",
    "actions":"output=1"
    }
#sama -> all duplicates
flow4_1 = {
    'switch':"00:00:00:00:00:00:00:04",
    "name":"flow_mod_4_1",
    "cookie":"0",
    "priority":"32768",
    "in_port":"3",
    "set_ipv4_src":"10.0.0.2",
    "set_ipv4_dst":"10.0.0.1",
    "active":"true",
    "actions":"output=2"
    }
flow4_2 = {
    'switch':"00:00:00:00:00:00:00:04",
    "name":"flow_mod_4_2",
    "cookie":"0",
    "priority":"32768",
    "in_port":"2",
    "set_ipv4_src":"10.0.0.1",
    "set_ipv4_dst":"10.0.0.2",
    "active":"true",
    "actions":"output=3"
    }
flow4_3 = {
    'switch':"00:00:00:00:00:00:00:04",
    "name":"flow_mod_4_3",
    "cookie":"0",
    "priority":"32768",
    "in_port":"1",
    "set_ipv4_src":"10.0.0.1",
    "set_ipv4_dst":"10.0.0.2",
    "active":"true",
    "actions":"output=3"
    }
    
flow3_1 = {
    'switch':"00:00:00:00:00:00:00:03",
    "name":"flow_mod_3_1",
    "cookie":"0",
    "priority":"32768",
    "in_port":"1",
    "active":"true",
    "actions":"output=2"
    }

flow3_2 = {
    'switch':"00:00:00:00:00:00:00:03",
    "name":"flow_mod_3_2",
    "cookie":"0",
    "priority":"32768",
    "in_port":"2",
    "active":"true",
    "actions":"output=1"
    }

flow2_1 = {
    'switch':"00:00:00:00:00:00:00:02",
    "name":"flow_mod_2_1",
    "cookie":"0",
    "priority":"32768",
    "in_port":"1",
    "set_ipv4_src":"10.0.0.1",
    "set_ipv4_dst":"10.0.0.2",
    "active":"true",
    "actions":"output=2"
    }

flow2_2 = {
    'switch':"00:00:00:00:00:00:00:02",
    "name":"flow_mod_2_2",
    "cookie":"0",
    "priority":"32768",
    "in_port":"2",
    "set_ipv4_src":"10.0.0.2",
    "set_ipv4_dst":"10.0.0.1",
    "active":"true",
    "actions":"output=1"
    }

loadBalance()
    

