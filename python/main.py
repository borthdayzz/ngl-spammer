_A=False
import random,requests,time,threading,signal,sys
DISCORD_WEBHOOK_URL='put discord webhook here'
running=True
def read_lines_from_file(filename):
	with open(filename,'r')as A:return[A.strip()for A in A.readlines()]
userAgentOptions=read_lines_from_file('user_agents.txt')
messages=read_lines_from_file('messages.txt')
uuids=read_lines_from_file('list_uuids.txt')
if len(uuids)==0:print('❌ Error: No UUIDs found in list_uuids.txt file.');exit(1)
def generate_user_agent():return random.choice(userAgentOptions)
def send_message(username,user_question,count):
	C=count;B=user_question;A=username;global running;D=random.choice(uuids).strip();E=generate_user_agent();F={'X-Requested-With':'XMLHttpRequest','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','User-Agent':E};G={'username':A,'question':B,'deviceId':D,'gameSlug':'','referrer':''}
	while running:
		try:
			H=requests.post('https://ngl.link/api/submit',headers=F,data=G,timeout=10)
			if H.status_code==200:
				print(f"Message sent successfully to {A} ({C}) with device ID: {D}")
				if C==1:notify_discord(A,B)
				break
			else:print(f"Failed to send message to {A}");time.sleep(10)
		except Exception as I:print(f"Failed to send message to {A}: {str(I)}");time.sleep(10)
def notify_discord(username,message):A={'content':f"Spamming message to {username}: {message}"};requests.post(DISCORD_WEBHOOK_URL,json=A)
def check_ngl_link(url):
	try:
		A=requests.head(url,timeout=10)
		if A.status_code==200:print('The ngl.link page exists.')
		elif A.status_code==404:print('The ngl.link page was deleted.')
		else:print('The ngl.link page returned an error.')
	except requests.RequestException as B:print('An error occurred while checking the ngl.link page:',B)
def shutdown_signal_handler(signal,frame):global running;print('Received shutdown signal. Shutting down gracefully...');running=_A
signal.signal(signal.SIGINT,shutdown_signal_handler)
def main():
	G='Input how many you want to send: ';F='Input username: ';global running
	while running:
		print('starhook ngl spammer');print('Choose an option:');print('1 - Constant bomb');print('2 - Custom message');print('3 - Check ngl.link page')
		try:A=input('Enter the option number: ')
		except EOFError:print('\nReceived shutdown signal. Shutting down gracefully...');running=_A;break
		if A=='1':
			B=input(F);C=int(input(G))
			for D in range(C):E=random.choice(messages);threading.Thread(target=send_message,args=(B,E,D+1)).start();time.sleep(2.5)
		elif A=='2':
			B=input(F);E=input('Input message: ');C=int(input(G))
			for D in range(C):threading.Thread(target=send_message,args=(B,E,D+1)).start();time.sleep(2.5)
		elif A=='3':
			while running:H=input('Enter the path component of the ngl.link (e.g., /barfing): ');I=f"https://ngl.link/{H}";check_ngl_link(I);break
		J=input('Do you want to continue? (yes or no): ')
		if J.lower()!='yes':running=_A
	print('Exiting program...')
main()