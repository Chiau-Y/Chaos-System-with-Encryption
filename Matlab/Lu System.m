% ----------------------------------------------- %
% 使用混沌系統(Choas System)中的呂氏系統(Lu System) %
% 利用不同初始值，來創造兩個混沌系統 - Master和Slave %
% ----------------------------------------------- %

clc;clear;

k=100000;    % The number of data

% ====== Initial Setting ====== %
x1 = zeros(1,k);x2 = zeros(1,k);x3 = zeros(1,k);
y1 = zeros(1,k);y2 = zeros(1,k);y3 = zeros(1,k);

% ====== Initial conditions  ====== %
x1(1) = 4; x2(1) = 3; x3(1) = 2;    
y1(1) = 8; y2(1) = -1; y3(1) = 5;	

% ====== Iterations for Choas System  ====== %
for i=1:k-1   

    % ====== Master  ====== %
    x1(i+1) = 0.9822*x1(i) + 0.01793*x2(i) + (4.488e-06)*(-x1(i))*x3(i);
    x2(i+1) = 1.01*x2(i) + 0.0005025*(-x1(i))*x3(i);
    x3(i+1) = 0.9985*x3(i) + 0.0004996*x1(i)*x2(i);    
    
    % ====== Slave  ====== %
    y1(i+1) =  0.9822*y1(i) +0.01793*y2(i) + (4.488e-06)*(-y1(i))*y3(i);
    y2(i+1) = 1.01*y2(i) + 0.0005025 *(-y1(i))*y3(i);% + u(i);    % PID controller added in the Slave 
    y3(i+1) = 0.9985*y3(i) + 0.0004996*y1(i)*y2(i);

end

% ====== 奇異吸子圖  ====== %
subplot(2,1,1)
plot3(x3,x1,x2,'.');
xlabel('x3');ylabel('x2');zlabel('x1');
grid on
subplot(2,1,2)
plot3(y3,y1,y2,'.','Color',[1 0.5 0]);
xlabel('y3');ylabel('y2');zlabel('y1');
grid on
