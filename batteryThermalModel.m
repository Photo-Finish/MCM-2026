function batteryThermalModel()
    % 科学常数
    KB = 1.380649e-23;
    
    % 热容和质量
    Cl = [0, 4180, 900, 700];  % J/(kg·K)
    m = [0, 0.005, 0.06, 0.12];  % kg
    
    % 热传导系数和面积
    k = [0, 2/2, 5/2, 0.6/2];  % W/(m*K)
    A = [0, 1.2e-4, 2*0.00175, 2*74.8*158.6e-6];  % m²
    d = [0, 0.0005, 0.005, 0.005];
    
    % 其他参数
    C = [0, 0.2550, -3740, 0.2561, -3740];
    U = [0, 1.2, 1];
    SOC0 = 1;  % 初始SOC
    I = 0.5;  % 电流
    C_N = 50000;
    
    a_0a_R = 242.3180;
    a_0a_G = 293.6999;
    a_0a_B = 294.0139;
    
    % 辅助函数
    cm = @(i, j) -1 * Cl(i) * m(j);
    
    katd = @(i, j, T_val, kp) k(i) * A(j) * T_val / d(kp);
    
    % 微分方程函数
    function dTdt = odeSystem(t, T, T_0)
        % T: [SOC; T_cpu/gpu; T_battery; T_screen]
        % T_0: 环境温度
        
        % 初始化返回数组
        dTdt = zeros(4, 1);
        
        % 提取状态变量
        T_soc = T(1);
        T_cpu_gpu = T(2);
        T_battery = T(3);
        T_screen = T(4);
        
        % 活化能
        E_a2 = 0.2 * 1.602176634e-19;
        E_a1 = 0.7 * 1.602176634e-19;
        
        % 动态功耗参数
        aerfa_1 = 0.5;
        U_1 = 1.2;
        mu_1 = 1;
        b_1 = 1.0;
        lemda_1 = 2;
        aerfa_2 = 0.5;
        U_2 = 1;
        mu_2 = 1;
        b_2 = 1.0;
        lemda_2 = 5/2;
        
        % 静态功耗
        I_gc = 1e-7;
        I_gg = 8.6e-8;
        P_net = 0.2;
        P_camera = 0.2;
        P_microphone = 0.1;
        P_speakers = 0.3;
        
        % 计算动态功耗
        P_cpu_dynamic = aerfa_1 * (U_1 ^ (2 + mu_1)) * b_1 * lemda_1;
        P_gpu_dynamic = aerfa_2 * (U_2 ^ (2 + mu_2)) * b_2 * lemda_2;
        
        % 屏幕功耗参数
        a_R = 3.3996;
        a_G = 7.0503;
        a_B = 19.5081;
        Br = 75; % 固定值
        P_R = 100;
        P_G = 100;
        P_B = 100;
        
        % 计算屏幕功耗
        P_screen = (exp(E_a1 / (KB * T_screen)) * (exp(-1 * E_a2 / (KB * T_screen)) + 1)) / ...
                   (exp(E_a1 / (KB * 293.16)) * (1 + exp(-1 * E_a2 / (KB * 293.16))));
        P_screen = P_screen * (a_0a_R * P_R + a_0a_G * P_G + a_0a_B * P_B + ...
                   Br * (a_R * P_R + a_G * P_G + a_B * P_B));
        P_screen = P_screen * 1e-6;
        
        % 总静态功耗
        P_static = P_cpu_dynamic + P_gpu_dynamic + U_1 * I_gc + U_2 * I_gg + ...
                   P_net + P_camera + P_microphone + P_speakers;
        
        % AI相关参数
        x = [0, 4.8347, -0.2437, -0.3751, -0.1628, 6.0577, 2.6921, -0.8159]; % 0.75C
        
        Fi_N = 0.5;
        U_s = 3.7;
        I_s = 2.0;
        
        % 计算AI项
        AI = (x(2) + x(3) * T_soc + x(4) * (T_soc ^ 2) + x(5) * (T_soc ^ 3)) * ...
             x(6) * (exp(x(7) / (T_screen + x(8))));
        IIFAI = I * I * Fi_N * AI;
        UI = U_s * I_s;
        
        % 四个微分方程
        % 1. SOC变化率
        dTdt(1) = (IIFAI + C(2) * U(2) * exp(C(3) / T_cpu_gpu) * T_cpu_gpu^2 + ...
                  P_screen + C(4) * U(3) * exp(C(5) / T_cpu_gpu) * T_cpu_gpu^2 + ...
                  P_static) / (-1 * C_N);
        
        % 2. CPU/GPU温度变化率
        dTdt(2) = (katd(2, 2, T_cpu_gpu, 2) - UI - katd(2, 2, T_screen, 2)) / cm(2, 2);
        
        % 3. 电池温度变化率
        dTdt(3) = (katd(3, 3, T_battery, 3) - IIFAI - katd(3, 3, T_screen, 3)) / cm(3, 3);
        
        % 4. 屏幕温度变化率
        dTdt(4) = (katd(4, 4, T_screen, 4) - IIFAI - katd(4, 4, T_0, 4) - UI) / cm(4, 4);
    end

    % 初始条件: [SOC; T_cpu/gpu; T_battery; T_screen] (开尔文温度)
    y0 = [SOC0; 20 + 273.16; 20 + 273.16; 20 + 273.16];
    
    % 时间范围
    tspan = [0, 7000];
    
    % 环境温度 (293.16K = 20°C)
    T_0 = 293.16;
    
    % 解微分方程
    options = odeset('RelTol', 1e-6, 'AbsTol', 1e-9);
    [t, y] = ode45(@(t, y) odeSystem(t, y, T_0), tspan, y0, options);
    
    % 提取结果
    SOC = y(:, 1);
    T_cpu_gpu = y(:, 2) - 273.16;  % 转换为摄氏度
    T_battery = y(:, 3) - 273.16;  % 转换为摄氏度
    T_screen = y(:, 4) - 273.16;   % 转换为摄氏度
    
    % 绘制结果
    figure('Position', [100, 100, 1200, 800]);
    
    % SOC随时间变化
    subplot(2, 2, 1);
    plot(t, SOC, 'b-', 'LineWidth', 1.5);
    xlabel('Time (s)');
    ylabel('SOC');
    title('SOC vs Time');
    grid on;
    
    % CPU/GPU温度随时间变化
    subplot(2, 2, 2);
    plot(t, T_cpu_gpu, 'r-', 'LineWidth', 1.5);
    xlabel('Time (s)');
    ylabel('Temperature (°C)');
    title('CPU/GPU Temperature vs Time');
    grid on;

    % 电池温度随时间变化
    subplot(2, 2, 3);
    plot(t, T_battery, 'g-', 'LineWidth', 1.5);
    xlabel('Time (s)');
    ylabel('Temperature (°C)');
    title('Battery Temperature vs Time');
    grid on;    
    % 屏幕温度随时间变化
    subplot(2, 2, 4);
    plot(t, T_screen, 'm-', 'LineWidth', 1.5);
    xlabel('Time (s)');
    ylabel('Temperature (°C)');
    title('Screen Temperature vs Time');
    grid on;

    % 调整子图间距
    sgtitle('Battery Thermal Model Simulation');



end