% -------------------------------------------------- %
% 使用混沌系統(Choas System)中的呂氏系統(Lu System)    %
% 利用不同初始值，來創造兩個混沌系統 - Master和Slave    %
% 用PID控制器同步兩個系統，控制器u放在非線性項的第二狀態 %
% -------------------------------------------------- %

clc;clear;

k=10000;    % The number of data

% ====== Parameters for PID ====== %
Kp = 0.0257;  
Ki = 0;  
Kd = 0.133;  

% ====== Initial Setting ====== %
u = zeros(1,k);e = zeros(1,k);
x1 = zeros(1,k);x2 = zeros(1,k);x3 = zeros(1,k);
y1 = zeros(1,k);y2 = zeros(1,k);y3 = zeros(1,k);

% ====== Initial conditions  ====== %
x1(1) = 4; x2(1) = 3; x3(1) = 2;    
y1(1) = 8; y2(1) = -1; y3(1) = 5;	
e_old=0;    % Initial for PID's Kd

% ====== Iterations for Choas System  ====== %
for i=1:k-1   
    e(i) = x2(i)-y2(i);
    u(i) = Kp*e(i)+ Ki*(sum(e))+Kd*(e(i)-e_old);    % PID Controller
    
    % ====== Master  ====== %
    x1(i+1) = 0.9822*x1(i) + 0.01793*x2(i) + (4.488e-06)*(-x1(i))*x3(i);
    x2(i+1) = 1.01*x2(i) + 0.0005025*(-x1(i))*x3(i);
    x3(i+1) = 0.9985*x3(i) + 0.0004996*x1(i)*x2(i);    
    
    % ====== Slave  ====== %
    y1(i+1) =  0.9822*y1(i) +0.01793*y2(i) + (4.488e-06)*(-y1(i))*y3(i);
    y2(i+1) = 1.01*y2(i) + 0.0005025 *(-y1(i))*y3(i) + u(i);    % PID controller added in the Slave 
    y3(i+1) = 0.9985*y3(i) + 0.0004996*y1(i)*y2(i);
    
    e_old = e(i);
end

% ====== Plot first state with synchronization and Error  ====== %
figure(1)
subplot(2,1,1)
plot(x2,'.b');hold on;
plot(y2,'.','Color',[1 0.5 0]);hold on;
legend('$Master : x_2$','$Slave : \bar{x_2}$','Interpreter','Latex','FontSize',14)
ylabel('value');
xlabel('The number of data');
subplot(2,1,2)
plot(e,'.','Color',[0.5 1 0.5]);
legend('$Error$','Interpreter','Latex','FontSize',14); 
xlabel('The number of data');
ylabel('value');

% ====== Plot every state with synchronization and Error  ====== %
figure(2)
subplot(4,1,1)
plot(x1,'-b');hold on;
plot(y1,'-r');hold on; 
subplot(4,1,2)
plot(x2,'-b');hold on;
plot(y2,'-r');hold on;
subplot(4,1,3)
plot(x3,'-b');hold on;
plot(y3,'-r');hold on;
subplot(4,1,4)
plot(e,'g');
legend('Error'); 
axis([-inf,inf,-0.001,0.001])

% ====== Plot Xs and Ys in Master and Slave  ====== %
figure(3)
subplot(2,1,1)  % Master
plot(x1,'-');hold on;
plot(x2,'-');hold on;
plot(x3,'-');hold on;
legend('x1','x2','x3'); 
subplot(2,1,2)  % Slave
plot(y1,'-');hold on;
plot(y2,'-');hold on;
plot(y3,'-');hold on;
legend('$\bar{x1}$','$\bar{x2}$','$\bar{x3}$','Interpreter','Latex')
