import copy
import streamlit as st
import time

class cardSuitRecord():

    def __init__(self,cards=0,magicN1=1,magicN2=1,record='',op="q"):
        self.card = cards
        self.record = record
        self.magicN1 = magicN1
        self.magicN2 = magicN2
        self.op = op

    @staticmethod
    def __recordOper__(a, b, opper):
        left = a.record
        right = b.record

        if opper in "*/" and a.op in "+-":
            left = '('  + a.record + ')'
        if (opper in "/" and b.op in "+-*/") or (opper in "-*" and b.op in "+-"):
            right = '(' + b.record + ')'
        if opper == '/':
            opper = '÷'
        return left + " " + opper + " " + right

    def __str__(self):
        return self.record

    def __float__(self):
        return float(self.card)

    def __abs__(self):
        return abs(self.card)

    def __add__(self, other):
        op = "+"
        card = self.card + other.card
        record = self.__recordOper__(self,other,'+')
        magicN1 = self.magicN1 + other.magicN1
        magicN2 = self.magicN2 + other.magicN2
        return cardSuitRecord(card, magicN1, magicN2, record, op)

    def __sub__(self, other):
        op = "-"
        if self.card > other.card:
            card = self.card - other.card
            record = self.__recordOper__(self,other,'-')
            magicN1 = self.magicN1 - other.magicN1
            magicN2 = self.magicN2 - other.magicN2
        else:
            card = other.card - self.card
            record = self.__recordOper__(other,self,'-')
            magicN1 = other.magicN1 - self.magicN1
            magicN2 = other.magicN2 - self.magicN2

        return cardSuitRecord(card, magicN1, magicN2, record, op)

    def __mul__(self, other):
        op = "*"
        card = self.card * other.card
        record = self.__recordOper__(self,other,'*')
        magicN1 = self.magicN1 * other.magicN1
        magicN2 = self.magicN2 * other.magicN2

        return cardSuitRecord(card, magicN1, magicN2, record, op)

    def __truediv__(self, other):
        op = "/"
        card = self.card / other.card
        record = self.__recordOper__(self,other,'/')
        magicN1 = self.magicN1 / other.magicN1
        magicN2 = self.magicN2 / other.magicN2
        return cardSuitRecord(card, magicN1, magicN2, record, op)
    
    def __lt__(self,other):
        if self.card < other.card:
            return True
        else:
            return False

    def __eq__(self,other):
        if self.card == other.card and self.record == other.record:
            return True
        else:
            return False

def operations(a,b,oper):
    if oper=='+':
        return a+b
    if oper=='-':
        return a-b
    if oper=='*':
        return a*b
    if oper=='/':
        return a/b
    if oper=='%':
        return b/a

def cal(cardSR, answer,solutions,hashSolutions1,hashSolutions2,gameMode, mybar,T1):
    '''本函数是一个递归设计。每次从序列中取出2个，然后进行加减乘除的计算，再把计算结果，与原来序列的剩余组合成下一轮
        迭代的输入。这样每次会减少一个数字，直至胜一个时，判断他是不是目标答案（例如24）即可。
        为了可以记录计算的过程，每次在取两个数出来生成第三个数的时候，计算过程用字符串形式记录下来。'''
    '''例如，起始数列是[1,2,3,4]，则同时定义对应的字符['1','2','3','4']
       计算1，2的积的时候，取出1，2， 剩余序列为[3,4].  然后计算得2=1*2，同时记录对应的计算过程'1*2'. 
       那么,下一轮的数字序列为[3,4,2]，下一轮的字符序列为['3','4','1*2']. 
       如此往复尝试，直至数字序列变为[24], 字符序列变为['1*2*3*4']为止。
    '''
    number = len(cardSR)
    #只剩下一个数的时候，判断计算结果。
    #如果计算结果不是24，或者结果是24，但是魔术字已经重复，则不添加。
    
    if number == 1 and abs(float(cardSR[0])-answer) < 0.00001:
        find_flag = False
        for i in range(len(hashSolutions1)):
            if abs(cardSR[0].magicN1 - hashSolutions1[i])/cardSR[0].magicN1 < 0.0001:
                mybar.progress(text=f'找到 :green[{len(solutions)}]  个答案, 耗时  :orange[{(time.time_ns()-T1)/1000000:,.0f}]  毫秒', value=len(solutions)/(len(solutions)+10))
                return
        for i in range(len(hashSolutions2)):
            if abs(cardSR[0].magicN2 - hashSolutions2[i])/cardSR[0].magicN2 < 0.0001:
                mybar.progress(text=f'找到 :green[{len(solutions)}]  个答案, 耗时  :orange[{(time.time_ns()-T1)/1000000:,.0f}]  毫秒', value=len(solutions)/(len(solutions)+10))
                return
        #findslt = str(cardSR[0])
        #if findslt in solutions: #重复的不要
        #    return
        
        solutions.append(str(cardSR[0]))                               #写入solutions
        hashSolutions1.append(cardSR[0].magicN1)               #写入魔术字
        hashSolutions2.append(cardSR[0].magicN2)               #写入魔术字

        st.markdown(f':orange[【{len(solutions)}】  ] :blue[{cardSR[0]}]')
        st.toast(cardSR[0])
        mybar.progress(text=f'找到 :green[{len(solutions)}]  个结果, 耗时  :orange[{(time.time_ns()-T1)/1000000:,.0f}]  毫秒', value=len(solutions)/(len(solutions)+10))
        return

    for i in range(0,number-1):
        for j in range (i+1,number):
            childSR = copy.deepcopy(cardSR)               #制作拷贝，每选择出2个数会制作一个新拷贝
            [A, B] = [childSR.pop(j), childSR.pop(i)]     #先pop后面的，再pop前面的，这样不需要考虑pop了前面引起后面数字位置的变化
            for k in ['*','+','/','%','-']:
                copychildSR  = copy.deepcopy(childSR)      #制作剩余数列拷贝（已经取出两个值），每个操作再制造一个新拷贝
                if ((abs(A) < 0.00001 or abs(A)==1) and k=='%') or ((abs(B)==1 or abs(B) < 0.00001) and k=='/'):    #0不能做除数; 因为1肯定会作为乘法，所以省略除法
                    continue
                copychildSR.append(operations(A,B,k))     #AB做运算后的结果和刚才剩余的项组成下一轮的输入
                cal(copychildSR, answer, solutions, hashSolutions1, hashSolutions2, gameMode, mybar,T1) #下一轮
                if gameMode != 0 and len(solutions)>=gameMode: # 算够了就返回
                    return