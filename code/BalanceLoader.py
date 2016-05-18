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

#This is load balancing script used to do custom routing in SDN-network
#Author Asmo Korkiatupa

#maaritetään funktio loadBalance
def loadBalance():
	#asetetaan apumuuttuja
    pushed = False
    
    #haetaan verkossa liikkuvat paketit yhden sekuntin intervallilla while loopissa
    while True:
        response = requests.get('http://192.168.2.102:8008/metric/ALL/ifinucastpkts/json')
        data = response.json()
        
        #parsitaan vastauksesta metricValue
        for i in data:
            metric = i['metricValue']
        print metric
        
		#timestamp on aikaleima muuttuja jota käytetaan lokitiedon kirjoituksessa
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time.sleep(1)
        
		#jos verkossa liikkuu yli 1000 pakettia / sekunti muutetaan reititysta.
        if metric >= 1000:
            
            if pushed == False:
				#pusketaan flow saannot floodlight-kontrollerille
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
				#jos lokitiedosto on jo olemassa lisataan sinne rivi ja aikaleima
                if os.path.isfile("rulelog.txt"):
					#avataan tiedosto lisataan seuraava rivi parametri "a" tarkoitta appendia.
                    file = open("rulelog.txt","a")
                    file.write(timestamp+" Flow rules PUSHED\n")
                    file.close()
					#tiedosto suljetaan.
				#jos lokitiedostoa ei ole olemassa sellainen luodaan.	
                else:
					#lokitiedostoon kirjoitus ja rivin vaihto \n
                    file = open("rulelog.txt","w")
                    file.write(timestamp+" Flow rules PUSHED and file created\n")
                    file.close()
					#tiedoston sulkeminen
			#jos saannot floodlight-kontrollerille on jo puskettu ja kuorma yli 1000pkt/s
			# tulostetaan jako kaytossa
            if pushed == True and metric >=1000:
			
                print "jako kaytossa"
		#jos floodlight-kontrollerille on puskettu flow saannot ja value alle 1000		
        if pushed == True and metric <=1000:
			
			# poistetaan flow saannot, kutsutaan staticflow pusherin remove metodia
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
			#apumuuttuja falseksi
            pushed = False
            print "Kuormanjako poistettu"
			#kirjoitetaan lokitiedostoon, etta kuorman jakaminen poistettu
            file = open("rulelog.txt","a")
            file.write(timestamp+" Flow rules DELETED\n")
            file.close()
			#tiedosto suljetaan.

#static flow pusher luokka
class StaticFlowPusher(object):
	#kaytetaan uuden instanssin luomisessa 
    def __init__(self, server):
        self.server = server
    
    def get(self,data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])
    #kaytetaan flow saantojen puskemiseen    
    def set(self,data):
        ret = self.rest_call(data,'POST')
        return ret[0] == 200
    #flow saantojen poistaminen    
    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200
    #rest kutsun muotoilu    
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
#luodaan uusi ilmentyma staticflowpusherista
#parametriksi asetetaan floodlight-kontrollerin ip osoite.    
pusher = StaticFlowPusher('192.168.2.104')

#verkkoon puskettavat flow saannot
#kytkin 01 eli s1
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
#kytkin 04 eli s4
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
#kytkin 03 eli s3    
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
#kytkin 02 eli s2 
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
#suorittaa ohjelman ajamisen. eli kutsuu funktiota loadBalance
#loadBalance funktion sisalla looppi joten pyorii kunnes sammutetaan ctrl+c
loadBalance()
    

