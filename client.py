# Import socket module 
import socket 
import random  
import time
import argparse
from _thread import *
import threading 

parser = argparse.ArgumentParser()
parser.add_argument('load', type=int, help='indicator for load on the servers')
args = parser.parse_args()
# print(args.load)
load = args.load
servers = list()
servers.append('192.168.122.100')
# thread function 
def threaded(c): 
    while True: 
        data = c.recv(1024) 
        if not data: 
            # print('Conn lost to monitor...') 
            break
        data = data.decode()
        print(f'Recieved from monitor : {data}')
        servers.append(data) 
        print(data)
        c.send(data.encode()) 

    c.close() 



def maintain_servers():
    host = "" 
    port = 23456
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    s.listen(5) 
    print("Socket is listening") 
  
    while True: 
  
        c, addr = s.accept() 
  
        # print('Connected to :', addr[0], ':', addr[1]) 
 
        start_new_thread(threaded, (c,)) 
    s.close() 
 
def loadinp():
    global load
    while True:
        x = input()
        load = int(x)
        print("New load = "+str(load))
        time.sleep(1)

def Main(): 
    # local host IP '127.0.0.1' 
    
    # host = '127.0.0.1'
  
    # Define the port on which you want to connect 
    
    th1 = threading.Thread(target=maintain_servers)
    th2 = threading.Thread(target=loadinp)
    th1.start()
    th2.start()
    # start_new_thread(maintain_servers, (None,))
    # start_new_thread(loadinp, (None,))
    while True: 
        if len(servers) == 0:
            time.sleep(5)
            print('sleeping...')
            continue
        host = servers[random.randint(0,len(servers)-1)]
        print(servers)
        print(host)
        port = 12345
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.connect((host,port)) 
        
        message = str(random.randint(pow(10, load-1), pow(10, load)))
        
        s.send(message.encode('ascii')) 
  
        data = s.recv(1024) 
        print(f'Cur Load : {load} ', end='')
        print(f'Received from the server : {host} ',str(data.decode('ascii'))) 
        s.close()
        time.sleep(0.5)
    
  
if __name__ == '__main__': 
    Main() 