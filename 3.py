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

#将C_p和m_p写作Cl[1]和m[1]
#将C_b和m_b写作Cl[2]和m[2]
#将C_e和m_e写作Cl[3]和m[3]
Cl=[0,]
m=[0,]
def cm(i,j):
    return -1*cl[i]*c[j]

#将k_p和A_p记作k[1]和A[1]
#将k_b和A_b记作k[2]和A[2]
#将k_e和A_e记作k[3]和A[3]
k=[0,]
A=[0,]
def katd(i,j,t): #计算k*A*T/d
    return k[i]*A[j]*t/d
#都是缩短行的大小用的辅助函数


def f(T,t,T_0):
    a=np.array([])
    P_cpu_dynamic=aerfa_1*(U_1**(2+mu_1))*b_1*lemda_1
    P_gpu_dynamic=aerfa_2*(U_2**(2+mu_2))*b_2*lemda_2

    P_static=P_cpu_dynamic + P_gpu_dynamic + U_1*I_gc + U_2*I_gg + P_net + P_camera + P_microphone

    #AI and IIFAI 都是引入的让代码看上去不那么一坨的辅助量      ，无实意
    AI=A[0]*(T_2**4)+A[1]*SOC*(T_2**3)+A[2]*SOC*SOC*(T_2**2)+A[3]*(SOC**3)*T_2+A[4]*(SOC**4)
    IIFAI=I*I*Fi_N*AI
    UI=U_s*I_s

    #I_gg:gpu的I_{gate}   I_gc:cpu的I_{gate}
    a=np.append(a,(IIFAi + C[1]*U[1]*(np.e**(C[2]/T[1]))*T[1]*T[1] + C[3]*U[2]*(np.e**(C[4]/T[1]))*T[1]*T[1] + k_0*(np.e**(E_a2/(KB*T_3)))*(1+(np.e**(-1*E_a2/(KB*T_3))))*(a_0+epsilon*L_0*np.sin(omega*t+Fi_0)+L_base)*a_ba + P_static )/(-1*C_N))
    a=np.append(katd(1,1,T[1]) - UI - katd(1,1,T[3]))/cm(1,1)
    a=np.append(a,(katd(2,2,T[2]) - IIFAI -katd(2,2,T[3]))/cm(2,2))
    a=np.append(a,(katd(3,3,T[2]) - IIFAI -katd(3,3,T_0) - UI)/cm(3,3))
    return a

#y0为四个数：SOC,T1,T2,T3
t=np.linspace(0,10000,100)
track=sp.odeint(f,[100,20+273,20+273,20+273],t,args=(293,))


plt.plot(t, track[0])
#plt.legend(loc='best')
#plt.xlabel('t')
plt.grid()
plt.show()