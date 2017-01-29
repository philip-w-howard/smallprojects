#!/usr/bin/python
import socket
import json
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

MAX_PEOPLE = 10

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet UDP
sock.bind((UDP_IP, UDP_PORT))

def read_file() :
    file = open("helpsessions.data", "r")
    contents = file.readlines()

    sessions = {}
    people = []
    session_name = ""
    for line in contents :
        line = line.strip()
        if len(line) < 1:
            continue

        if line[0] == "#" :
            if len(session_name) > 1 :
                sessions[session_name] = people
            session_name = line[1:]
            people = []
        else :
            people.append(line)
            people.sort()

    if len(session_name) > 1 :
        sessions[session_name] = people

    return sessions

def write_file(sessions) :
    file = open("helpsessions.data", "w")

    for session in sessions.keys() :
        file.write("#" + session + "\n")
        for person in sessions[session] :
            file.write(person + "\n")

    file.close()

def send_response(response, destination) :
    sock.sendto(response, destination)

def proc_request(cmd, requester) :

    params = cmd.split()
    if len(params) < 1 :
        send_response("Empty command", requester)
        return
    elif params[0] == "list" :
        sessions = read_file()
        response = json.dumps(sessions)
        send_response(response, requester)
        return
    elif params[0] == "add" and len(params) > 2 :
        sessions = read_file()
        if params[1] in sessions :
            people = sessions[params[1]]
            if len(people) >= MAX_PEOPLE :
                print "session full"
                send_response("Session full", requester)
            elif params[2] not in people :
                sessions[params[1]].append(params[2])
                sessions[params[1]].sort()
                print "added", params[2], "to", params[1]
                write_file(sessions)
                send_response("Success", requester)
            else :
                print params[2], "already in", params[1]
                send_response("Success", requester)
        else :
            send_response("Invalid session", requester)

    elif params[0] == "drop" :
        sessions = read_file()
        if params[1] in sessions :
            people = sessions[params[1]]
            if params[2] in people :
                sessions[params[1]].remove(params[2])
                print "removed", params[2], "to", params[1]
                write_file(sessions)
            else :
                print params[2], "not in", params[1]

            send_response("Success", requester)

        else :
            send_response("Invalid session", requester)

    else :
        send_response("Unknown command", requester)
        return

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    proc_request(data, addr)
    sys.stdout.flush()
