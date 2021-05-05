# -------------------------------- #
# Master端有一個混沌系統             #
# 讀取raw檔，利用混論系統的數值做加密 #
# 加密過後將數值透過UART傳送給Slave端 #
# 利用DAC將數值在示波器上顯示        #
# -------------------------------- #

import matplotlib.pyplot as plt
import Adafruit_MCP4725
import RPi.GPIO
import serial
import time

start = time.time()
dac = Adafruit_MCP4725.MCP4725(address=0x60)    # for DAC
ser = serial.Serial("/dev/ttyAMA0",115200)  # for UART

f = open('/home/pi/Chaos/Rawdata/test02.raw', 'rb') # read the data
k, j ,i ,num = 0, 0, 0, 0
x1, x2, x3 = 4, 3, 2    # initial conditions

data_o, data_e, x11 = [], [], []
flag = [0]*2 

print("--------------Start--------------")
while True:
#----------------------------------Raw file Format-----------------------------------
    if flag[1] == 0:
        data = f.read(1)    # read the data by one byte, open the file
        d = ord(data) 
        if k == 511 :   # discard the first 512 data, they are not biomedical signals
            print("\nStart sending data\n")
            flag[1] = 1
        k += 1 
#------------------------------------Save the data------------------------------------
    else:
        for i in range(12500):
            for j in range(8):  # 8 chanels
                data = f.read(1)    #read the data by one byte
                #if i == 5000:
                    #flag[0] = 1    #stop recieve the data by setting beforehand
                    #break                                                    
                if not data:  
                    flag[0] = 1     #stop recieve the data
                    break        
                else :
                    d = ord(data)                    
                    if j == 0:                        
                        dac.set_voltage(round(d*4095/255))  # DAC to scope with original signals
#--------------------------------------Eecryption-------------------------------------- 
                        e1 = x2

                        x1s = 0.9822*x1 + 0.01793*x2 + (4.488e-06)*(-x1)*x3
                        x2s = 1.01*x2 + 0.0005025*(-x1)*x3
                        x3s = 0.9985*x3 + 0.0004996*x1*x2  
                        x1, x2, x3 = x1s, x2s, x3s 
                        dac.set_voltage(round((x1+25)*2047/50))  # DAC to scope with chaos system's state

                        if (num%3000) <= 500 :
                                scale = 100
                        elif (num%3000) <= 1000:
                                scale = 350
                        elif (num%3000) <= 1500:
                                scale = 500
                        elif (num%3000) <= 2000:
                                scale = 150
                        elif (num%3000) <= 2500:
                                scale = 200
                        else:
                                scale = 400      

                        d_encryption = round(d + scale*x1,2)    # encrytion the signals
                        
                        data_o.append(d)
                        data_e.append(d_encryption) 
                        x11.append(x1) 
  
                        msg = ',' + str(round(e1,3)) +',' + str(d_encryption) + ',' + '\n'
                        ser.write(msg.encode())     # send the encryption signals with UART
                        num+=1                                
                    else:
                        pass
            if flag[0] == 1:
                break
        if flag[0] == 1:
            flag[0] = 0
            break
f.close()

end = time.time()
print("Time : ",round(end-start,3)," sec")

time.sleep(0.001)
msg = ',' + 's' + ',' + '\n'
ser.write(msg.encode()) 
time.sleep(0.0001)
ser.close()

print("The number of data : ", num)
print("--------------End--------------")

plt.figure(1)
plt.subplot(3,1,1)
l1,=plt.plot(data_o,color='#4169e1')
plt.legend(handles=[l1], labels=['Original Data'], loc='lower right')
plt.subplot(3,1,2)
l2,=plt.plot(data_e,color='#db7093')
plt.legend(handles=[l2], labels=['Encrypted Data'], loc='lower right')
plt.subplot(3,1,3)
l3,=plt.plot(x11,color='#ff8c00')
plt.legend(handles=[l3], labels=['x1'], loc='lower right')
plt.xlabel('The number of data')
plt.show()
