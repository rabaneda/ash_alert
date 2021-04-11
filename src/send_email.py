#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 00:16:42 2021

@author: albertosr
"""

import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Send_email:
    
    #CHANGE THIS CLASS OBJECTS FOR DIFFERENT SERVERS OR EMAIL ADDRESSES
    #NO NEED TO CHANGE DIRECTLY HERE, AFTER CLASS INSTANCE IS CALLED, THEY CAN
    #BE MODIFIED; e.g.:
    # foo = Send_email()
    # foo.server = 'something else'
    
    server = "smtp.gmail.com"
    sender= "*****@gmail.com"
    receivers = ['*****@met.no', '*****@met.no', '*******@met.no']
    
    def __init__(self, file):
        
        self.file = file

    
    def send_email(self, port = 587):
        
    
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "ASH POLLUTION ALERT Alberto Rabaneda"
        message["From"] = Send_email.sender_email
        receivers = ''.join([''.join([x, ',']) for x in Send_email.receiver_email])
        message["To"] = receivers
        body = """\
        Hi,
        
        This is an automatic email send by Alberto S. Rabaneda.
        This email is part of an exercise within the selection process for a 
        job position at met Norway as Scientific Programmer.
        
        If you received this email, ash pollution from an Icelandic volcano has been
        forecasted to reach the Norwegian shore.
        Please, find attached a zip file with csv files and maps with pollution data.
        
        All the best,
        
        Alberto S. Rabaneda
        
        P.D.: The scripts to produce this email, attachments and for triggering the
        tool after the forecasting model has finshed calculations, will be available
        at my Github on a private repository. If you want to access the repository, 
        please send me your Github username.
        """
    
        message.attach(MIMEText(body, "plain"))
        
        filename = self.file
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
      
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
      
        # Add header as key/value pair to attachment part
        part.add_header("Content-Disposition", f"attachment; filename= {filename}")
      
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
    
        context = ssl.create_default_context()
        password = input("Type your password and press enter: ")
        with smtplib.SMTP(Send_email.smtp_server, port) as server:
            server.starttls(context = context)
            server.login(Send_email.sender_email, password)
            server.sendmail(Send_email.sender_email, Send_email.receiver_email, text)

