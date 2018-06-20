#!/usr/bin/python
##-*- encoding: utf-8 -*-

import socket
import sys,getopt
import binascii
VERSION=0.2
#sys.setdefaultencoding('utf-8')

def getTempbyHex(readHex):
    return int("0x"+binascii.b2a_hex(readHex),16)/100.00 - 40

def usage():
    sys.stderr.write("""USAGE: %s [options]
    iw340 Reader for Linux/Unix
    options:
    -p, --port=PORT: port, a number, must be 5200 now.
    -h, --help:      show this usage.
    -H, --host=:     Hostname or IP address. default is 192.168.1.188
    -v, --version:   show version.

""" % (sys.argv[0], ))
if __name__ == '__main__':
  PORT = 5200
  HOSTNAME='192.168.1.188'
  try:
    opts, args = getopt.getopt(sys.argv[1:],
    "h:H:p:v",
     ["help", "host=","port=","version"]
    )
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-h","--help"):
      usage()
      sys.exit()
    elif o in ("-v", "--version"):
      print "iW340 Reader for Linux/Unix, Version ", VERSION
      sys.exit()
    elif o in ("-p", "--port"):
      try:
        PORT = int ( a )
      except ValueError:
        PORT = 5200
    elif o in ("-H", "--host"):
      HOSTNAME=a

  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  try:
    s.connect((HOSTNAME, PORT))
    s.send("\xbb\x80\x05") #Query for Temperature and Humiture from SHT10 Sensors
    result=s.recv(1024)
    s.close()
  except socket.error,msg:
    print 'Fail to connect the PCsensor iw340, Error code: '+  msg[1],', ', HOSTNAME,':',PORT
    sys.exit()
  Num=int(binascii.b2a_hex(result[3:4])) #Number of SHT10 Sensors
  for i in range(0,Num):
    first=4+i*4
    print getTempbyHex(result[first:(first+2)])

