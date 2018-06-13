import RPi.GPIO as GPIO
import time
from ctypes import *
import os

#存放时序数据
data = [0 for i in range(40)]
def driver():
        j = 0
        # 传感器上电后，要等待1s以越过不稳定状态
        GPIO.setmode(GPIO.BOARD)
        time.sleep(1)
        # 先向传感器发送开始信号，握手-LOW-
        GPIO.setup(16, GPIO.OUT)
        GPIO.output(16, GPIO.LOW)
        # 主机把总线拉低必须大于18毫秒，这里采用20毫秒
        time.sleep(0.02)
        # 然后主机拉高并延时等待传感器的响应
        GPIO.output(16, GPIO.HIGH)
        # 执行1次需要十几微秒
        i = 1
        i = 1
        # 等待传感器的握手响应信号和数据信号
        GPIO.setup(16, GPIO.IN)
        while GPIO.input(16) == 1:
                continue
        # 总线为低电平，说明传感器发送响应信号，80us低电平
        while GPIO.input(16) == 0:
                continue
        # 然后传感器再把总线拉高80us，然后才准备发送数据
        while GPIO.input(16) == 1:
                continue
        # 开始发送数据
        # 一次完整的数据为40bit，高位先出
        # 8bit湿度整数数据+8bit湿度小数数据+8bit温度整数数据+8bit温度小数数据+8bit校验和
        while j < 40:
                k = 0
                #每一位的起始信号，都以50us低电平开始
                while GPIO.input(16) == 0:
                        continue
                #每一位的数值信号，高电平的长短决定了数据位是0还是1。
                while GPIO.input(16) == 1:
                        #需要知道每次循环的耗时，才能知道k < x是表示0
                        k += 1
                        if k > 100:
                                break
                # 高电平持续26-28us表示0， 高电平持续70us表示1
                if k < 3:
                        data[j] = 0
                else:
                        data[j] = 1
                j += 1
        print(data)
#2）计算湿度、温度、校验和
def compute():
        humidity_bit = data[0:8]
        humidity_point_bit = data[8:16]
        temperature_bit = data[16:24]
        temperature_point_bit = data[24:32]
        check_bit = data[32:40]
        humidity = 0
        humidity_point = 0
        temperature = 0
        temperature_point = 0
        check = 0

#按照每8位转换成一个十进制数字
        for i in range(8):
               # 湿度整数部分
                humidity += humidity_bit[i] * 2**(7-i)
                humidity_point += humidity_point_bit[i] * 2**(7-i)
               # 温度整数部分
                temperature += temperature_bit[i] * 2**(7-i)
                temperature_point += temperature_point_bit[i] * 2**(7-i)
                check += check_bit[i] * 2**(7-i)
        sum = humidity + humidity_point + temperature + temperature_point
        print("temperature:", temperature, ", humidity:", humidity)
        if check == sum:
                print("temperature:", temperature, ", humidity:", humidity)
        else:
                print("wrong!", check, "!=",  sum)

if __name__ == "__main__":
        driver()
        compute()
        GPIO.cleanup()
