import optparse
from threading import *
from socket import *
screenLock =Semaphore(value=1) #to prevent multiple threads to print to the screen at once
def connScan(tgtHost,tgtPort):
	try:
		connSkt=socket(AF_INET, SOCK_STREAM)
		connSkt.connect((tgtHost,tgtPort)) #establishes a connection to target
		connSkt.send('PythonPortScan\r\n') #send a string of data to the open port and wait for the response
		results=connSkt.recv(100) #the response might give us an indication of the appliction running on the target host and port
		screenLock.acquire()
		print '[+]%d/tcp open'% tgtPort
		print '[+] '+str(results)
		
	except:
		screenLock.acquire()
		print '[-]%d/tcp closed'% tgtPort
	
	finally:
		screenLock.release()
		connSkt.close()


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
		t=Thread(target=connScan, args=(tgtHost,int(tgtPort)))
		t.start()	

def main():		
	parser=optparse.OptionParser('usage %prog -H ' + '<target host> -p <target ports>') #parse command line arguments
	parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
	parser.add_option('-p',dest='tgtPort',type='string',help='specify target port[s] inside \"\" separated by commas')
	(options,args)=parser.parse_args()
	tgtHost=options.tgtHost
	tgtPorts=str(options.tgtPort).split(", ")
	if(tgtHost==None) | (tgtPorts[0]==None):
		print parser.usage
		exit(0)
	portScan(tgtHost,tgtPorts)	
if __name__=="__main__":
	main()
