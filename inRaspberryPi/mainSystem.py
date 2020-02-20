#!/usr/bin/python
# -*- coding: utf-8 -*-

# import
import math
import pandas as pd
import numpy as np
import random
import datetime
# import CameraSystem
import SocketCommunication
from GPSCalculation import vincenty_inverse
from BMX055 import getBMXMag, initAcclData, getAcclData, initializeBMX055
from MotorControl import forward, reverse, turnLeft, turnRight, motorStop
import serial
import micropyGPS
import threading
import time
# from CameraSystem import camera_system

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

gps = micropyGPS.MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。
                                     # 引数はタイムゾーンの時差と出力フォーマット

def getGPS():
    def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
        s = serial.Serial('/dev/ttyS0', 9600, timeout=10)
        s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
        while True:
            sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
            if sentence[0] != '$': # 先頭が'$'でなければ捨てる
                continue
            for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
                gps.update(x)

    gpsthread = threading.Thread(target=rungps, args=()) # 上の関数を実行するスレッドを生成
    gpsthread.daemon = True
    gpsthread.start() # スレッドを起動

def camera_mode():
    red_points = camera_system()
    if len(red_points) > 0:
        red_point        = max(red_points, key=(lambda x: x[2] * x[3]))
        red_point_center = np.array(red_point[0:2] + (red_point[2:4])/2, dtype=int)
        red_point_center = np.round(red_point_center)
        print 'red_point : ' + str(red_point_center)

def direction_check(azimuth):
    if   azimuth < 45:  direction = 'north'
    elif azimuth < 135: direction = 'east'
    elif azimuth < 225: direction = 'south'
    elif azimuth < 315: direction = 'west'
    elif azimuth < 360: direction = 'north'
    else: direction = 'error'

def update_location():
    # GPSから取得した値をもとにposition_x,yを更新
    position_x = gps.latitude[0]
    position_y = gps.longitude[0]

    diff_x = Goal_x - position_x
    diff_y = Goal_y - position_y
    
    # 緯度経度の計算
    result = vincenty_inverse(position_x, position_y, Goal_x, Goal_y, 1)

    # 距離ごとに前進する時間を変える advance_coff
    # 角度によって旋回する向きと量を変える
    distance = result['distance']
    azimuth  = result['azimuth1']

    direction = getBMXMag()
    directionGoal   = direction_check(azimuth)
    directionCanSat = direction_check(direction)

    advance_coff = distance * 0.01
    if advance_coff>1: advance_coff = 1

    return result, direction

def motor(name, spd, sleeptime=1):
    if name == 'f': forward(spd)
    if name == 'b': reverse(spd)
    if name == 'r': turnRight(spd)
    if name == 'l': turnLeft(spd)
    time.sleep(sleeptime)
    motorStop()
    time.sleep(1)

if __name__ == '__main__':
    print "start at : " + str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    
    print "initialize Accl Data"
    initializeBMX055()
    offset = initAcclData()
    time.sleep(1)
    print offset
    while True:
        getAcclData(offset[0],offset[1],offset[2])
        getBMXdata()
        time.sleep(0.2)

    print "start GPS scan"
    getGPS()
    
    while True:
        # 加速度を取得、パラシュートの切り離しに使う
        acclData = getAcclData(offset[0],offset[1],offset[2])
        

        print "######count : " + str(count)
        count += 1
        print gps.clean_sentences
        # GPSのデータがある程度たまったら
        if gps.clean_sentences > 20:
            # motor('f',10,1)
            # motor('b',10,1)
            result, direction = update_location()
            distance = result['distance']
            azimuth  = result['azimuth1']
            
            # direction と azimuth で向きを計算、旋回

            # カメラ
            if result['distance'] < 5:
                print "count : "+ str(count)
                print "Camera mode"
                camera_mode()
                break
            if count > 10000:
                print("#######count over#########")
                break
            
            # ログ用 pandasDataFrame
            tmp = pd.Series([datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),position_x,position_y,Goal_x,Goal_y,distance,azimuth,direction], index = df_log.columns)
            socket_send_data = tmp.to_json()
            print tmp
            df_log = df_log.append(tmp, ignore_index = True)
            
            df_log.to_csv('CanSat_log/log.csv')
        time.sleep(5)