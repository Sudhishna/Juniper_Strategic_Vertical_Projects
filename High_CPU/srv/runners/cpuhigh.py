import sys
import salt.client
import urllib2
import subprocess
import pycurl
import cgitb
import cgi
import StringIO
import json
import re
from jnpr.junos import Device
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib

def infoCollect(event_data):

  # Fetch the arguments passed from the event sent
  events = event_data["data"]
  filePath = events["path"]

  with open (filePath, "r") as myfile:
    data=myfile.readlines()
    body="".join(data)

  dev = Device(host='192.168.20.1', user='root', password='salt123')
  dev.open()
  target = open("/var/log/juniper_rtsockmon.txt", 'w')
  from jnpr.junos.utils.start_shell import StartShell
  with StartShell(dev, timeout=30) as ss:
    target.write(ss.run("rtsockmon -t")[1])
  target.close()
  dev.close()
  
  # Send out an email to the user with the test details during failure
  # Email configurations
  msg = MIMEMultipart()
  msg['Subject'] = "CPU HIGH"
  msg['From'] = 'jedijsnapy@gmail.com'
  emaillist = "ssendhil@juniper.net,nvarshney@juniper.net"
  msg['To'] = "ssendhil@juniper.net,nvarshney@juniper.net"

  part = MIMEText(body)
  msg.attach(part)
 
  filename = "/var/log/juniper_rtsockmon.txt"
  f = file(filename)
  part = MIMEText(f.read())
  part.add_header('Content-Disposition', 'attachment', filename=filename)
  msg.attach(part)

  server = smtplib.SMTP("smtp.gmail.com")
  server.ehlo()
  server.starttls()
  server.login("jedijsnapy@gmail.com", "Juniper9")
  server.sendmail(msg['From'], emaillist, msg.as_string())
  server.close()
