import sys

data_file = sys.argv[1]
html_file = "/tmp/report.html"

f = open(data_file, "r")
lines = f.readlines()

old_stdout = sys.stdout
sys.stdout = open(html_file, 'w')
print "<html><head><title>SITI TOOLS STATUS</title></head><body><table border=1><tr><th>URL</th><th>STATUS</th></tr>"

for line in lines:
  #print line
  url, status_code = line.split(",")
  if "200" in status_code:
    status_color = "GREEN"
  elif "403" in status_code and ("jenkins" in url or "8080" in url):
    status_color = "GREEN"
  else:
    status_color = "RED"

  print "<tr><td>" + url + "</td><td bgcolor=" + status_color + ">" + status_code + "</td></tr>"

print "</table></body></html>"
sys.stdout = old_stdout

