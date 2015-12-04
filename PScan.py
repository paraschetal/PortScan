import optparse

from socket import *
def connScan(tgtHost,tgtPort):
	try:
		connSkt=socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost,tgtPort))
		connSkt.send('PythonPortScan\r\n')
		results=connSkt.recv(100)
		print '[+]%d/tcp open'% tgtPort
		print '[+] '+str(results)
		connSkt.close()
	except:
		print '[-]%d/tcp closed'% tgtPort

def portScan(tgtHost,tgtPorts):
	try:
		tgtIP=gethostbyname(tgtHost)
	except:
		print "[-] Cannot resolve '%s' : Unknown host"%tgtHost
		return
	try:
		tgtName=gethostbyaddr(tgtIP)
		print '\n[+] Scan results for: '+tgtName[0]
	except:
		print 'Scan Results for: '+ tgtIP
	setdefaulttimeout(1)
	for tgtPort in tgtPorts:
		print 'Scanning port '+tgtPort
		connScan(tgtHost, int(tgtPort))	

def main():		
	parser=optparse.OptionParser('usage %prog -H ' + '<target host> -p <target ports>') #Our program utilizes the optparse library to parse command line arguments
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
	parser.add_option('-p',dest='tgtPort',type='string',help='specify target port[s] inside \"\" separated by commas')
	(options,args)=parser.parse_args()
	tgtHost=options.tgtHost
	print options.tgtPort
	tgtPorts=str(options.tgtPort).split(", ")
	if(tgtHost==None) | (tgtPorts[0]==None):
		print "[-] You must specify a target host and port[s](within \"\")."
		exit(0)
	portScan(tgtHost,tgtPorts)	
if __name__=="__main__":
	main()
