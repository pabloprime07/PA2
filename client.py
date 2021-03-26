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
def maintain_servers():
    host = "" 
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    s.listen(5)
    c, addr = s.accept()
    while True: 
        data = c.recv(1024) 
        if not data:  
            break
        print(data)
        data = str(nth_prime_number(int(data)))        
        print(data)
        c.send(data.encode()) 
    c.close() 
 

def Main(): 
    # local host IP '127.0.0.1' 
    servers = list()
    host = '127.0.0.1'
  
    # Define the port on which you want to connect 
    
  
    start_new_thread()
    while True: 
        if len(servers) == 0:
            sleep(3)
            continue
        host = servers[random.randint(0,len(servers)-1]
        port = 12345
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.connect((host,port)) 
        
        message = str(random.randint(pow(10,args.load-1), pow(10,args.load)))
        # message sent to server 
        s.send(message.encode('ascii')) 
  
        # messaga received from server 
        data = s.recv(1024) 
  
        # print the received message 
        # here it would be a reverse of sent message 
        print('Received from the server :',str(data.decode('ascii'))) 
  
        # ask the client whether he wants to continue 
        time.sleep(0.5)
    # close the connection 
    s.close() 
  
if __name__ == '__main__': 
    Main() 