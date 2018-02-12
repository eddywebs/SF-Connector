import requests, os, csv, datetime, json, sys, argparse, logging
from requests.auth import HTTPBasicAuth
from FileWriter import FileWriter
from SalesforceApi import SalesforceApi
from io import StringIO
from UDPConnect import UDPConnect

sfEnv = {}
_debug = 0

parser = argparse.ArgumentParser(description="Salesforce Event Monitoring Log Retrieval\n\nThis python script will authenticate against Salesforce and pull json responses containing api logs that may be downloaded for consumption by a log processing application. Request responses are logged in the /logs directory. Each run of this app will generate multiple requests, those requests are merged into a single log file")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('orgName', nargs='?', default='', help='enter the org key of the environment contained in .env')
group.add_argument('-e', '--env', help='display list of Salesforce environments contained in the .env file', action='store_true')

parser.add_argument('-d', '--debug', help='print results of program to terminal', action='store_true')
parser.add_argument('-l', '--log', help='prints log of http requests to /logs folder', action='store_true')
parser.add_argument('-v', '--verbose', help='prints full http request and response (status code and headers) '
                                            'log to terminal. **NOTE, this argument prints a lot of information to the '
                                            'terminal', action='store_true')
parser.add_argument('-s', '--send', help='sends the logs the graylog server ip and port via UDP',
                    dest='graylog_server', action='store')
args = parser.parse_args()

if args.orgName != '':
    with open('.env') as json_data:
        d = json.load(json_data)
    sfEnv = d[args.orgName]
    print (">>Fetching logs from, %s"  % sfEnv['salesforceURL'])

if args.debug:
    _debug=1
    print (">>Debug turned on")
if args.env:
    print (">>The following environments have credentials stored: ")
    with open('.env') as json_data:
        d = json.load(json_data)
    for item in d:
        print ("  -  %s" % item)
    print (">>You can use one of the sites by entering:\n\n  $ python retrievePackage orgname\n")
    sys.exit()
if args.log:
    logStorageLocation = 'logs/'+datetime.datetime.now().strftime('%Y%m%d-%H%M.%S')+'.log'
    logging.basicConfig(filename= logStorageLocation, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    print (">>Logging turned on. File can be found at, %s" % logStorageLocation)
if args.verbose:
    try: # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

sa = SalesforceApi(environment=sfEnv, debug=_debug)

sa.authenticate()
eventLogFile = set()
# retrieve Event Logs
response = sa.queryEventLogFile()
for record in response['records']:
    eventLogFile.add(sa.eventLogFile(record))

if args.graylog_server:
    print('sending logs to graylog-server %s' % args.graylog_server)
    ip, port = args.graylog_server.split(':')

    if (port==''):
        raise ValueError('port is missing please provide a valid port for sending UDP messages')

    udp = UDPConnect(ip, port)
    for logFile in eventLogFile:
        # testdata = StringIO(foo.content.decode('utf-8'))
        reader = csv.DictReader(StringIO(logFile.content.decode('utf-8')))
        for row in reader:
            #add GELF required fields
            row["version"] = '1.1'
            row["host"] = 'salesforce'
            row["short_message"] = row["EVENT_TYPE"]+' event entry'
            udp.send(json.dumps(row))
            print(json.dumps(row))

    #finally close the socket
    udp.sock.close()
    print('all done sending messages, lets goto sleep :)')