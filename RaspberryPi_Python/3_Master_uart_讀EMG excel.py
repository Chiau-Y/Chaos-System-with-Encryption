import matplotlib.pyplot as plt
import Adafruit_MCP4725
import RPi.GPIO
import serial
import time
import xlrd

start = time.time()
dac = Adafruit_MCP4725.MCP4725(address=0x60)    # DAC
ser = serial.Serial("/dev/ttyAMA0",115200)  # UART

book = xlrd.open_workbook('/home/pi/Chaos/Rawdata/EMG.xlsx',encoding_override='utf-8')
sheet = book.sheets()[0]

k, j ,i ,num = 0, 0, 0, 0
x1, x2, x3 = 4, 3, 2

data_o, data_e, x11 = [], [], []

print("--------------Start--------------")
while True:
        print("\nStart sending data\n")
        rows = sheet.nrows
        for i in range(rows-1):
                d = int(sheet.cell(i+1,0).value)
                dac.set_voltage(round(d*4095/255))
                #--------------------------------------Encryption-------------------------------------- 
                e1 = x2

                x1s = 0.9822*x1 + 0.01793*x2 + (4.488e-06)*(-x1)*x3
                x2s = 1.01*x2 + 0.0005025*(-x1)*x3
                x3s = 0.9985*x3 + 0.0004996*x1*x2  
                x1, x2, x3 = x1s, x2s, x3s 
                #dac.set_voltage(round((x1+25)*4095/50))

                if (i%3000) <= 500 :
                     scale = 100
                elif (i%3000) <= 1000:
                     scale = 350
                elif (i%3000) <= 1500:
                     scale = 500
                elif (i%3000) <= 2000:
                     scale = 150
                elif (i%3000) <= 2500:
                     scale = 200
                else:
                     scale = 400

                d_encryption = round(d + scale*x1,2)                       #Encryption

                data_o.append(d)
                data_e.append(d_encryption)
                x11.append(x1)  
                
                msg = ',' + str(round(e1,3)) +',' + str(d_encryption) + ',' + '\n'
                ser.write(msg.encode()) 
                num+=1  
        break


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
plt.subplot(2,1,1)
l1,=plt.plot(data_o,color='#4169e1')
plt.legend(handles=[l1], labels=['Original Data'], loc='lower right')
plt.subplot(2,1,2)
l2,=plt.plot(data_e,color='#db7093')
plt.legend(handles=[l2], labels=['Encrypted Data'], loc='lower right')
# plt.subplot(3,1,3)
# l3,=plt.plot(x11,color='#ff8c00')
# plt.legend(handles=[l3], labels=['x1'], loc='lower right')
plt.xlabel('The number of data')
plt.show()
