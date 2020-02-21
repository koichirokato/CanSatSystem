#!/usr/bin/python
# -*- coding: utf-8 -*-

import smbus
import time
import math

# Get I2C bus
bus = smbus.SMBus(1)

def initializeBMX055():
    # BMX055 Accl address, 0x19
    # Select PMU_Range register, 0x0F(15)
    #       0x03(03)    Range = +/- 2g
    try:
        bus.write_byte_data(0x19, 0x0F, 0x03)
    except:
        pass
    # BMX055 Accl address, 0x19
    # Select PMU_BW register, 0x10(16)
    #       0x08(08)    Bandwidth = 7.81 Hz
    bus.write_byte_data(0x19, 0x10, 0x08)
    # BMX055 Accl address, 0x19
    # Select PMU_LPW register, 0x11(17)
    #       0x00(00)    Normal mode, Sleep duration = 0.5ms
    bus.write_byte_data(0x19, 0x11, 0x00)

    time.sleep(0.5)

    # BMX055 Gyro address, 0x69
    # Select Range register, 0x0F(15)
    #       0x04(04)    Full scale = +/- 125 degree/s
    try:
        bus.write_byte_data(0x69, 0x0F, 0x04)
    except:
        pass
    # BMX055 Gyro address, 0x69
    # Select Bandwidth register, 0x10(16)
    #       0x07(07)    ODR = 100 Hz
    bus.write_byte_data(0x69, 0x10, 0x07)
    # BMX055 Gyro address, 0x69
    # Select LPM1 register, 0x11(17)
    #       0x00(00)    Normal mode, Sleep duration = 2ms
    bus.write_byte_data(0x69, 0x11, 0x00)

    time.sleep(0.5)

    # BMX055 Mag address, 0x13
    # Select Mag register, 0x4B(75)
    #       0x83(121)   Soft reset
    try:
        bus.write_byte_data(0x13, 0x4B, 0x83)
    except:
        pass
    # BMX055 Mag address, 0x13
    # Select Mag register, 0x4C(76)
    #       0x00(00)    Normal Mode, ODR = 10 Hz
    bus.write_byte_data(0x13, 0x4C, 0x00)
    # BMX055 Mag address, 0x13
    # Select Mag register, 0x4E(78)
    #       0x84(122)   X, Y, Z-Axis enabled
    bus.write_byte_data(0x13, 0x4E, 0x84)
    # BMX055 Mag address, 0x13
    # Select Mag register, 0x51(81)
    #       0x04(04)    No. of Repetitions for X-Y Axis = 9
    bus.write_byte_data(0x13, 0x51, 0x04)
    # BMX055 Mag address, 0x13
    # Select Mag register, 0x52(82)
    #       0x0F(15)    No. of Repetitions for Z-Axis = 15
    bus.write_byte_data(0x13, 0x52, 0x0F)

    time.sleep(0.5)

offsetxAccl,offsetyAccl,offsetzAccl = 0,0,0

def initAcclData():
    # calibration use 1000times average
    print('initialize start')
    x,y,z=0,0,0
    for i in range(1000):
        # BMX055 Accl address, 0x19(24)
        # Read data back from 0x02(02), 6 bytes
        # xAccl LSB, xAccl MSB, yAccl LSB, yAccl MSB, zAccl LSB, zAccl MSB
        try:
            data = bus.read_i2c_block_data(0x19, 0x02, 6)
        except:
            initializeBMX055()
            data = bus.read_i2c_block_data(0x19, 0x02, 6)
        # Convert the data to 12-bits
        xAccl = ((data[1] * 256) + (data[0] & 0xF0)) / 16
        if xAccl > 2047 :
            xAccl -= 4096
        yAccl = ((data[3] * 256) + (data[2] & 0xF0)) / 16
        if yAccl > 2047 :
            yAccl -= 4096
        zAccl = ((data[5] * 256) + (data[4] & 0xF0)) / 16
        if zAccl > 2047 :
            zAccl -= 4096

        x += xAccl
        y += yAccl
        z += zAccl
    
    offsetxAccl = -1 * x / 1000
    offsetyAccl = -1 * y / 1000
    offsetzAccl = -1 * z / 1000

    print('initialize finish')
    print('offset x, y, z : ' + str(offsetxAccl) + ',' + str(offsetyAccl) + ',' + str(offsetzAccl))
    return offsetxAccl, offsetyAccl, offsetzAccl

def getAcclData(offsetxAccl, offsetyAccl, offsetzAccl):
    # BMX055 Accl address, 0x19(24)
    # Read data back from 0x02(02), 6 bytes
    # xAccl LSB, xAccl MSB, yAccl LSB, yAccl MSB, zAccl LSB, zAccl MSB
    data = bus.read_i2c_block_data(0x19, 0x02, 6)
    # Convert the data to 12-bits
    xAccl = ((data[1] * 256) + (data[0] & 0xF0)) / 16
    if xAccl > 2047 :
        xAccl -= 4096
    yAccl = ((data[3] * 256) + (data[2] & 0xF0)) / 16
    if yAccl > 2047 :
        yAccl -= 4096
    zAccl = ((data[5] * 256) + (data[4] & 0xF0)) / 16
    if zAccl > 2047 :
        zAccl -= 4096
    
    xAccl += offsetxAccl
    yAccl += offsetyAccl
    zAccl += offsetzAccl

    return xAccl,yAccl,zAccl

