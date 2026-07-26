import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as sp
import matplotlib
matplotlib.use('TkAgg')    
# 科学常数
epsilon_0 = 3.0401  # Li的标准电池电势
R = 8.314  # 普适气体常数
F = 96485.33  # 法拉第常数

# 初始化变量（这里需要您根据实际情况设置这些值）
# /, SoC, Battery, Cover&Screen
# 热容和质量
Cl = [0, 800, 900, 700]  # J/(kg·K) - 假设值
m = [0, 0.1, 0.1, 0.1]  # kg - 假设值

# 热传导系数和面积
k = [0, 237, 401, 1.5]  # W/(m·K) - 假设值
A = [0, 0.012, 0.012, 0.024]  # m² - 假设值
d = 0.01  # 厚度 - 假设值

# 其他参数（需要您根据实际情况设置）
C = [0, 1e-6, 1000, 1e-5, 1000]  # 假设值
U = [0, 12, 15]  # 假设值
SOC = 0.8  # 初始SOC - 假设值
I = 2.0  # 电流 - 假设值
C_N = 10000  # 假设值


# 辅助函数
def cm(i, j):
    return -1 * Cl[i] * m[j]


def katd(i, j, T_val):
    return k[i] * A[j] * T_val / d


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

    # 这里需要您根据实际情况定义这些变量
    # 动态功耗参数（假设值）
    aerfa_1 = 0.5
    U_1 = 1.2
    mu_1 = 0.5
    b_1 = 1.0
    lemda_1 = 1.0
    aerfa_2 = 0.5
    U_2 = 1.5
    mu_2 = 0.5
    b_2 = 1.0
    lemda_2 = 1.0

    # 静态功耗（假设值）
    I_gc = 0.1
    I_gg = 0.1
    P_net = 0.5
    P_camera = 2
    P_microphone = 0.5
    P_speakers = 0.5

    # 计算动态功耗
    P_cpu_dynamic = aerfa_1 * (U_1 ** (2 + mu_1)) * b_1 * lemda_1
    P_gpu_dynamic = aerfa_2 * (U_2 ** (2 + mu_2)) * b_2 * lemda_2

    # 总静态功耗
    P_static = P_cpu_dynamic + P_gpu_dynamic + U_1 * I_gc + U_2 * I_gg + P_net + P_camera + P_microphone + P_speakers

    # AI相关参数（假设值）
    x = [0, 1e-3, 2e-3, 3e-3, 4e-3, 5e-3, 300, 25]
    Fi_N = 0.5
    U_s = 3.7
    I_s = 2.0

    # 电化学反应参数（假设值）
    k_0 = 1e-6
    E_a2 = 50000
    E_a1 = 30000
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

    # 四个微分方程
    # 1. SOC变化率
    a[0] = (IIFAI + C[1] * U[1] * (np.exp(C[2] / T_cpu_gpu)) * T_cpu_gpu ** 2 +
            C[3] * U[2] * (np.exp(C[4] / T_cpu_gpu)) * T_cpu_gpu ** 2 + P_static) / (-1 * C_N)
    print(a[0])

    # 2. CPU/GPU温度变化率
    a[1] = (katd(1, 1, T_cpu_gpu) - UI - katd(1, 1, T_screen)) / cm(1, 1)
    print(a[1])

    # 3. 电池温度变化率
    a[2] = (katd(2, 2, T_battery) - IIFAI - katd(2, 2, T_screen)) / cm(2, 2)
    print(a[2])

    # 4. 屏幕温度变化率
    a[3] = (katd(3, 3, T_screen) - IIFAI - katd(3, 3, T_0) - UI) / cm(3, 3)
    print(a[3])
    print()

    return a


# 初始条件: [SOC, T_cpu/gpu, T_battery, T_screen]
# SOC，温度用开尔文
y0 = [1, 20 + 273, 20 + 273, 20 + 273]

# 时间点
t = np.linspace(0, 300, 1000)

# 环境温度（293K = 20°C）


# 解微分方程
track = sp.odeint(f, y0, t, args=(293,))

# 绘制结果
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(t, track[:, 0])
plt.title('SOC vs Time')
plt.xlabel('Time (s)')
plt.ylabel('SOC')
plt.grid(True)

plt.subplot(2, 2, 2)
plt.plot(t, track[:, 1] - 273)  # 转换为摄氏度
plt.title('CPU/GPU Temperature vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(t, track[:, 2] - 273)  # 转换为摄氏度
plt.title('Battery Temperature vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(t, track[:, 3] - 273)  # 转换为摄氏度
plt.title('Screen Temperature vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.grid(True)

plt.tight_layout()
plt.show()      #这是代码，让ai重写了plt部分和把数组中的数改成角标形式。数据是乱来的