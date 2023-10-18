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
    discretized_data = []

    # Perform equal width discretization
    for value in Class:
        for i in range(10):
            # if value == max(Class):
            #      discretized_data.append(10)
            if Splitting_point[i] <= value < Splitting_point[i + 1]:
                discretized_data.append(i + 1)
                break

    return discretized_data

# 创建一个字典来存储每个属性的分箱结果
discretized_data = {}

# 循环处理每个属性
for class_value in Attributes:  # 跳过第一个和最后一个列名
    values = [float(row[class_value]) for row in raw_data]
    discretized_values = equalwidth(values)
    discretized_data[class_value] = discretized_values

# 打印每个属性的宽度分箱结果
for attribute, discretized_values in discretized_data.items():
    print(f"{attribute} 的等宽分箱结果：{discretized_values}")


# while True:
#     class_to_dis = []
#     for i in range(10)
#     class_values = [row["RI"] for row in raw_data]
#     for sample_class in raw_data: #增強for循環，逐步抽出raw_data的每個比資料，全部抽完結束回圈
#                     # select_raw_data = sample[feature]
#         class_to_dis.append(sample_class[1] for sample_class in raw_data.items()) #逐步把每比資料對應的特徵值加到all_features
#                 # candidate_features.append(all_feature) #把all_features的資料加到condidate_features

# class_values = [prob[1] for prob in probs.items()] # 抽出字典value到list中，[0]是key [1]是value