import sys

invfile = sys.argv[1]

combinations = {}

with open(invfile) as fp:
  lines = fp.readlines()
  for line in lines:
    domain,host,servers,version = line.replace('\n','').split(':')
    if 'soa' in servers.lower():
      stack = 'soa'
    elif 'osb' in servers.lower():
      stack = 'osb'
    elif 'gtw' in servers.lower():
      stack = 'gtw'
    elif 'odi' in servers.lower():
      stack = 'odi'
    #print servers

    if stack not in ['odi', 'bam']:
      if not domain in combinations.keys():
        combinations[domain] = {}
        combinations[domain]['hosts'] = host
        combinations[domain]['stack'] = stack      
        #combinations[domain]['run'] = host
        combinations[domain]['version'] = version
      else:
        existingValue = combinations[domain]['hosts']
        combinations[domain]['hosts'] = existingValue + "," + host

print combinations
#for combo in combinations:
#  print combo, combinations[combo]

#for domain in combinations:
#  print domain, combinations[domain]
