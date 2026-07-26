import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as sp
import matplotlib
matplotlib.use('TkAgg')
# 科学常数
KB=1.380649e-23
epsilon_0 = 3.0401  # Li的标准电池电势
#R = 8.314  # 普适气体常数
#F = 96485.33  # 法拉第常数

# 初始化变量（这里需要您根据实际情况设置这些值）
# 热容和质量
Cl = [0, 4180, 900, 700]  # J/(kg·K) - 假设值
m = [0, 0.005, 0.06, 0.12]  # kg - 假设值

# 热传导系数和面积
k = [0,2/2,5/2,0.6/2]  # W/(m*K) - 假设值    1：0.8~1.05    #考虑到了热传导不是完全传导，它只有50%传出了
A = [0, 1.2e-4, 2*0.00175, 2*74.8*158.6e-6]  # m² - 假设值
d = [0, 0.0005 , 0.005 ,0.005]  #

# 其他参数（需要您根据实际情况设置）
C = [0, 0.2550, -3740, 0.2561, -3740]  # 假设值
U = [0, 1.2, 1]  # 假设值
SOC = 1  # 初始SOC - 假设值
I = 0.5  # 电流 - 假设值
C_N = 50000  # 假设值

a_0a_R=242.3180
a_0a_G=293.6999
a_0a_B=294.0139# 辅助函数
def cm(i, j):
    return -1 * Cl[i] * m[j]


def katd(i, j, T_val, kp):
    return k[i] * A[j] * T_val / d[kp]


def f(T, t, T_0):
    """
    T: [SOC, T_cpu/gpu, T_battery, T_screen]
    t: 时间
    T_0: 环境温度
    """
    # 初始化返回数组
    a = np.zeros(4)

    # 提取温度
    T_soc, T_cpu_gpu, T_battery, T_screen = T

    E_a2 = 0.2*1.602176634e-19
    E_a1 = 0.7*1.602176634e-19
    # 这里需要您根据实际情况定义这些变量
    # 动态功耗参数（假设值）
    aerfa_1 = 0.5
    U_1 = 1.2
    mu_1 = 1
    b_1 = 1.0
    lemda_1 = 2
    aerfa_2 = 0.5
    U_2 = 1
    mu_2 = 1
    b_2 = 1.0
    lemda_2 = 5/2

    # 静态功耗（假设值）
    I_gc = 1e-7
    I_gg = 8.6e-8
    P_net = 0.2
    P_camera = 0.2
    P_microphone = 0.1
    P_speakers = 0.3

    # 计算动态功耗
    P_cpu_dynamic = aerfa_1 * (U_1 ** (2 + mu_1)) * b_1 * lemda_1
    P_gpu_dynamic = aerfa_2 * (U_2 ** (2 + mu_2)) * b_2 * lemda_2
    print(P_cpu_dynamic, P_gpu_dynamic)

    '''P_R=random.randint(1,255)
    P_G=random.randint(1,255)
    P_B=random.randint(1,255)'''
    a_R=3.3996
    a_G=7.0503
    a_B=19.5081
    Br =random.randint(0,100)
    P_R=P_B=P_G=100
    Br=75
    P_screen = (np.exp(E_a1 / (KB*T[3])) * (np.exp(-1*E_a2/(KB*T[3]))+1)) / (np.exp(E_a1/(KB*293.16)) * (1+np.exp(-1*E_a2/(KB*293.16))))
    print('p1',P_screen)
    P_screen*=(a_0a_R*P_R + a_0a_G*P_G + a_0a_B*P_B + Br*(a_R*P_R+a_G*P_G+a_B*P_B))

    P_screen*=1e-6

    #
    P_static = P_cpu_dynamic + P_gpu_dynamic + U_1 * I_gc + U_2 * I_gg + P_net + P_camera + P_microphone + P_speakers
    print('P_static',P_static)

    # AI相关参数（假设值）
    x = [0, 4.8347, -0.2437, -0.3751, -0.1628, 6.0577, 2.6921, -0.8159] #0.75C
    #x = [0, 4.2362, -0.2760, -0.6248, -0.0240, 19.0968,2.7253,  0.1822] #1.75C
    #x = [0, 3.3824, -1.0973, -0.3668,  0.7126, 23.5287,2.6668,  0.0940] #2.75C

    Fi_N = 0.5
    U_s = 3.7
    I_s = 2.0

    # 电化学反应参数（假设值）
    k_0 = 1e-6

    a_0 = 1.0
    epsilon = 0.1
    L_0 = 0.01
    omega = 0.0001
    Fi_0 = 0.0
    L_base = 0.01
    a_ba = 1.0

    # 计算AI项
    AI = (x[1] + x[2] * T_soc + x[3] * (T_soc ** 2) + x[4] * (T_soc ** 3)) * x[5] * (np.exp(x[6] / (T_screen + x[7])))
    IIFAI = I * I * Fi_N * AI
    UI = U_s * I_s
    print('IIFAI',IIFAI)

    # 四个微分方程
    # 1. SOC变化率
    a[0] = (IIFAI + C[1] * U[1] * (np.exp(C[2] / T_cpu_gpu)) * T_cpu_gpu ** 2 + P_screen +
            C[3] * U[2] * (np.exp(C[4] / T_cpu_gpu)) * T_cpu_gpu ** 2 + P_static) / (-1 * C_N)
    #print(k_0 * (np.exp(E_a1 / (KB * T_battery))) * (1 + (np.exp(-1 * E_a2 / (KB * T_battery)))) * (a_0a_R+a_0a_G+a_0a_B + (epsilon * L_0 * np.sin(omega * t + Fi_0) + L_base) * a_ba))
    print(a[0])
    print('一坨',C[1] * U[1] * (np.exp(C[2] / T_cpu_gpu)) * T_cpu_gpu ** 2   )

    # 2. CPU/GPU温度变化率
    a[1] = (katd(1, 1, T_cpu_gpu,1) - UI - katd(1, 1, T_screen,1)) / cm(1, 1)
    print(a[1])

    # 3. 电池温度变化率
    a[2] = (katd(2, 2, T_battery,2) - IIFAI - katd(2, 2, T_screen,2)) / cm(2, 2)
    print(a[2])

    # 4. 屏幕温度变化率
    a[3] = (katd(3, 3, T_screen,3) - IIFAI - katd(3, 3, T_0,3) - UI) / cm(3, 3)
    print(a[3])
    return a

    print()


# 初始条件: [SOC, T_cpu/gpu, T_battery, T_screen]
# SOC，温度用开尔文
y0 = [1, 20 + 273.16, 20 + 273.16, 20 + 273.16]

# 时间点
t = np.linspace(0, 7000, 1000)

# 环境温度（293K = 20°C）


# 解微分方程
track = sp.odeint(f, y0, t, args=(293.16,))

# 绘制结果
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(t, track[:, 0])
plt.title('SOC / Time')
plt.xlabel('Time (s)')
plt.ylabel('SOC')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(t, track[:, 1] - 273.16)  # 转换为摄氏度
plt.title('CPU/GPU Temperature / Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(t, track[:, 2] - 273.16)  # 转换为摄氏度
plt.title('Battery Temperature / Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(t, track[:, 3] - 273.16)  # 转换为摄氏度
plt.title('Screen Temperature / Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(True)

plt.tight_layout()
plt.show()