import streamlit as st
import pandas as pd
import numpy as np
import TwentyFourMagic as TF
import time

#default game rules
MaxCardNum = 10; DefCard = 4; CardMin = 1; DefMin  = 1; CardMax = 20; DefMax  = 13; DefTargetNum = 24

if 'calculating' not in st.session_state:
   st.session_state['calculating'] = False

def calculating(state:bool=True):
    st.session_state['calculating'] = state
    
st.markdown('# :blue[计算24点]')

with st.sidebar:
    st.markdown('## :orange[选择规则]')
    with st.form('rules'):
        card_num = st.slider('选择牌张数', 1, MaxCardNum, DefCard,key='card_num')
        card_range = st.slider('选择牌点范围', CardMin, CardMax, (DefMin, DefMax), key = 'card_min')
        TargetNum = st.number_input('选择计算目标值 例如24', None, None, DefTargetNum, key ='target')
        with st.container():
            gameMode = st.number_input('取多少个答案', 0, 10000, 0, key = 'gameMode')
            st.markdown(':orange[注：取0时搜索所有答案]')
        submitted_rules = st.form_submit_button("确认规则 | 重置随机牌点", disabled=st.session_state['calculating'])

    with st.container():
        if 'initcard' not in st.session_state:
            st.session_state['initcard'] = np.random.randint(card_range[0], card_range[1]+1, size=MaxCardNum)
        if submitted_rules:
            st.session_state['initcard'] = np.random.randint(card_range[0], card_range[1]+1, size=MaxCardNum)
    
    st.markdown('## :orange[选择牌点]')
    with st.form('numbers'):
        cardset = [0]*card_num
        for i in range(card_num):
            cardset[i] = st.number_input(label=f'.', min_value=card_range[0], max_value=card_range[1], value=st.session_state['initcard'][i],key=str(f'cardset{i}'))

        submitted_cal = st.form_submit_button("开始计算", on_click=calculating)
        
if submitted_cal:
    with st.form('cal'):
        st.form_submit_button('重新开始', on_click=calculating(False))
        
        st.markdown(f'### :orange[:blue[{card_num}] 张牌     :blue[{cardset}] 计算 :blue[{TargetNum}] 点]')

        numcardsuit = list(map(int,cardset));    numcardsuit.sort(reverse=True)
        
        magicN1 = np.random.randint(4342,95956394,size=card_num)
        magicN2 = np.random.randint(4342,95956394,size=card_num)

        cardSR_A = []
        for i in range(card_num):
            magicN1[i] = magicN1[numcardsuit.index(numcardsuit[i])]                                   #如果牌有重复，魔术字跟着做同样的重复
            magicN2[i] = magicN1[numcardsuit.index(numcardsuit[i])]                                   #如果牌有重复，魔术字跟着做同样的重复
            if numcardsuit[i] == 1: magicN1[i] = 1; magicN2[i] = 1
            cardSR_A.append(TF.cardSuitRecord(numcardsuit[i],magicN1[i],magicN2[i],str(numcardsuit[i])))        #构建组合“牌组数字” + “牌组字符”
        
        solutions = []
        hashSolutions1 = []
        hashSolutions2 = []

        
        my_bar = st.progress(0)
        with st.container():
            with st.spinner('正在搜索答案'):
                T1 = time.time_ns()
                TF.cal(cardSR_A, TargetNum,solutions,hashSolutions1,hashSolutions2,st.session_state['gameMode'],my_bar,T1)
                T2 = time.time_ns()
                T2_1 = (T2-T1)/1000000
                for i in range(1,11):
                    my_bar.progress(text=f'找到 :green[ {len(solutions)} ]  个答案, 耗时  :orange[ {T2_1:,.0f} ]  毫秒', value=(len(solutions)+i)/(len(solutions)+10) if (len(solutions) != 0) else 1.0 )
                    time.sleep(0.05)
                    
            st.success(f'计算结束, 耗时 {T2_1:,.0f} 毫秒', icon='✅')
            st.session_state['calculating'] = False
