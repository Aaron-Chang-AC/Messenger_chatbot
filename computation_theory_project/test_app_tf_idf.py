# coding=utf-8
import json,urllib,math,time,socket,os,logging,jieba;
SaveDirectory = os.getcwd()
F='file:'
F=F+SaveDirectory+'/computation_theory_project/CTBC.json'
print(F)
R= urllib.urlopen(F);
S = R.read();
O = json.loads(S.decode("utf-8"));
I = input()
SEG = jieba.cut(I,cut_all=False); #CKIP_input

Q=[];
for u in SEG:
	Q.append(u)

#preprocessing_2
STR=[];
for A in range(0,len(O)):
	if O[A]['question']!='':
		CKIP_OF_Oi=jieba.cut(O[A]['question'],cut_all=False) #tokenize questions
		STR.append([])
                Y=[]
                for u in CKIP_OF_Oi:
                        Y.append([])
		for B in range(0,len(Q)):
			STR[A].append([])
			STR[A][B]=Q[B]
	else:
		STR.append([])




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
		print(O[i]['answer'])
	else:
		i=i+1
#L
IT = 0
while IT == 0:
        I = input()
        SEG = jieba.cut(I,cut_all=False); #CKIP_input
        Q=[];
        for u in SEG:
                Q.append(u)
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
                	print(O[i]['answer'])
                else:
                        i=i+1
