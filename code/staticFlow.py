import httplib
import json

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
