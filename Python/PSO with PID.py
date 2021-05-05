# Reference : https://blog.csdn.net/weixin_43943550/article/details/90601945

# -------------------------------- #
# 利用PSO找混沌系統中PID最佳解    #
# 每一次的iteration，混沌系統都跑1000次 #
# 利用最後的誤差去決定這次PID數值的好壞 #
# 利用DAC將數值在示波器上顯示        #
# -------------------------------- #

import numpy as np
import random
import matplotlib.pyplot as plt
import math
 
x1, x2, x3 = 4, 3, 2
y1, y2, y3 = 8, -1, 5
e_sum, e_old = 0, 0 
iterators = 0
 
# ----------------------PSO參數設定---------------------------------
class PSO():
    def __init__(self, pN, dim):
        self.w = 0.7  # [0.0,1.5]
        self.c1 = 2  # [0,4]
        self.c2 = 2  # [0,4]
        self.r1 = 0.6
        self.r2 = 0.3
        self.pN = pN  # 粒子數量 [20,40]
        self.dim = dim  # 搜索维度 
        self.X = np.zeros((self.pN, self.dim))  # 所有粒子的位置和速度
        self.V = np.zeros((self.pN, self.dim))
        self.pbest = np.zeros((self.pN, self.dim))  # 個體經歷的最佳位置和全局最佳位置
        self.gbest = np.zeros((1, self.dim))
        self.p_fit = np.zeros(self.pN)  # 每個個體的歷史最佳適應值
        self.fit = 1e10  # 全局最佳適應值
 
# ---------------------------目標函數--------------------------------
    def function(self, Kp, Ki, Kd):
        x1, x2, x3 = 4, 3, 2
        y1, y2, y3 = 8, -1, 5
        e_sum, e_old = 0, 0 

        for i in range (1000):
            e = x2 - y2
            e_sum += e

            x1s = 0.9822*x1 + 0.01793*x2 + (4.488e-06)*(-x1)*x3
            x2s = 1.01*x2 + 0.0005025*(-x1)*x3
            x3s = 0.9985*x3 + 0.0004996*x1*x2  
            x1, x2, x3 = x1s, x2s, x3s 

            y1s =  0.9822*y1 +0.01793*y2 + (4.488e-06)*(-y1)*y3 
            y2s = 1.01*y2 + 0.0005025 *(-y1)*y3 + Kp*e + Ki*e_sum + Kd*(e-e_old)
            y3s = 0.9985*y3 + 0.0004996*y1*y2
            y1, y2, y3 = y1s, y2s, y3s
            
            e_old = e  

        ans = abs(x2 - y2) + abs(x1 - y1) + abs(x3 - y3) 
        return ans  
 
# --------------------------初始化种群----------------------------------
    def init_Population(self):
        for i in range(self.pN):
            for j in range(self.dim):
                self.X[i][j] = random.uniform(0, 0.5)
                self.V[i][j] = random.uniform(0, 1)
            self.pbest[i] = self.X[i]
            tmp = self.function(self.X[i][0],self.X[i][1],self.X[i][2])
            self.p_fit[i] = tmp
            if tmp < self.fit:
                self.fit = tmp
                self.gbest = self.X[i]
 
# -------------------------更新粒子位置---------------------------------- 
    def iterator(self):
        global iterators
        Error = []
        kp, ki, kd = [], [], []
        while (True):
            iterators += 1
            for i in range(self.pN):  # 更新gbest\pbest
                temp = self.function(self.X[i][0],self.X[i][1],self.X[i][2])
                if temp < self.p_fit[i]:  # 更新個體最優
                    self.p_fit[i] = temp
                    self.pbest[i] = self.X[i]
                    if self.p_fit[i] < self.fit:  # 更新全局最優
                        self.gbest = self.X[i]
                        self.fit = self.p_fit[i]
            for i in range(self.pN):
                self.V[i] = self.w * self.V[i] + self.c1 * self.r1 * (self.pbest[i] - self.X[i]) + \
                            self.c2 * self.r2 * (self.gbest - self.X[i])
                self.X[i] = self.X[i] + self.V[i]
            Error.append(self.fit)
            kp.append(self.X[i][0])
            ki.append(self.X[i][1])
            kd.append(self.X[i][2])
            print("No. ",iterators, end=" ")
            print(self.X[0], end=" ")
            print(self.fit)  # 輸出目前最好的數值(最小誤差值)
            if round(self.fit,7) < 1e-7 : # 當誤差值小於10的-7次方時停止PSO
                break
            elif iterators == 200:  # 當跑200次iteration時停止PSO
                break
        return Error, kp, ki, kd
 
# ----------------------Main Program-----------------------
my_pso = PSO(pN=40, dim=3) # 三個維度 for PID
my_pso.init_Population()
Error, kp, ki, kd = my_pso.iterator()

# -------------------------Plot-----------------------
plt.figure(1)
plt.title("PID with PSO")
plt.xlabel("iterators", size=14)
plt.ylabel("fitness(Error)", size=14)
t = np.array([t for t in range(0, iterators)])
l4, = plt.plot(t, np.array(Error), color='g', linewidth=3, label='Error')
plt.legend(loc='upper right')

plt.figure(2)
plt.title("PID with PSO")
plt.xlabel("iterators", size=14)
plt.ylabel("fitness", size=14)
t = np.array([t for t in range(0, iterators)])
l1, = plt.plot(t, np.array(kp), color='#db7093', linewidth=3, label='Kp')
l2, = plt.plot(t, np.array(ki), color='b', linewidth=3, label='Ki')
l3, = plt.plot(t, np.array(kd), color='#ff8c00', linewidth=3, label='Kd')

plt.legend(loc='upper right')
plt.show()
