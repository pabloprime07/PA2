import libvirt
import argparse
import time
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
    doms = conn.listAllDomains()
    prevtimes = [ 0 for x in doms]
    usagetimes = [ [] for x in doms]
    n = 10
    for ii in range(n):
        
        for i in range(len(doms)):
            cputime = doms[i].getCPUStats(True)[0]["cpu_time"]-doms[i].getCPUStats(True)[0]["system_time"]-doms[i].getCPUStats(True)[0]["user_time"]
            cputime = doms[i].getCPUStats(True)[0]["cpu_time"]
            
            cpuutil = (cputime-prevtimes[i])/(2E9)
            usagetimes[i].append(cpuutil)
            prevtimes[i] = cputime
        time.sleep(0.5)

    for i in range(len(doms)):
        avgusage = sum(usagetimes[i])/n
        print(f'Usage for {doms[i].name()} :: {avgusage}')
        print()
    # if avgusage > highloadthreshold:
    #     highloadcount = highloadcount + 1
    # else :
        # highloadcount = 0
    
    # if highloadcount == maxhighloadretry :
    #     print(f'High Load from {dom.name()} for the last {maxhighloadretry} times')
    #     # Thread(target=startNewVM).start()
    #     for x in conn.listAllDomains():
    #         if x.isActive() == False:
    #             x.create()        
    #             host = "127.0.0.1"
    #             port = 23456
    #             s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    #             s.connect((host,port)) 
    #             message = domips[x.name()]
    #             s.send(message.encode('ascii')) 
    #             data = s.recv(1024) 
    #             print('Received from the client :',str(data.decode('ascii'))) 
    #             s.close()
    #             break
    time.sleep(1)

conn.close()