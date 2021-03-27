import libvirt
import argparse
import time
import socket
# parser = argparse.ArgumentParser()
# parser.add_argument('load', type=int, help='indicator for load on the servers')
# args = parser.parse_args()
# print(args.load)
# print(type(args.load))


domips = {'ubuntu20.04':'192.168.122.100', 'ubuntu20.04-2':'192.168.122.230', 'ubuntu20.04-3':'192.168.122.144'}
conn = libvirt.open('qemu:///system')

print(conn.getHostname())
# print(conn.getMaxVcpus())
# print(conn.getSysinfo())

print(conn.listAllDomains())
print(conn.listDomainsID())
print(conn.listAllDomains())
print(conn.listDefinedDomains())
for x in conn.listAllDomains():
    print("shapeshifters ")
    print(x.UUIDString())
    print(x.name())
# dom = conn.lookupByID(1)
# if dom == None:
#     print('Failed to find the domain '+domName, file=sys.stderr)
#     exit(1)

# cpu_stats = dom.getCPUStats(False)
# # print(dom.hostname())
# for (i, cpu) in enumerate(cpu_stats):
#    print('CPU '+str(i)+' Time: '+str(cpu['cpu_time'] / 1000000000.))

while True:

    # timer = timer + 1
    alldoms = conn.listAllDomains()
    doms = list()
    for x in alldoms:
        if x.isActive() == True:
            doms.append(x)
    prevtimes = [ 0 for x in doms]
    usagetimes = [ [] for x in doms]
    n = 10
    for ii in range(n):
        if ii == 0:
            for i in range(len(doms)):
                cputime = doms[i].getCPUStats(True)[0]["cpu_time"]
                prevtimes[i] = cputime
            time.sleep(0.5)
            continue    
        for i in range(len(doms)):
            # cputime = doms[i].getCPUStats(True)[0]["cpu_time"]-doms[i].getCPUStats(True)[0]["system_time"]-doms[i].getCPUStats(True)[0]["user_time"]
            cputime = doms[i].getCPUStats(True)[0]["cpu_time"]
            
            cpuutil = 2*(cputime-prevtimes[i])/(1E7)
            # print(f'Usage for {doms[i].name()} :: {cpuutil}')
            # if prevtimes[i]==0:
            #     continue
            usagetimes[i].append(cpuutil)
            prevtimes[i] = cputime
        time.sleep(0.5)
    minusage = 1000
    for i in range(len(doms)):
        avgusage = sum(usagetimes[i])/n
        minusage = min(avgusage, minusage)
        print(f'Usage for {doms[i].name()} :: {avgusage}')
    print()
    # if avgusage > highloadthreshold:
    #     highloadcount = highloadcount + 1
    # else :
        # highloadcount = 0
    
    # if highloadcount == maxhighloadretry :
    #     print(f'High Load from {dom.name()} for the last {maxhighloadretry} times')
    #     # Thread(target=startNewVM).start()
    if minusage > 50:
        for x in conn.listAllDomains():
            if x.isActive() == False:
                print("Starting new server.....")
                x.create()
                time.sleep(30)        
                host = "127.0.0.1"
                port = 23456
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
                s.connect((host,port)) 
                message = domips[x.name()]
                s.send(message.encode('ascii')) 
                data = s.recv(1024) 
                print('Started new server at : ',str(data.decode('ascii'))) 
                s.close()
    time.sleep(1)

conn.close()