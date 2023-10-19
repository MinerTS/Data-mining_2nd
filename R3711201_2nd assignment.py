import math

with open('作業/第二次/glass.txt', 'r') as file:
    lines = file.readlines()
# 自定義column name
column_names = ['Id number', 'RI', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ba', 'Fe','Type of glass']
Attributes = [0,1,2,3,4,5,6,7,8]
# 初始化字典
raw_data = []
Ground_tru = []

for line in lines:
    row = line.strip().split(',')
    Ground_tru.append(row.pop(10))
    if len(row) == len(Attributes)+1:
            instance = dict(zip(Attributes, row[1:]))
            raw_data.append(instance)


def equalwidth(Class):
    
    interval_width = (max(Class) - min(Class)) / 10
    # 計算各個splitting points包含max, min
    Splitting_point = [min(Class) + i * interval_width for i in range(11)]
    discretized_class = []

    # Perform equal width discretization
    for value in Class:
        for i in range(10):
            if Splitting_point[i] <= value < Splitting_point[i + 1]:
                discretized_class.append(i + 1)
            if value == max(Class):
                discretized_class.append(10)
                break
    return discretized_class


# 创建一个字典来存储每个属性的分箱结果
discretized_row = []
discretized_data = []

# 循环处理每个属性
for class_selected in Attributes:  # 跳过第一个和最后一个列名
    valuesTodis = [float(row[class_selected]) for row in raw_data]
    discretized_values = equalwidth(valuesTodis)
    discretized_str = []
    for value in discretized_values:
        str_value = str(value)
        discretized_str.append(str_value)

    discretized_row.append(discretized_str)

for values in zip(*discretized_row):
    discretized_dict = {key: value for key, value in zip(Attributes, values)}
    discretized_data.append(discretized_dict)

# for i in discretized_data:
#     for j in range(Attributes):
#         discretized_data[i][j] = str(discretized_data[i][j])

print(discretized_data)