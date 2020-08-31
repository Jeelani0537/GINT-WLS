import subprocess
import sys

fmw_version = sys.argv[1]
domain_names = sys.argv[2]
properties = {}

for domain in domain_names.split(','):
  hostname_command = "cat /opt/oracle/domains" + fmw_version + "/" + domain + "/servers/AdminServer/data/nodemanager/AdminServer.url | awk -F':' '{print $2}' | awk -F'/' '{print $3'}"
  port_command = "cat /opt/oracle/domains" + fmw_version + "/" + domain + "/servers/AdminServer/data/nodemanager/AdminServer.url | awk -F':' '{print $3}'"
  properties[domain] = {}
  proc = subprocess.Popen([hostname_command], stdout=subprocess.PIPE, shell=True)
  (hostout, err) = proc.communicate()
  properties[domain]['host'] = hostout.replace('\n','')
  proc = subprocess.Popen([port_command], stdout=subprocess.PIPE, shell=True)
  (portout, err) = proc.communicate()
  properties[domain]['port'] = portout.replace('\n','')

print properties
