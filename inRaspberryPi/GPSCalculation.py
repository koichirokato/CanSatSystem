#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import *

# 楕円体
ELLIPSOID_GRS80 = 1 # GRS80
ELLIPSOID_WGS84 = 2 # WGS84

# 楕円体ごとの長軸半径と扁平率
GEODETIC_DATUM = {
    ELLIPSOID_GRS80: [
        6378137.0,         # [GRS80]長軸半径
        1 / 298.257222101, # [GRS80]扁平率
    ],
    ELLIPSOID_WGS84: [
        6378137.0,         # [WGS84]長軸半径
        1 / 298.257223563, # [WGS84]扁平率
    ],
}

# 反復計算の上限回数
ITERATION_LIMIT = 1000

'''
Vincenty法(逆解法)
2地点の座標(緯度経度)から、距離と方位角を計算する
:param lat1: 始点の緯度
:param lon1: 始点の経度
:param lat2: 終点の緯度
:param lon2: 終点の経度
:param ellipsoid: 楕円体
:return: 距離と方位角
'''
def vincenty_inverse(lat1, lon1, lat2, lon2, ellipsoid=None):

    # 差異が無ければ0.0を返す
    if abs(lat1 - lat2) <= 0.00001 and abs(lon1-lon2) <= 0.00001:
        return {
            'distance': 0.0,
            'azimuth1': 0.0,
            'azimuth2': 0.0,
        }

    # 計算時に必要な長軸半径(a)と扁平率(F)を定数から取得し、短軸半径(b)を算出する
    # 楕円体が未指定の場合はGRS80の値を用いる
    a, F = GEODETIC_DATUM.get(ellipsoid, GEODETIC_DATUM.get(ELLIPSOID_GRS80))
    b = (1 - F) * a

    PHAI1 = radians(lat1)
    PHAI2 = radians(lat2)
    LAMDA1 = radians(lon1)
    LAMDA2 = radians(lon2)

    # 更成緯度(補助球上の緯度)
    U1 = atan((1 - F) * tan(PHAI1))
    U2 = atan((1 - F) * tan(PHAI2))

    sinU1 = sin(U1)
    sinU2 = sin(U2)
    cosU1 = cos(U1)
    cosU2 = cos(U2)

    # 2点間の経度差
    L = LAMDA2 - LAMDA1

    # LAMDAをLで初期化
    LAMDA = L

    # 以下の計算をLAMDAが収束するまで反復する
    # 地点によっては収束しないことがあり得るため、反復回数に上限を設ける
    for i in range(ITERATION_LIMIT):
        sinLAMDA = sin(LAMDA)
        cosLAMDA = cos(LAMDA)
        sinOMEGA = sqrt((cosU2 * sinLAMDA) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLAMDA) ** 2)
        cosOMEGA = sinU1 * sinU2 + cosU1 * cosU2 * cosLAMDA
        OMEGA = atan2(sinOMEGA, cosOMEGA)
        sinARUFA = cosU1 * cosU2 * sinLAMDA / sinOMEGA
        cos2ARUFA = 1 - sinARUFA ** 2
        cos2OMEGAm = cosOMEGA - 2 * sinU1 * sinU2 / cos2ARUFA
        C = F / 16 * cos2ARUFA * (4 + F * (4 - 3 * cos2ARUFA))
        LAMDA_dash = LAMDA
        LAMDA = L + (1 - C) * F * sinARUFA * (OMEGA + C * sinOMEGA * (cos2OMEGAm + C * cosOMEGA * (-1 + 2 * cos2OMEGAm ** 2)))

        # 偏差が.000000000001以下ならbreak
        if abs(LAMDA - LAMDA_dash) <= 1e-12:
            break
    else:
        # 計算が収束しなかった場合はNoneを返す
        return None

    # LAMDAが所望の精度まで収束したら以下の計算を行う
    u2 = cos2ARUFA * (a ** 2 - b ** 2) / (b ** 2)
    A = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    diff_OMEGA = B * sinOMEGA * (cos2OMEGAm + B / 4 * (cosOMEGA * (-1 + 2 * cos2OMEGAm ** 2) - B / 6 * cos2OMEGAm * (-3 + 4 * sinOMEGA ** 2) * (-3 + 4 * cos2OMEGAm ** 2)))

    # 2点間の楕円体上の距離
    s = b * A * (OMEGA - diff_OMEGA)

    # 各点における方位角
    ARUFA1 = atan2(cosU2 * sinLAMDA, cosU1 * sinU2 - sinU1 * cosU2 * cosLAMDA)
    ARUFA2 = atan2(cosU1 * sinLAMDA, -sinU1 * cosU2 + cosU1 * sinU2 * cosLAMDA) + pi

    if ARUFA1 < 0:
        ARUFA1 = ARUFA1 + pi * 2

    return {
        'distance': s,           # 距離
        'azimuth1': degrees(ARUFA1), # 方位角(始点→終点)
        'azimuth2': degrees(ARUFA2), # 方位角(終点→始点)
    }