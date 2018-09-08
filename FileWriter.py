import os
import datetime
from pathlib import Path
'''
>>> import os
>>> os.path.join('app', 'subdir', 'dir', 'filename.foo')
'app/subdir/dir/filename.foo'

'''

class FileWriter:
    path = ''

    def __init__(self,debug=0, eventLogFile=0):
        #path = 'data/'+eventLogFile["EventType"]+'/'+eventLogFile["LogDate"]+'_'+eventLogFile["Id"]+'.csv'
        self.path = Path("data/"+eventLogFile["EventType"])
        self.fileName = eventLogFile["Id"]+'.csv' #eventLogFile["LogDate"]+'_'+eventLogFile["Id"]+'.csv'
        self.filePath = self.path / self.fileName
        self.debug = debug
        if self.debug:
            print("[DEBUG] writing eventlog file to path>>", self.filePath)
            print( self.path.exists())

        self.path.mkdir(parents=True, exist_ok=True)
        # if not os.path.exists(os.path.dirname(self.path)):
        #     os.makedirs(os.path.dirname(self.path))

    def writeFile(self, input):
        with open(self.filePath, 'a') as outputlog:
            outputlog.write(str(input))
            outputlog.write("\n")