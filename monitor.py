import libvirt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('load', type=int, help='indicator for load on the servers')
args = parser.parse_args()
# print(args.load)
# print(type(args.load))
def getCPUtime(dom):
    return dom.getCPUStats(True)[0]["cpu_time"]


conn = libvirt.open('qemu:///system')

print(conn.getHostname())
# print(conn.getMaxVcpus())
# print(conn.getSysinfo())

print(conn.listAllDomains())
print(conn.listDomainsID())

# dom = conn.lookupByID(1)
# if dom == None:
#     print('Failed to find the domain '+domName, file=sys.stderr)
#     exit(1)

# cpu_stats = dom.getCPUStats(False)
# # print(dom.hostname())
# for (i, cpu) in enumerate(cpu_stats):
#    print('CPU '+str(i)+' Time: '+str(cpu['cpu_time'] / 1000000000.))


conn.close()