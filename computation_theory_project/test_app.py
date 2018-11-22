import json,sys
import requests
import json,urllib.request,math,time,socket,os,jieba;
import logging
from bottle import debug, request, route, run
##TF_IDF here###########################################
SaveDirectory = os.getcwd()
F='file:\\'
F=F+SaveDirectory+'\\computation_theory_project\\CTBC.json'
print(F)
R= urllib.request.urlopen(F);
S = R.read();
O = json.loads(S.decode());
u=0
Q=[];
#preprocessing_1
for A in range(0,len(O)):
	s=''
	for i in range(0,len(O[A]['question'])):
		if O[A]['question'][i]=='(':
			s=s+'【'
		elif O[A]['question'][i]==')':
			s=s+'】'
		else:
			s=s+O[A]['question'][i]
	O[A]['question']=s

#preprocessing_2
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

##TF_IDF_end############################################

GRAPH_URL = "https://graph.facebook.com/v2.6"
VERIFY_TOKEN = 'F64051164'
PAGE_TOKEN = 'EAAHK1xehjWoBAMH1TN1T9Sba5htlOjeljUu2YQadxJrbMO3DFQwlTJmWPrnyVwY950LgZBEro9xWjvlS1jpMk2eah6ZBeCQlEFmW3n1IWadZAqMhQNqFsiQpcL9ddmu6LGhzpTZCurPIfvd6k0Yf8hhQgTypH1dM8VSkZBRBNBRg0lpbHVL9y'

def send_to_messenger(ctx):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
    response = requests.post(url, json=ctx)

@route('/chat', method=["GET", "POST"])
def bot_endpoint():
    if request.method.lower() == 'get':
        verify_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            url = "{0}/me/subscribed_apps?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
            response = requests.post(url)
            return hub_challenge
    else:
        body = json.loads(request.body.read())
        user_id = body['entry'][0]['messaging'][0]['sender']['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['messaging'][0]['message']['text']
        # we just echo to show it works
        SEG = jieba.cut(message_text,cut_all=False)
        Q=[];
        for i in SEG:
            Q.append(i)
        #start
        r=[];
        for A in range(0,len(STR)):
                SUM=0
                for X in Q:
                        if X in STR[A]:
                                SUM=SUM+1
                if len(STR[A]) != 0:
                        SUM=SUM/len(STR[A])
                else:
                        SUM=0;
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
        ADL=0
        for A in range(0,len(STR)):
                ADL=ADL+len(STR[A])
        ADL=ADL/len(STR)

        #SCORE
        SCORE=[];			
        for A in range(0,len(STR)):
                SUM = 0
                J=[]
                fqi = 0
                for B in range(0,len(Q)):
                        fqi=0
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
        for j in SCORE:
                if j == max(SCORE):
                	#print(O[i]['answer'])
                	break
                else:
                        i=i+1
        # use your imagination afterwards
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


debug(True)
run(reloader=True, port=8088)
