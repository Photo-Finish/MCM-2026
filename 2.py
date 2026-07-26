import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as sp
import matplotlib
matplotlib.use('TkAgg')
#科学常数
KB=1.380649e-23  #玻尔兹曼常数
epsilon_0=3.0401   #Li的标准电池电势
R=8.314        #普适气体常数
F=96485.33      #法拉第常数
#e写作np.e
#定义

        #t单位为秒
def f(T,t,T_0):
    a=np.array([])
    P_static=aerfa_1*(U_1**(2+mu_1))*b_1*lemda_1 + aerfa_2*(U_2**(2+mu_2))*b_2*lemda_2 + U_1*I_gc + U_2*I_gg + P_net + P_camera + P_microphone  #                                       #
    a=np.append(a,(I*I*Fi_N* (A[0]*(T_2**4)+A[1]*SOC*(T_2**3)+A[2]*SOC*SOC*(T_2**2)+A[3]*(SOC**3)*T_2+A[4]*(SOC**4)) + C_1*U_1*(np.e**(C_2/T_1))*T_1*T_1 + C_3*U_2*(np.e**(C_4/T_1))*T_1*T_1 + k_0*(np.e**(E_a2/(KB*T_3)))*(1+(np.e**(-1*E_a2/(KB*T_3))))*(a_0+epsilon*L_0*np.sin(omega*t+Fi_0)+L_base)*a_ba + P_static )/(-1*C_N))
    a=np.append((a,k_p*A_p*T[3]/d + U_s*I_s - k_p*A_p*T[1]/d )/(C_p*m_p))
    a=np.append(a,(k_b*A_b*T[2]/d - I*I*Fi_N* (A[0]*(T_2**4)+A[1]*SOC*(T_2**3)+A[2]*SOC*SOC*(T_2**2)+A[3]*(SOC**3)*T_2+A[4]*(SOC**4)) -k_b*A_b*T_3/d)/(-1*C_b*m_b))
    a=np.append(a,(k_e*A_e*T[2]/d - I*I*Fi_N* (A[0]*(T_2**4)+A[1]*SOC*(T_2**3)+A[2]*SOC*SOC*(T_2**2)+A[3]*(SOC**3)*T_2+A[4]*(SOC**4)) -k_e*A_e*T_0/d -U_s*I_s)/(-1*C_e*m_e))


    return a

#y0为四个数：SOC,T1,T2,T3
t=np.linspace(0,10000,100)
track=sp.odeint(f,[100,20+273,20+273,20+273],t,args=(293,))


plt.plot(t, track[0])
#plt.legend(loc='best')
#plt.xlabel('t')
plt.grid()
plt.show()