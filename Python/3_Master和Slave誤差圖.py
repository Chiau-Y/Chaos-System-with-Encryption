import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

f = open('D:\\test08.raw', 'rb')              #read the data
k, j ,i ,num, u2, e1, e2 = 0, 0, 0, 0, 0, 0, 0
x1, x2, x3 = 4, 3, 2
y1, y2, y3 = 8, -1, 5
Kp, Ki = 0.9, 0.8
# Kp, Ki = 0.9, 0.3
# x1, x2, x3 = 5, -3, 12
# y1, y2, y3 = -8, 1, -5
# Kp, Ki = 1.1, 0.8
e1_sum, e2_sum = 0, 0

Data1 = [[0]*8 for i in range(12500)]         #row = unknown , column = 8
Data2 = [[0]*8 for i in range(12500)]         #row = unknown , column = 8
Data = [[0]*8 for i in range(12500)]
raw_data_format = [0]*600  
flag = [0]*2                                  #stop recieve the data, stop recieve raw file format

data_o = []                                   #matplot
data_e = []                                   #matplot
data_d = []                                   #matplot
x11 = []                                      #matplot
x22 = []                                      #matplot
x33 = []                                      #matplot
y11 = []                                      #matplot
y22 = []                                      #matplot
y33 = []                                      #matplot
e = []                                        #matplot

while True :                     
#----------------------------------Raw file Format-----------------------------------
       if flag[1] == 0:
              data = f.read(1) #line()                            #read the data by one byte, open the file
              d = ord(data) 
              raw_data_format[k] = d
              if k == 511 :
                     flag[1] = 1
              k += 1 
#------------------------------------Save the data------------------------------------
       else:
              for i in range(12500):
                     for j in range(8):
                            data = f.read(1)                     #read the data by one byte
                            # if i == 5000:
                            #        flag[0] = 1                   #stop recieve the data
                            #        break                                                    
                            if not data:  
                                   flag[0] = 1                   #stop recieve the data
                                   break        
                            else :
                                   d = ord(data)
                                   
                                   if j == 3:
                                          Data[i][j] = d 
#--------------------------------------Eecryption-------------------------------------- 
                                          e1 = x2
                                          e1_sum += e1

                                          x1s = 0.9822*x1 + 0.01793*x2 + (4.488e-06)*(-x1)*x3
                                          x2s = 1.01*x2 + 0.0005025*(-x1)*x3
                                          x3s = 0.9985*x3 + 0.0004996*x1*x2  
                                          x1, x2, x3 = x1s, x2s, x3s

                                          x2n = (x2+30)*255/60
                                          Data1[i][j] = round(d + x2n)                       #Encryption
#--------------------------------------Decryption--------------------------------------
                                          e2 = -y2
                                          e2_sum += e2
                                          u2 = Kp*(e1 + e2) + Ki*(e1_sum + e2_sum)

                                          y1s =  0.9822*y1 +0.01793*y2 + (4.488e-06)*(-y1)*y3
                                          y2s = 1.01*y2 + 0.0005025 *(-y1)*y3 + u2
                                          y3s = 0.9985*y3 + 0.0004996*y1*y2
                                          y1, y2, y3 = y1s, y2s, y3s  

                                          y2n = (y2+30)*255/60        
                                          Data2[i][j] = round(Data1[i][j]-y2n)        #Decryption

                                          data_o.append(Data[i][j])
                                          data_e.append(Data1[i][j])
                                          data_d.append(Data2[i][j])
                                          x11.append(x1)  
                                          x22.append(x2n) 
                                          x33.append(x3) 
                                          y11.append(y1)  
                                          y22.append(y2n) 
                                          y33.append(y3) 
                                          # e.append(x2n-y2n)
                                          e.append(Data[i][j]-Data2[i][j])   
                                          num+=1   
                                          # print("No. ",num,"x2 = ",'%.6f'%x2s,"y2 = ",'%.6f'%y2s,"e = ",'%.6f'%(e1+e2),end = '\n')  
                                          # print("Data = ",Data[i][j],"x2 = ",x2s,"y2 = ",y2s,"Encryption = ",'%.6f   '%Data1[i][j],"Decryption = ",Data2[i][j],end = "\n")    
                                   else:
                                          pass
                     if flag[0] == 1:
                            break
              if flag[0] == 1:
                     flag[0] = 0
                     # print(num)
                     break
f.close()

###################################################
# Original Data vs Encryption vs Decryption
plt.figure(1)
plt.subplot(4,1,1)
l1,=plt.plot(x22,color='#4169e1')
plt.legend(handles=[l1], labels=['Master_x'], loc='lower right')
plt.subplot(4,1,2)
l2,=plt.plot(y22,color='#db7093')
plt.legend(handles=[l2], labels=['Slaver_y'], loc='lower right')
plt.subplot(4,1,3)
l1,=plt.plot(x22,color='#4169e1')
l2,=plt.plot(y22,color='#db7093')
plt.legend(handles=[l1, l2], labels=['Master_x','Slaver_y'], loc='lower right')
plt.subplot(4,1,4)
l3,=plt.plot(e,color='#ff8c00')
plt.legend(handles=[l3], labels=['Error'], loc='lower right')
plt.xlabel('Number of data')

plt.show()