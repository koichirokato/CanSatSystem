# import
import math
import pandas as pd
import numpy as np
import random
import datetime
import CameraSystem
import SocketCommunication
from GPSCalculation import vincenty_inverse

# x:緯度,y:経度 
# 東京タワー
Goal_x = 35.658581
Goal_y = 139.745433
# 豊洲キャンパス
position_x = 35.660533
position_y = 139.794851

start_x = position_x
start_y = position_y

filename = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
df_log = pd.DataFrame(columns=['time','position_x','position_y','Goal_x','Goal_y','distance','azimuth','direction'])
df_log = df_log.append(pd.Series([datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),position_x,position_y,Goal_x,Goal_y,0,0,''], index=df_log.columns), ignore_index=True)
advance_coff = 1
count = 0
direction = ''

while True:
    count += 1

    # GPSから取得した値をもとにposition_x,yを更新
    diff_x = Goal_x - position_x
    diff_y = Goal_y - position_y

    random_x = random.random()*0.0001
    random_y = random.random()*0.0001

    if count >= 500:
        random_x = random_y = 0
        
    position_x += diff_x * 0.1 * advance_coff + random_x
    position_y += diff_y * 0.1 * advance_coff + random_y

    # 緯度経度の計算
    result = vincenty_inverse(position_x, position_y, Goal_x, Goal_y, 1)

    # 距離ごとに前進する時間を変える advance_coff
    # 角度によって旋回する向きと量を変える
    distance = result['distance']
    azimuth  = result['azimuth1']
    if   azimuth < 45:  direction = 'north'
    elif azimuth < 135: direction = 'east'
    elif azimuth < 225: direction = 'south'
    elif azimuth < 315: direction = 'west'
    elif azimuth < 360: direction = 'north'
    else: direction = 'error'

    advance_coff = distance * 0.01
    if advance_coff>1: advance_coff = 1
#     advance_coff = 1
    if result['distance'] < 5:
        print("count : "+ str(count))
        print("Camera mode")
        break
    if count > 10000:
        print("#######count over#########")
        break
    
    # ログ用 pandasDataFrame
    tmp = pd.Series([datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),position_x,position_y,Goal_x,Goal_y,distance,azimuth,direction], index = df_log.columns)
    socket_send_data = tmp.to_json()
    df_log = df_log.append(tmp, ignore_index = True)
    
    df_log.to_csv('CanSat_log/log.csv')