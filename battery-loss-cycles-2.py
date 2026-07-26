import csv

r = 1.0  # 初始容量比例
with open('capacity_decay.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 写入表头
    writer.writerow(['Cycle', 'Remaining_Percentage'])
    
    for i in range(1, 101):
        r *= 0.9971793207
        # 写入每一行数据
        writer.writerow([i, f'{r*100:.6f}'])

print("数据已保存到 capacity_decay.csv")