# Salesforce Event Monitoring Log connector
A lightweight Python command line utility that fetches Salesforce Event Monitoring Log Files for the purpose of consumption by log management and monitoring software. Use env.bak file as sample .env file.

# Usage

## Run Locally
Only Retrieve logs for a given environment and save it in data dir
```
$ retrieveLogs.py {orgname} 
>>Fetching logs from, orgname.cs32.my.salesforce.com
```

Retrieve logs for a given environment and send it to graylog server 
```
$ retrieveLogs.py {orgname} -s {graylogserver ip }:{udp input stream port}
for e.g. retrieveLogs.py orgname1 -s 104.236.226.67:12201
>>Fetching logs from, orgname.cs32.my.salesforce.com
```
Print debug output to terminal
```
$ retrieveLogs.py orgname -d
>>Fetching logs from, gsa-red--reddv10dvn.cs32.my.salesforce.com
>>Debug turned on
[TRUNCATED]
```
Display list of environments stored in .env (sample .env.bak file)
```
$ retrieveLogs.py -e
>>The following environments have credentials stored:
  - orgname1
  - orgname2
  - orgname3
>>You can use one of the sites by entering:

  $ python retrievePackage orgname
```
Display help
```
$ python retrieveLogs.py -h
usage: retrieveLogs.py [-h] [-e] [-d] [-l] [-v] [orgName]

Salesforce Event Monitoring Log Retrieval This python script will authenticate
against Salesforce and pull json responses containing api logs that may be
downloaded for consumption by a log processing application. Request responses
are logged in the /logs directory. Each run of this app will generate multiple
requests, those requests are merged into a single log file

positional arguments:
  orgName        enter the org key of the environment contained in .env

optional arguments:
  -h, --help     show this help message and exit
  -e, --env      display list of Salesforce environments contained in the .env
                 file
  -d, --debug    print results of program to terminal
  -l, --log      prints log of http requests to /logs folder
  -v, --verbose  prints full http request and response (status code and
                 headers) log to terminal. **NOTE, this argument prints a lot
                 of information to the terminal
  -s, --send    sends the fetched log files to a graylog input stream on UDP port                
```
Retrieve basic logs and store in logs/ directory
```
$ retrieveLogs.py {orgname} -l
>>Fetching logs from, orgname.cs32.my.salesforce.com
>>Logging turned on. File can be found at, logs/20161204-2027.34.log
```
Retrieve logs and display robust request log information including HTTP requests, response codes, and headers
```
$ retrieveLogs.py {orgname} -v
>>Fetching logs from, orgname.cs32.my.salesforce.com
[TRUNCATED]
```

