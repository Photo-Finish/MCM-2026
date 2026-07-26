import sys
from decimal import Decimal, getcontext

def main():
    # 设置高精度环境（可根据需要调整精度位数）
    getcontext().prec = 30  # 设置为30位精度
    
    # 物理常数定义（使用Decimal类型）
    M_Li = Decimal('6.94')        # 锂的摩尔质量 (g/mol)
    V = Decimal('2.5e-7')        # 体积 (m^3)
    U0 = Decimal('3.7')          # 参考电压 (V)
    E_std = Decimal('3.0401')    # 标准电势 (V)
    F = Decimal('96485')         # 法拉第常数 (C/mol)
    R = Decimal('8.314')         # 理想气体常数 (J/(mol·K))
    T = Decimal('298')           # 温度 (K)
    C_0 = Decimal('100')         # 初始容量 (mAh)
    m = Decimal('0.050')            # 初始质量 (g)
    
    # 定义常数
    QUARTER = Decimal('0.25')
    FIVE = Decimal('5')
    
    # 设置迭代次数
    N = 100
    
    # 初始化变量
    m_n_1 = m                # 上一轮质量
    C_n = C_0                # 当前容量
    
    # 打开文件准备写入结果
    with open('battery-loss-output-high-precision.csv', 'w') as f:
        # 写入CSV表头
        f.write("迭代次数,质量(g),r_plus系数,r_minus系数,容量(mAh)\n")
        
        # 主循环
        for i in range(1, N + 1):
            # 计算中间变量以提高性能
            exp_arg1 = -F * (U0 - E_std) / (QUARTER * R * T)
            exp_arg2 = -F * (FIVE - U0 + E_std) / (QUARTER * R * T)
            
            # 计算指数项
            term1 = M_Li * V / m_n_1
            term2 = Decimal.exp(exp_arg1)
            term3 = Decimal.exp(exp_arg2)
            
            # 计算两个衰减系数
            r_plus_n_1 = Decimal('1') - term1 * term2
            r_minus_n_1 = Decimal('1') - term1 * term3
            
            # 检查衰减系数是否合理（应介于0和1之间）
            if r_plus_n_1 <= Decimal('0') or r_minus_n_1 <= Decimal('0'):
                print(f"警告：第{i}次迭代中衰减系数变为非正数")
                print(f"r_plus_n_1 = {r_plus_n_1}")
                print(f"r_minus_n_1 = {r_minus_n_1}")
                print(f"term1 = {term1}, term2 = {term2}, term3 = {term3}")
                break
            
            # 计算新的质量和容量
            m_n = m_n_1 * r_plus_n_1 * r_minus_n_1
            C_n = C_n * r_plus_n_1 * r_minus_n_1
            
            # 写入当前迭代结果
            f.write(f"{i},{m_n:.12f},{r_plus_n_1:.12f},{r_minus_n_1:.12f},{C_n:.12f}\n")
            
            # 更新质量变量用于下一轮迭代
            m_n_1 = m_n
            
            # 进度提示
            if i % 10 == 0:
                print(f"已完成 {i}/{N} 次迭代...")
    
    print(f"\n高精度计算完成！")
    print(f"结果已保存到 'battery-loss-output-high-precision.csv'")
    print(f"最终质量: {m_n_1:.12f} g")
    print(f"最终容量: {C_n:.12f} mAh")
    print(f"容量保持率: {(C_n/C_0*100):.6f}%")

if __name__ == "__main__":
    main()