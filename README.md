I. Introduction
------------------------------------------------
This python script is for solving the Test1 Question described bellow, it has been tested with 3 mimic services in Cygwin Linux as explainning in following.

II Origent Question
------------------------------------------------
Assumption: 

"rbcapp1" is a critical application that needs to be monitored and its status should be recorded into Elasticsearch. This Application depends on 3 services: httpd, rabbitMQ and postgreSQL .

If any of these services are down, "rbcapp1" state will be considered "DOWN" otherwise it is "UP".

Notes:

·       Please assume all these services runs under Linux machines.

·       Please include a READ.me file to describe the answers.

 

TEST1:  Assume all 3 services are running on the same server as Linux services.

    Write a Python script that monitors these services and creates a JSON object with application_name, application_status and host_name.

Sample JSON Payload

{ 
   "service_name":"httpd",
   "service_status":"UP",
   "host_name":"host1"
}

Please write this JSON object to a file named {serviceName}-status-{@timestamp}.json

    Write a simple Python REST webservice that: 

        Accepts the above created JSON file and writes it to Elasticsearch 
        Provide a second endpoint where the data can be retrieved, i.e 

POST /add  à Insert payload into Elasticsearch

GET /health_check à Return the Application status (“UP” or “DOWN”)

Sample calls

https://myservice.rbc.com/add

https://myservice.rbc.com/health_check

II. File list
------------------------------------------------
test1.py  #python script

#python script generated json files: 
httpd-status-2020_08_26 19_18_07.json  
bash-status-2020_08_26 19_18_07.json
ps-status-2020_08_26 19_18_07.json

hn.txt ,  #host_name in my Cygwin Linux.


IV. Design Decisions and Test Issues explaination.
------------------------------------------------
Since I only have a Cygwin to mimic Linux in my Windows 10, I don't real set up httpd, rabbitMQ and postgreSQL services in my Cygwin. 
But I use "ps au | grep service_name" command to monitor whether the service exist in my Linux. 
For simplicity and demostration, I have tested 3 services: httpd, bash, ps (The last two processes are running,
so they are detected and returned in the getfeedback() function).
In linux which have apache webserver, postgres database, message system rabbitmq, just replace the services name as following comment:
	services = ('ps','httpd','bash')
	#services = ('postgres','httpd','rabbitmq')
	
add() function implements the task for POST payload into supposed remote restful server,providing the remote endpoint where stored the json data,
while health_check() implements the task of GET json file and return the status of application.

After called getfeedback(), the main() function do a judgement based on condition: 
'If any of these services are down, "rbcapp1" state will be considered "DOWN" otherwise it is "UP".'

Then stored the status into a dictionary together with the host_name, service_name, 
after that used json.dump to serialize dictionary to json file, and call add() to post json to RestAPI.

health_check() function is for GET the application status from RestAPI.

