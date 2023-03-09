clear;clc;close all;
rho = 1025;
a = 2;
g = 9.8;
omega = 1.047
Vg = g/(2*omega);
k = (omega^2)/g;

zs = linspace(-a,0,500);
a33 = @(z) pi*rho*(a.^2 - z.^2);
A33 = integral(a33,-a,0)
C33 = rho*g*pi*a^2
F3 = rho*g*pi*a^2
B33 = k/(4*rho*g*Vg)*(88000)^2
