import matplotlib.pyplot as plt
import numpy as np
 
f = open('D:\\test08.raw', 'rb')              #read the data

Data = [[0]*8 for i in range(12500)]
raw_data_format = [0]*600  
flag = [0]*2                                  #stop recieve the data, stop recieve raw file format

data_0 = []                                   #matplot
data_1 = []                                   #matplot
data_2 = []                                   #matplot
data_3 = []                                   #matplot
data_4 = []                                   #matplot
data_5 = []                                   #matplot
data_6 = []                                   #matplot
numm = [1, 2, 3, 4, 5, 6]
datanum = []

while True :                     
#-----------------------------------Raw file Format-----------------------------------
       if flag[1] == 0:
              data = f.read(1) # read the data by one byte, open the file
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
                            if i == 3500:
                                   flag[0] = 1                   #stop recieve the data
                                   break                                                    
                            if not data:  
                                   flag[0] = 1                   #stop recieve the data
                                   break        
                            else :
                                   d = ord(data)                                  
                                   Data[i][j] = d 
                                   # 每500筆找一次峰值
                                   if j == 3: # channel number
                                          if i <= 500:
                                                 data_0.append(d)
                                          if i > 500 and i <= 1000:
                                                 data_1.append(d)
                                          elif i > 1000 and i <= 1500:
                                                 data_2.append(d)
                                          elif i > 1500 and i <= 2000:
                                                 data_3.append(d)
                                          elif i > 2000 and i <= 2500:
                                                 data_4.append(d)
                                          elif i > 2500 and i <= 3000:
                                                 data_5.append(d)
                                          elif i > 3000 and i <= 3500:
                                                 data_6.append(d)
                                                 
                                          num += 1                                     
                     if flag[0] == 1:
                            break
              if flag[0] == 1:
                     flag[0] = 0
                     break
f.close()

# 採樣頻率為 500 Hz, 兩個峰值之間採樣點數 (個數) / 500 (個數/sec) = 每1個心跳多少秒 --> 60秒/每1個心跳多少秒 = 心跳/每分鐘
print("The index of the highest value in 0~500 data : no.",data_0.index(max(data_0)))
print("The index of the highest value in 501~100 data : no.",(501 + data_1.index(max(data_1))))
print("The Difference is : ",((501 + data_1.index(max(data_1)))-data_0.index(max(data_0))), "data")
print("The number of heart beats : ",round(60/(((501 + data_1.index(max(data_1)))-data_0.index(max(data_0)))*(1/500)),2),"times/min.")
print("-------------------------------------")
print("The index of the highest value in 501~1000 data : no.",data_1.index(max(data_1)))
print("The index of the highest value in 1001~1500 data : no.",(501 + data_2.index(max(data_2))))
print("The Difference is : ",((501 + data_2.index(max(data_2)))-data_1.index(max(data_1))), "data")
print("The number of heart beats : ",round(60/(((501 + data_2.index(max(data_2)))-data_1.index(max(data_1)))*(1/500)),2),"times/min.")
print("-------------------------------------")
print("The index of the highest value in 1001~1500 data : no.",data_2.index(max(data_2)))
print("The index of the highest value in 1501~2000 data : no.",(501 + data_3.index(max(data_3))))
print("The Difference is : ",((501 + data_3.index(max(data_3)))-data_2.index(max(data_2))), "data")
print("The number of heart beats : ",round(60/(((501 + data_3.index(max(data_3)))-data_2.index(max(data_2)))*(1/500)),2),"times/min.")
print("-------------------------------------")
print("The index of the highest value in 1501~2000 data : no.",data_3.index(max(data_3)))
print("The index of the highest value in 2001~2500 data : no.",(501 + data_4.index(max(data_4))))
print("The Difference is : ",((501 + data_4.index(max(data_4)))-data_3.index(max(data_3))), "data")
print("The number of heart beats : ",round(60/(((501 + data_4.index(max(data_4)))-data_3.index(max(data_3)))*(1/500)),2),"times/min.")
print("-------------------------------------")
print("The index of the highest value in 2001~2500 data : no.",data_4.index(max(data_4)))
print("The index of the highest value in 2501~3000 data : no.",(501 + data_5.index(max(data_5))))
print("The Difference is : ",((501 + data_5.index(max(data_5)))-data_4.index(max(data_4))), "data")
print("The number of heart beats : ",round(60/(((501 + data_5.index(max(data_5)))-data_4.index(max(data_5)))*(1/500)),2),"times/min.")
print("-------------------------------------")
print("The index of the highest value in 2501~3000 data : no.",data_5.index(max(data_5)))
print("The index of the highest value in 3001~3500 data : no.",(501 + data_6.index(max(data_6))))
print("The Difference is : ",((501 + data_6.index(max(data_6)))-data_5.index(max(data_5))), "data")
print("The number of heart beats : ",round(60/(((501 + data_6.index(max(data_6)))-data_5.index(max(data_5)))*(1/500)),2),"times/min.")
