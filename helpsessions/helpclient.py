#!/usr/bin/python
import socket
import json
import os
import pwd

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet UDP

user = pwd.getpwuid( os.getuid() ).pw_name
print "Running as", user

session_list = []

def display_menu() :
    global session_list

    print ""

    sock.sendto("list", (UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(4096)

    sessions = json.loads(data)
    id = 0
    session_list = []
    for session in sessions.keys() :
        session_list.append(session)
        id += 1
        print id, ":", session
        people = sessions[session]
        for person in people :
            print "    ", person
    print ""

def add(session) :
    session = int(session) - 1
    if len(session_list) > session and session >= 0 :
        sock.sendto("add " + session_list[session] + " " + user, (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(4096)

        print data
    else :
        print "Invalid session number"

def drop(session) :
    session = int(session) - 1
    if len(session_list) > session and session >= 0 :
        sock.sendto("drop " + session_list[session] + " " + user, (UDP_IP, UDP_PORT))
        data, addr = sock.recvfrom(4096)

        print data
    else :
        print "Invalid session number"

while (True) :
    display_menu()

    cmd = raw_input("add <session>, drop <session>, exit: ")
    print ""
    if len(cmd) > 0 :
        params = cmd.split()
        session_num = -1    
        if len(params) > 1 :
            try :
                session_num = int(params[1])
            except :
                print "Must enter an integer value"

        if params[0] == "exit" :
            break
        elif params[0] == "add" and len(params) > 1 :
            add(session_num)
        elif params[0] == "drop" and len(params) > 1 :
            drop(session_num)
        else :
            print "Unrecognized command"

print "thank you for useing the help session registration system"
