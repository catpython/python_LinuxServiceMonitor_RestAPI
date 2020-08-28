import json
import time
import os
import subprocess
import sys
import requests


'''
x='{"service_name":"httpd","service_status":"UP","host_name":"host1"}'
# parse x:
y = json.loads(x)

# the result is a Python dictionary:
print(y["service_name"])


# a Python object (dict):
x = { 
	"service_name":"httpd",
	"service_status":"UP",
	"host_name":"host1"
}

# convert into JSON:
y = json.dumps(x)

print(y)
# the result is a JSON string:

'''

timestp = time.strftime("%Y_%m_%d %H_%M_%S", time.localtime())

def health_check():		
	application_name = "rbcapp1"  
	# defining a params dict for the parameters to be sent to the API 
	PARAMS = {'application_name':application_name} 
	#r = requests.get('https://api.github.com/events')
	
	url = 'https://myservice.rbc.com/health_check'
	r = requests.get(url, params = PARAMS)
	#print(r.text)
	
	rs = r.status_code
	print(rs)
	if rs == 200:
		print("Request successfull")
		# extracting data in json format 
		data = r.json() 		  
		print(data)
		print(data['application_status'])	
		return data['application_status']
	else:
		print("Request returned an error")
		return None
	
	

# requests post json file with RestAPI
def add(file):
	with open(file) as f:
		payload = json.load(f)
		#print(payload)
		#print(type(payload))
	
	#url = "https://httpbin.org/post"	
	url = "https://myservice.rbc.com/add"
	
	#myobj = {'somekey': 'somevalue'}
	x = requests.post(url, data = payload)

	#print the response text (the content of the requested file):
	#print(x.text)

	
def getfeedback(cmd):
	res= subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	try:
		out = res.stdout.read()	
		res.stdout.close()
		out = out.strip()
	except OSError as e:
		print("Execution failed:", e)	
		print "Error: ", sys.exc_info()[1]
	return out
	
	
def main():	

	host_name_cmd = "hostname"
	host_name = getfeedback(host_name_cmd)

	#services = ('postgres','httpd','rabbitmq')
	services = ('ps','httpd','bash')

	# suppose application status flag is UP in begining, will change it according to service status.
	app_status = 'UP' 

	for s in services:
		cmd = "ps au | grep " + s
		r = getfeedback(cmd)
		if len(r)> 1:
			pstatus = 'UP'
		else:
			pstatus = 'DOWN'
		
		x = { 
		"service_name":s,
		"service_status":pstatus,
		"host_name":host_name
		}
		#creates a JSON object with service_name, service_status and host_name, as Sample JSON Payload shown:
		'''
		{ 
	   "service_name":"httpd",
	   "service_status":"UP",
	   "host_name":"host1"
		}
		'''
		
		file = s+'-status-'+timestp+'.json'
		with open (file, 'w') as fw:
			json.dump(x, fw)
			
		add(file)
		
		# if any service process among three is DOWN, then application status is DOWN
		if pstatus == 'DOWN':
			app_status = 'DOWN' 


	# creates a JSON object with application_name, application_status and host_name.

	app_name = 'rbcapp1'

	x = { 
	"application_name":app_name,
	"application_status":app_status,
	"host_name":host_name
	}

	file = app_name + '-status-' + timestp + '.json'
	with open (file, 'w') as fw:
		json.dump(x, fw)
	add(file)
		

if __name__ == "__main__":	
	main()
	hs= health_check()	
	
	
	
	