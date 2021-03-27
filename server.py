import socket 
  
from _thread import *
import threading 
  
def nth_prime_number(n):
    
    prime_list = [2]
    num = 3
    
    while len(prime_list) < n:  
        for p in prime_list:    
            if num % p == 0:
                break
        else:
            prime_list.append(num)
        num += 2

    return prime_list[-1]

# thread function 
def threaded(c): 
    while True: 
        data = c.recv(1024) 
        if not data: 
            print('Bye') 
            break
  
        print(data)
        data = str(nth_prime_number(int(data))) 
        print(data)
        c.send(data.encode()) 

    c.close() 
  
  
def Main(): 
    host = "" 
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to port", port) 
  
    s.listen(5) 
    print("socket is listening") 
  
    while True: 
  
        c, addr = s.accept() 
  
        print('Connected to :', addr[0], ':', addr[1]) 
 
        start_new_thread(threaded, (c,)) 
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 