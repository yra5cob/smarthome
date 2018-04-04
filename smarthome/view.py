from django.http.response import HttpResponse
import socket
import sys
from _thread import *

from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

smartobjects={}

HOST = '192.168.43.79'  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    sys.exit()

print('Socket bind complete')
print('Socket now listening')
def startListening():
    s.listen(10)
    while 1:
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        data=""
        state=""
        data = conn.recv(1024).decode()
        if len(data.split("/n"))==3:
            (data, state) = data.split("\n", 1)
        else:
            state = conn.recv(1024).decode()
        # state = conn.recv(1024).decode().rstrip('\n')
        content={}
        content['conn']=conn
        content['state']=state.strip()
        smartobjects[data.strip()]=content
        print("here")
    s.close()
start_new_thread(startListening, ())

@csrf_exempt
def index(request):
    if 'action' in request.POST:
        conn=smartobjects[request.POST.get('port')]['conn']
        conn.send(request.POST.get('msg').encode())
        if request.POST.get('msg')=='OFF':
            smartobjects[request.POST.get('port')]['state']='ON'
        else:
            smartobjects[request.POST.get('port')]['state'] = 'OFF'
        conn.send(".".encode())
        print("send")
        return HttpResponse("")
    body=""
    for key, value in smartobjects.items():

        body+='<div><label>'+key+'  </label><button id="'+key+'" onclick="send(this)">'+value["state"]+'</button><div>'

    return HttpResponse(render_to_string('base.html',{'body':body}))