import libvirt
import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument('load', type=int, help='indicator for load on the servers')
args = parser.parse_args()
# print(args.load)
# print(type(args.load))
def getCPUtime(dom):
    return dom.getCPUStats(True)[0]["cpu_time"]

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
    
    for x in conn.listDomainsID():
        dom = conn.lookupByID(x)
        if dom == None:
            print('Failed to find the domain '+x, file=sys.stderr)
            exit(1)        
        timer = 0
        usagelist = list()
        
        prevcputime = 0
        maxhighloadretry = 1

        highloadthreshold = 0.9
        highloadcount = 0
        while True:
            timer = timer + 1
            if timer >= 1E7:
                break
            currcputime = getCPUtime(dom)
            cpuusage = (currcputime - prevcputime)/(1E7)
            usagelist.append(cpuusage)
            prevcputime = currcputime
        avgusage = sum(usagelist)/maxhighloadretry
        print(avgusage)
        # if avgusage > highloadthreshold:
        #     highloadcount = highloadcount + 1
        # else :
            # highloadcount = 0
        
        if highloadcount == maxhighloadretry :
            print(f'High Load from {dom.name()} for the last {maxhighloadretry} times')
            # Thread(target=startNewVM).start()
            for x in conn.listAllDomains():
                if x.isActive() == False:
                    x.create()        
                    host = "127.0.0.1"
                    port = 23456
                    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
                    s.connect((host,port)) 
                    message = domips[x.name()]
                    s.send(message.encode('ascii')) 
                    data = s.recv(1024) 
                    print('Received from the client :',str(data.decode('ascii'))) 
                    s.close()
                    break
    time.sleep(1)

conn.close()