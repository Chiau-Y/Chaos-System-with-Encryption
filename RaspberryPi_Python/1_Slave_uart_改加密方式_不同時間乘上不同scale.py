import matplotlib.pyplot as plt
import Adafruit_MCP4725
import RPi.GPIO
import serial
import time

dac = Adafruit_MCP4725.MCP4725(address=0x60)    # DAC
ser = serial.Serial("/dev/ttyAMA0",115200)  # UART

y1, y2, y3 = 8, -1, 5
Kp, Ki = 0.9, 0.8
e_sum, num = 0, 0
data_e, data_d = [], []
ready = 0
a = 0

print("--------Start----------")

while True:
        read_data = ser.inWaiting()       
        if read_data != 0:             
                msg_r = str(ser.readline())  
                if ready == 0:
                        start=time.time()
                        print("\nStart receiving data\n")
                        ready = 1
# -----------------------------Decryption------------------------------
                msg = msg_r.split(',')
                if msg[len(msg)-2] == 's' :
                        break
                else:
                        e1 = float(msg[1])
                        d_encryption = float(msg[2])             
                        e2 = -y2
                        e_sum += (e2+e1)
                        u2 = Kp*(e1 + e2) + Ki*e_sum
                        if (e2+e1) < 0.0001 and a == 0:
                                pid=time.time()
                                print("Synchronization Time : ",round(pid-start,3)," sec")
                                a = 1
                        y1s =  0.9822*y1 +0.01793*y2 + (4.488e-06)*(-y1)*y3
                        y2s = 1.01*y2 + 0.0005025 *(-y1)*y3 + u2
                        y3s = 0.9985*y3 + 0.0004996*y1*y2
                        y1, y2, y3 = y1s, y2s, y3s  
                        
                        #dac.set_voltage(round((y1+25)*2047/50))
                        
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
                        
                        d_decryption = round(d_encryption-scale*y1)        #Decryption
                        dac.set_voltage(round(d_decryption*4095/255))
                        
                        data_e.append(d_encryption)
                        data_d.append(d_decryption)
                        num+=1   

end=time.time()
print("Time : ",round(end-start,3)," sec")
print("The number of data : ",num-1)
print("--------END----------")

plt.figure(1)
plt.subplot(2,1,1)
l1,=plt.plot(data_e,color='#db7093')
plt.legend(handles=[l1], labels=['Encrypted Data'], loc='lower right')
plt.subplot(2,1,2)
l2,=plt.plot(data_d,color='#ff8c00')
plt.legend(handles=[l2], labels=['Decrypted Data'], loc='lower right')
plt.xlabel('The number of data')
plt.show()