def getBMXdata():
    # BMX055 Accl address, 0x19(24)
    # Read data back from 0x02(02), 6 bytes
    # xAccl LSB, xAccl MSB, yAccl LSB, yAccl MSB, zAccl LSB, zAccl MSB
    data = bus.read_i2c_block_data(0x19, 0x02, 6)
    # Convert the data to 12-bits
    xAccl = ((data[1] * 256) + (data[0] & 0xF0)) / 16
    if xAccl > 2047 :
        xAccl -= 4096
    yAccl = ((data[3] * 256) + (data[2] & 0xF0)) / 16
    if yAccl > 2047 :
        yAccl -= 4096
    zAccl = ((data[5] * 256) + (data[4] & 0xF0)) / 16
    if zAccl > 2047 :
        zAccl -= 4096
    
    # BMX055 Gyro address, 0x69(104)
    # Read data back from 0x02(02), 6 bytes
    # xGyro LSB, xGyro MSB, yGyro LSB, yGyro MSB, zGyro LSB, zGyro MSB
    data = bus.read_i2c_block_data(0x69, 0x02, 6)
    # Convert the data
    xGyro = data[1] * 256 + data[0]
    if xGyro > 32767 :
        xGyro -= 65536
    yGyro = data[3] * 256 + data[2]
    if yGyro > 32767 :
        yGyro -= 65536
    zGyro = data[5] * 256 + data[4]
    if zGyro > 32767 :
        zGyro -= 65536

    # BMX055 Mag address, 0x13(16)
    # Read data back from 0x42(66), 6 bytes
    # X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB
    data = bus.read_i2c_block_data(0x13, 0x42, 6)

    # Convert the data
    xMag = ((data[1] * 256) + (data[0] & 0xF8)) / 8
    if xMag > 4095 :
        xMag -= 8192
    yMag = ((data[3] * 256) + (data[2] & 0xF8)) / 8
    if yMag > 4095 :
        yMag -= 8192
    zMag = ((data[5] * 256) + (data[4] & 0xFE)) / 2
    if zMag > 16383 :
        zMag -= 32768

    time.sleep(0.2)

    print "Acceleration in X-Axis : %d" %xAccl
    print "Acceleration in Y-Axis : %d" %yAccl
    print "Acceleration in Z-Axis : %d" %zAccl
    print "X-Axis of Rotation : %d" %xGyro
    print "Y-Axis of Rotation : %d" %yGyro
    print "Z-Axis of Rotation : %d" %zGyro
    print "Magnetic field in X-Axis : %d" %xMag
    print "Magnetic field in Y-Axis : %d" %yMag
    print "Magnetic field in Z-Axis : %d" %zMag
    
    print 90-math.degrees(math.atan2(yMag,xMag))
    cansat_turning = 90-math.degrees(math.atan2(yMag,xMag))
    return cansat_turning

def getBMXMag():
    # BMX055 Mag address, 0x13(16)
    # Read data back from 0x42(66), 6 bytes
    # X-Axis LSB, X-Axis MSB, Y-Axis LSB, Y-Axis MSB, Z-Axis LSB, Z-Axis MSB
    data = bus.read_i2c_block_data(0x13, 0x42, 6)

    # Convert the data
    xMag = ((data[1] * 256) + (data[0] & 0xF8)) / 8
    if xMag > 4095 :
        xMag -= 8192
    yMag = ((data[3] * 256) + (data[2] & 0xF8)) / 8
    if yMag > 4095 :
        yMag -= 8192
    zMag = ((data[5] * 256) + (data[4] & 0xFE)) / 2
    if zMag > 16383 :
        zMag -= 32768

    time.sleep(0.2)

    print 90-math.degrees(math.atan2(yMag,xMag))
    cansat_turning = 90-math.degrees(math.atan2(yMag,xMag))
    return cansat_turning

def stopCheck():
    count = 10
    sleeptime = 1
    stopcount = 0
    offset = initAcclData()
    while True:
        for i in range(count):
            x,y,z = getAcclData(offset[0],offset[1],offset[2])
            print x,y,z
            if abs(x) <= 2 and abs(y) <= 2 and abs(z) <= 2:
                stopcount += 1
                time.sleep(sleeptime)

        if stopcount >= count:
            print 'stop'
            break
        else:
            print 'moving'
            stopcount = 0
            time.sleep(5)


if __name__ == '__main__':
    # Output data to screen
    # bus.write_byte_data(0x13, 0x4B, 0x83)
    # bus.write_byte_data(0x13, 0x4C, 0x00)
    initializeBMX055()
    offset = initAcclData()
    time.sleep(1)
    print(offset)

    stopCheck()
    while True:
        getAcclData(offset[0],offset[1],offset[2])
        getBMXdata()
        time.sleep(0.2)