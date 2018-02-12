import socket
#import sys

class UDPConnect():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

    def send(self, message):
        try:
            # print('sending message')
            self.sock.sendto(bytes(message, "utf-8"), (self.ip, self.port))
        except Exception as e:
            print('ERROR %s \n' % e)
            print('uhh oo failed sending to ipaddress: %s on port: %s' % (message, self.ip, self.port))
            # self.sock.close()
        finally:
            pass
            # print('message success!')
            #self.sock.close()