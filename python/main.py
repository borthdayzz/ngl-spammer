N=range
H=False
C=input
A=print
import ctypes as K,random as F,requests as D,time as E,threading as L,signal as I,sys,config as O
K.windll.kernel32.SetConsoleTitleW('starhook.solutions')
B=True
def G(filename):
	with open(filename,'r')as A:return[A.strip()for A in A.readlines()]
P=G('user_agents.txt')
Q=G('messages.txt')
J=G('uuids.txt')
if len(J)==0:A('❌ Error: No UUIDs found in uuids.txt file.');exit(1)
def R():return F.choice(P)
def M(username,user_question,count):
	H=count;G=user_question;C=username;global B;I=F.choice(J).strip();K=R();L={'X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':K};M={'username':C,'question':G,'deviceId':I,'gameSlug':'','referrer':''}
	while B:
		try:
			N=D.post('https://ngl.link/api/submit',headers=L,data=M,timeout=10)
			if N.status_code==200:
				A(f"Message sent successfully to {C} ({H}) with device ID: {I}")
				if H==1:S(C,G)
				break
			else:A(f"Failed to send message to {C}");E.sleep(10)
		except Exception as O:A(f"Failed to send message to {C}: {str(O)}");E.sleep(10)
def S(username,message):A={'content':f"Spamming message to {username}: {message}"};D.post(O.DISCORD_WEBHOOK_URL,json=A)
def T(url):
	try:
		B=D.head(url,timeout=10)
		if B.status_code==200:A('The ngl.link page exists.')
		elif B.status_code==404:A('The ngl.link page was deleted.')
		else:A('The ngl.link page returned an error.')
	except D.RequestException as C:A('An error occurred while checking the ngl.link page:',C)
def U(signal,frame):global B;A('Received shutdown signal. Shutting down gracefully...');B=H
I.signal(I.SIGINT,U)
def V():
	P='Input how many you want to send: ';O='Input username: ';global B
	while B:
		A('starhook ngl spammer');A('Choose an option:');A('1 - Constant bomb');A('2 - Custom message');A('3 - Check ngl.link page')
		try:D=C('Enter the option number: ')
		except EOFError:A('\nReceived shutdown signal. Shutting down gracefully...');B=H;break
		if D=='1':
			G=C(O);I=int(C(P))
			for J in N(I):K=F.choice(Q);L.Thread(target=M,args=(G,K,J+1)).start();E.sleep(2.5)
		elif D=='2':
			G=C(O);K=C('Input message: ');I=int(C(P))
			for J in N(I):L.Thread(target=M,args=(G,K,J+1)).start();E.sleep(2.5)
		elif D=='3':
			while B:R=C('Enter the path component of the ngl.link (e.g., /barfing): ');S=f"https://ngl.link/{R}";T(S);break
		U=C('Do you want to continue? (yes or no): ')
		if U.lower()!='yes':B=H
	A('Exiting program...')
if __name__=='__main__':V()
