# Automation Assignment

## Getting Started

This app demonstrates basic network automation scenario by checking current device config and then doing some changes 
in configuration as per the request.

## Technologies/Libraries Used

~~~
 1. Flask
 2. Robot Framework
 3. ODL
 4. SQLite
 5. Rest
 6. NETCONF
 7. Ncclient
 8. YANG
 9. Docker
 10.Jenkins
             
~~~

## ODL(Open Day Light)
ODL's Netconf-testtool simulates NETCONF devices. To simulate a device, testtool jar is needed to be run with appropriate
flags.

###Example:

```
java -jar <netconf-testtool-1.1.0-SNAPSHOT-executable.jar> --schemas-dir SCHEMAS-DIR <yang-folder>
```


## Flask

By using flask, REST API's have been created to automate the network configurations.
Inside REST api's implementation, **ncclient** library has been used to Communicate to NETCONF devices using different 
NETCONF operations(edit-config, get etc.) 

###  Sample Input:
```
POST: http://localhost:5000/automation

{
    "device-name": "test-1",
    "ip-address": "1.2.3.4",
    "interface-name": "ethernet-1",
    "shutdown": "yes"
}

GET: http://localhost:5000/automation/ethernet-1
```

###  Sample Output:
```
POST
201 Created
{
    "info": "request processed successfully"
}

GET
200 OK
{
    "admin-state": "up",
    "oper-status": "up"
}
```

## Robot Framework:

By Robot Framework, we have automated REST calls to the Flask application. We can easily send REST calls through 
Robot and verify the output as well as HTTP response code.
HTML report/logs are generated after the execution of test cases which are easy to understand.
Total 5 automated test cases are currently present in the Test Suite.

To Execute test cases:
```
robot RestAutomation.robot
```

## SQLite:

SQLite is used to store device interactions which app does through NETCONF. Currently, we store ID, REST Request Method,
NetConf Operation, Interface Name and NETCONF response in DB.

There is a special rest endpoint written to showcase current records present in the DB in HTML format.
```
GET: http://localhost:5000/automation/records
```

## Docker and Jenkins

Dockerfile is present to build the Docker image and run the service as a Docker container.
```
sudo docker build --tag  automation-docker .
sudo docker run --name automation-docker -p 5001:5001 automation-docker
```

Jenkins Pipeline is created just to fetch the code from the Github repo and check for the Dockerfile inside it.
