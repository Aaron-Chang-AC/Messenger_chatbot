# coding=utf-8
import requests
import urllib
import json,math,time,socket,os,jieba,sys;
import logging
from bottle import debug, request, route, run

####load json file###############################
SaveDirectory = os.getcwd()
F='file:'
F=F+SaveDirectory+'/computation_theory_project/CTBC.json'
print("json path: ",F)
R= urllib.urlopen(F);
S = R.read();
O = json.loads(S.decode("utf-8"));
u=0
Q=[];
state=0;
flag=0;
flag2=0;
#preprocessing_1:
for A in range(0,len(O)):
	s=''
	for i in range(0,len(O[A]['question'])):
		s=s+O[A]['question'][i]
	O[A]['question']=s
#preprocessing_2:
STR=[];
for A in range(0,len(O)):
        if O[A]['question'] != '':
                CKIP_OF_Oi=jieba.cut(O[A]['question'],cut_all=False) #tokenize questions
                STR.append([])
                Q=[]
                for i in CKIP_OF_Oi:
                        Q.append(i)
                for B in range(0,len(Q)):
                        STR[A].append([])
                        STR[A][B]=Q[B]
        else:
                STR.append([])
####end of loading################################

GRAPH_URL = "https://graph.facebook.com/v2.6"
VERIFY_TOKEN = 'F64051164'
PAGE_TOKEN = 'EAAHK1xehjWoBAL5NFzViYZAxRVC7box45ZAHzAdICvDeDQgWrJm2uMbmOZBg6Kbr0LjGBheXnoG1ZCzwqp120pI9kKdWZA1mSkVji0tRtVOPONDM8VmX5hJWcpXZCjjtI3rnQkoqderob1lHDyxDLDwu04hUe7NZAKwH4hlLcLbZAYXDVIiNmmDy'

def send_to_messenger(ctx):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
    response = requests.post(url, json=ctx)

@route('/chat', method="GET")
def webhook_handler():
    if request.method.lower() == 'get':
        verify_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            url = "{0}/me/subscribed_apps?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
            response = requests.post(url)
            return hub_challenge

@route('/chat', method="POST")
def bot_endpoint():
    global state
    print("The state is: ",state)
    if state == 0:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        
        SEG = jieba.cut(message_text,cut_all=False)
        Q=[];
        for i in SEG:
            Q.append(i)
        #start
        r=[];
        for A in range(0,len(STR)):
                SUM=0.0
                for X in Q:
                        if X in STR[A]:
                                SUM=SUM+1
                if len(STR[A]) != 0:
                        SUM=SUM/len(STR[A])
                else:
                        SUM=0.0;
                r.append(SUM)

        #calculate qi
        qi=[];
        for A in range(0,len(Q)):
                qi.append(0)
        for A in range(0,len(STR)):
                for B in range(0,len(Q)):
                        if Q[B] in STR[A]:
                                qi[B]=qi[B]+1

        #IDF
        IDF=[];
        for B in range(0,len(Q)):
                SUM = (len(STR)-qi[B]+0.5)/(qi[B]+0.5)
                if SUM != 0:
                        SUM = math.log(SUM,10)
                IDF.append(SUM)

        #average document length
        ADL=0.0
        for A in range(0,len(STR)):
                ADL=ADL+len(STR[A])
        ADL=ADL/len(STR)

        #SCORE
        SCORE=[];			
        for A in range(0,len(STR)):
                SUM = 0.0
                J=[]
                fqi = 0.0
                for B in range(0,len(Q)):
                        fqi=0.0
                        for C in range(0,len(STR[A])):
                                if Q[B] == STR[A][C]:
                                        fqi=fqi+1
                        if len(STR[A]) != 0:
                                fqi=fqi/len(STR[A])
                        else:
                                fqi=0
                        fqi=fqi*(1.5+1)/(fqi+1.5*(1-0.75+0.75*len(STR[A])/ADL))
                        temp=fqi*IDF[B]
                        J.append(temp)
                SCORE.append(sum(J))
        #final
        i=0
        if message_text == "你是誰".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "我是中國信託聊天機器人",
                }
            }
            state=1; #change state to 1
            response = send_to_messenger(ctx)
            return ''
        if message_text=="你好".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "你好!!",
                }
            }
            state=2; #change state to 2
            response = send_to_messenger(ctx)
            return ''
        if message_text=="今天天氣很好".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "去散散步怎麼樣??",
                }
            }
            state=3; #change state to 3
            response = send_to_messenger(ctx)
            return ''
        if message_text=="今天空氣很糟糕".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "是的，所以你外出時可能需要口罩!",
                }
            }
            state=4; #change state to 4
            response = send_to_messenger(ctx)
            return ''
        for j in SCORE:
                if j == max(SCORE):
                	break
                else:
                        i=i+1
        # send the result
        if user_id != page_id:
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': O[i]['answer'],
                }
            }
            response = send_to_messenger(ctx)
        return ''
    elif state == 1:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        if message_text == "你是誰".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "我是中國信託聊天機器人",
                }
            }
            state=1; #change state to 1
            response = send_to_messenger(ctx)
            return ''
        elif message_text == "return":
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "請再次提出問題!",
                }
            }
            state=0;
            print("reset state to: ",state)
            response = send_to_messenger(ctx)
            return ''
    elif state ==2:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        if message_text=="你好".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "你好!!",
                }
            }
            state=2;
            response = send_to_messenger(ctx)
            return ''
        elif message_text == "return":
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "請再次提出問題!",
                }
            }
            state=0;
            response = send_to_messenger(ctx)
            return ''
    elif state ==3:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        if message_text=="今天天氣很好".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "去散散步怎麼樣??",
                }
            }
            state=3;
            response = send_to_messenger(ctx)
            return ''
        elif message_text == "return":
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "請再次提出問題!",
                }
            }
            state=0;
            response = send_to_messenger(ctx)
            return ''
    elif state ==4:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        if message_text == "你會建議使用哪種口罩".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "https://my-best.tw/13800/",
                }
            }
            state=5;
            response = send_to_messenger(ctx)
            return ''
        elif message_text == "return":
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "請再次提出問題!",
                }
            }
            state=0;
            response = send_to_messenger(ctx)
            return ''
    elif state==5:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        if message_text=="謝謝".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "還有什麼需求嗎?",
                }
            }
            state=6;
            response = send_to_messenger(ctx)
            return ''
        elif message_text == "return":
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "請再次提出問題!",
                }
            }
            state=0;
            response = send_to_messenger(ctx)
            return ''
    elif state==6:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        if message_text=="沒有".decode('utf-8'):
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "別客氣!!",
                }
            }
            state=0;
            response = send_to_messenger(ctx)
            return ''
        elif message_text == "return":
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': "請再次提出問題!",
                }
            }
            state=0;
            response = send_to_messenger(ctx)
            return ''

run(host="localhost", port=8088,debug=True)
