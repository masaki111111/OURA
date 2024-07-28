import plotly.graph_objects as go
import requests
import streamlit as st
import numpy as np
import pandas as pd
import json
import oura
import datetime
import time
import plotly.graph_objects as go
import pytz
import math
import matplotlib.pyplot as plt

import datetime
import pytz

# 日本のタイムゾーンを設定
japan_tz = pytz.timezone('Asia/Tokyo')

# 現在の日本時間を取得
now = datetime.datetime.now(japan_tz)
dt_now = now.strftime('%Y-%m-%d')

# 昨日の日付を取得
yd = now - datetime.timedelta(days=1)
dt_yd = yd.strftime('%Y-%m-%d')

# 一昨日の日付を取得
dby = now - datetime.timedelta(days=2)
dt_dby = dby.strftime('%Y-%m-%d')

# 三日前の日付を取得
days_ago_3 = now - datetime.timedelta(days=3)
dt_days_ago_3 = days_ago_3.strftime('%Y-%m-%d')

# 結果を表示
print(f"今日の日付 (日本時間): {dt_now}")
print(f"昨日の日付 (日本時間): {dt_yd}")
print(f"一昨日の日付 (日本時間): {dt_dby}")
print(f"三日前の日付 (日本時間): {dt_days_ago_3}")

#期間を指定
start_text = dt_dby
end_text = dt_now

url = 'https://api.ouraring.com/v2/usercollection/daily_readiness' 
params={ 
    'start_date': start_text,#'2024-06-28', 
    'end_date': end_text #'2024-06-30'
}
headers = { 
  'Authorization': 'Bearer  XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS' 
}
response = requests.get(url, headers=headers, params=params) 
st.write(response.text)



a2 = response.json()
st.write(a2)#これでJsonデータが整列される


#1つの睡眠についてのドキュメント
import requests 
url = 'https://api.ouraring.com/v2/usercollection/daily_sleep'
params={ 
    'start_date': '2024-05-06', 
    'end_date': '2024-05-07'
}
headers = { 
  'Authorization': 'Bearer XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS' 
}
response = requests.request('GET', url, headers=headers, params=params) 
a1 =response.json()
st.write(a1)#これでJsonデータが整列される


#シングルスリープドキュメント
url = 'https://api.ouraring.com/v2/usercollection/sleep'
params = {
    'start_date': '2024-06-24',#start_text, #'2024-06-28', #start_text (全期間が欲しい場合)
    'end_date': '2024-06-26'#end_text #'2024-06-30' #end_text　(全期間が欲しい場合)
}
headers = { 
  'Authorization': 'Bearer XYJFZ6LI76CH3JX5VGUUCHT4JGWTEQRS' 
}
response = requests.get(url, headers=headers, params=params) 
#st.write(response)#jsonデータ取得
a0 = response.json()
st.write(a0)#これでJsonデータが整列される


date1 = (a0["data"][0]["bedtime_start"])
date2 = (a0["data"][0]["bedtime_end"])

date3 = (a0["data"][1]["bedtime_start"])
date4 = (a0["data"][1]["bedtime_end"])


""" date5 = (a0["data"][2]["bedtime_start"])
date6 = (a0["data"][2]["bedtime_end"]) """


date_start0 =pd.to_datetime(date1, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_start0 = date_start0.tz_localize(None)

date_end0 =pd.to_datetime(date2, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_end0 = date_end0.tz_localize(None)

date_start1 =pd.to_datetime(date3, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_start1 = date_start0.tz_localize(None)

date_end1 =pd.to_datetime(date4, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_end1 = date_end0.tz_localize(None)

""" date_start2 =pd.to_datetime(date5, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_start2 = date_start0.tz_localize(None)

date_end2 =pd.to_datetime(date6, format='%Y-%m-%dT%H:%M:%S%z')#フォーマットを変更して、タイムゾーン情報を含む形式を指定します
date_end2 = date_end0.tz_localize(None) """

b = (a2["data"][0]["score"])#変数に一日目のスコアを代入

duration_in_hrs = (a0["data"][0]["total_sleep_duration"])#変数に一日目の睡眠時間を代入

#x_choice = st.radio("", ("今日", "昨日","一昨日"), horizontal=True, args=[1, 0])<3日間のグラフ表示変更>

fig = go.Figure()

# データトレースを追加
fig.add_trace(go.Scatter(
    x=[date_start0, date_start0],
    y=[36, 38],
    mode='lines+markers',
    name='lines+markers',
    line=dict(color="Red", width=3)
))
fig.add_trace(go.Scatter(
    x=[date_end0, date_end0],
    y=[36, 38],
    mode='lines+markers',
    name='lines+markers',
    line=dict(color="Red", width=3)
))


st.plotly_chart(fig)


ss1 = '睡眠スコアは'
ss2 = b
ss3 = 'でした'
st.markdown("{0}{1}{2}".format(ss1,ss2,ss3))

# 睡眠時間

# 小数点切り捨て
n = 1
m = duration_in_hrs / 3617.14286#(仮)total_sleep_durationを時間に変更する
new_duration_in_hrs = math.floor(m * 10 ** n) / (10 ** n)

ss1 = '睡眠時間は'
ss2 = new_duration_in_hrs
ss3 = '時間でした'
st.markdown("{0}{1}{2}".format(ss1,ss2,ss3))

# 起床時刻と体温上がり初めの差異
""" rhythm_delay = df_getup.strftime('%H時%M分%S秒')
a = 'あなたの眠ってから体温が上がり始めた時刻は'
b = 'です'
c = rhythm_delay
st.markdown("{0}{1}{2}".format(a,c,b))
st.caption("深部体温は正常なリズムの場合，入眠と共に低下し，眠っている間は低い状態がキープされ，目覚めに向けて再度上昇していきます．")
st.caption("深部体温が上昇することで体が活動できるように変化していきます．起床するとさらに深部体温が上昇します．深部体温が上昇し始めるよりも先に起床してしまうのは良い目覚めとは言えません．")


# 就寝時刻と体温下がり始めの差異
rhythm_delay_fa = df_fall_asleep - date_start[0]
a = 'あなたの眠ってから体温が下がり始めるまでの時間は'
b = 'です'
c = rhythm_delay_fa
st.markdown("{0}{1}{2}".format(a,c,b))
st.caption("正常なリズムの場合，入眠と共に深部体温は低下していきます．低下しない場合，良い睡眠は得られません．体温の最高値と最低値の差は健康な場合1°C程度です．")
 """