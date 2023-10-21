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


def equalwidth(Class, class_index):
    
    interval_width = (max(Class) - min(Class)) / 10
    # 計算各個splitting points包含max, min
    Splitting_point = [min(Class) + i * interval_width for i in range(11)]
    Splitting_str = ["{:.4f}".format(num) for num in Splitting_point] # 調整浮點數顯示位數
        
    discretized_class = []

    # Perform equal width discretization
    for value in Class:
        for i in range(10):
            if Splitting_point[i] <= value < Splitting_point[i + 1]:
                discretized_class.append(i + 1)
            if value == max(Class):
                discretized_class.append(10)
                break
    class_name = column_names[Attributes[class_index]+1]  # 获取类别名称
    print(f"Splitting Points(include Max. and Min.) for {class_name}: {Splitting_str}")

    return discretized_class

def equalfrequency(Class, class_index):
    # 计算每个箱的数据点数量
    interval_freq = len(Class) // 10
    bin_sizes = [interval_freq] * 10
    Sorted_class = sorted(Class)

    # 处理余数，以确保每个箱中的数据点数量相等
    remainder = len(Class) % 10
    for i in range(remainder):
        bin_sizes[i] += 1

    # 计算分箱点
    Splitting_point = [0]
    for size in bin_sizes:
        next_point = Splitting_point[-1] + size
        Splitting_point.append(next_point)

    # 转换为浮点数以适应小数位数格式化
    # Splitting_point = [float(point) for point in Splitting_point]

    # Splitting_str = [str(num) for num in Splitting_point]  # 调整浮点数显示位数

    Splitting_intervals = []
    # for value in  Sorted_class:
    for i in Splitting_point[:10]:
        Splitting_intervals.append(Sorted_class[i])
    Splitting_intervals.append(Sorted_class[213])
    # 执行等频分箱
    discretized_class = []

    for value in Class:
        # for i in range(10):
        #     if Splitting_intervals[i] <= value < Splitting_intervals[i + 1]:
        for j in range(10):
            if Splitting_point[j] <= Sorted_class.index(value) < Splitting_point[j+1]:
                 discretized_class.append(j + 1)
            if value == max(Class):
                discretized_class.append(10)
                break

    # Splitting_str = []
    # for i in Splitting_point:
    #     Splitting_str.append(discretized_class[i])
    Splitting_str = ["{:.4f}".format(num) for num in Splitting_intervals] # 調整浮點數顯示位數
    class_name = column_names[Attributes[class_index] + 1]  # 获取类别名称
    print(f"Splitting Points(include Max. and Min.) for {class_name}:\n{Splitting_str}")

    return discretized_class



print("\nRun Equal Frequency:\n")
# 创建一个字典来存储每个属性的分箱结果
discretized_row = []
discr_equ_data = []  #EquWid後的資料，List包含Dict裡面的value為str

# 循环处理每个属性
for class_selected in Attributes:  # 跳过第一个和最后一个列名
    valuesTodis = [float(row[class_selected]) for row in raw_data]
    discr_freq_values = equalfrequency(valuesTodis, class_selected)  #執行EquWid

    discr_freq_str = []
    for value in discr_freq_values:
        str_value = str(value)
        discr_freq_str.append(str_value)

    discretized_row.append(discr_freq_str)

for values in zip(*discretized_row):
    discretized_dict = {key: value for key, value in zip(Attributes, values)}
    discr_equ_data.append(discretized_dict)



def probability(data):   #計算類別資料發生率公式
    total_samples = len(data)
    value_counts = {}
   
    for value in data:
        if value in value_counts:
            value_counts[value] += 1
        else:
            value_counts[value] = 1

    prob = {key: value / total_samples for key, value in value_counts.items()}

    return prob

def H_entropy(data):   # 計算Entropye公式_H(X),H(Y)
    # entropy_value = -sum(p * math.log2(p) for p in probability(data).values())
    probs = probability(data)
    probs_values = [prob[1] for prob in probs.items()] # 抽出字典value到list中，[0]是key [1]是value


    entropy_value = -sum(p * math.log2(p) for p in probs_values)
    return entropy_value

def Hxy_entropy(class1, class2):   #計算Entropye公式_H(X,Y)
    Hxy_data = list(zip(class1, class2))
    Hxy_prob = probability(Hxy_data)
    Hxy_entropy = -sum(p * math.log2(p) for p in Hxy_prob.values())
    return Hxy_entropy

def sym_uncert(p_x, p_y):   #計算symmetric_uncertainty公式_U(X,Y)
    h_x = H_entropy(p_x)
    h_y = H_entropy(p_y)
    h_xy = Hxy_entropy(p_x,p_y)

    Uxy = 2 * (h_x + h_y - h_xy) / (h_x + h_y)
    return Uxy

def sym_uncertC(p_x):   #計算symmetric_uncertainty公式_U(X,C)
    #Ground_tru = [G["Class"]for G in data ]   #Ground_truth
    h_x = H_entropy(p_x)
    h_C = H_entropy(Ground_tru)
    h_xC = Hxy_entropy(p_x,Ground_tru)

    Uxy = 2 * (h_x + h_C - h_xC) / (h_x + h_C)
    return Uxy

def Goodness(class1,selected_f):   #只輸入一個變數，把遠本
    num = 0   #分子計數
    den = 0   #分母計數
    
    # 計算分子：對已選特徵套用sym_uncertC函數的結果相加
    for feature_index in range(len(selected_f)):
        feature = Attributes.index(feature_index)
        num += sym_uncertC(class1[feature])

    # 計算分母：對已選特徵兩兩組合套用sym_uncert函數的結果相加
    if len(selected_f) ==1:
        den += 1
    else:
        for i in range(len(selected_f)):
            for j in range(len(selected_f)):
                # feature_index1 = selected_f[i]
                # feature_index2 = selected_f[j]
                # den += sym_uncert(class1[feature_index1], class1[feature_index2])
                den += sym_uncert(class1[i], class1[j])

    if den == 0:
        Gn = 0
    else:
        Gn = num / math.sqrt(den)
    return Gn


#**************************
#**************************
#**************************
#**************************
#**************************
fwd_selected_features = []
fwd_best_goodness = 0.0
while True:  # while迴圈須設定statement，for迴圈跑完全部資料後自動結束
    feature_to_add = None
    best_feature_goodness = 0.0

    for feature in Attributes:
        all_value = []
        for value in raw_data:
            all_value.append(value[feature]) #逐步把每比資料對應的特徵值加到all_features
        
        Sorted_conut = 1
        Sorted_value = sorted(all_value)
        Splitting_value = [Sorted_value[0]]
        Splitting_point = [0]
        better_gain = 0
        for j in range(Sorted_conut):
            if j == 0:
                for i in range(len(Sorted_value)):
                    S1 = Sorted_value[:i]
                    S2 = Sorted_value[i:]
                    X = (len(S1)/len(Sorted_value)) * H_entropy(S1)
                    Y = (len(S2)/len(Sorted_value)) * H_entropy(S2)
                    Gain = H_entropy(Sorted_value) - (X + Y)
                    if Gain > better_gain:
                        better_gain = Gain
                        Splitting_value.append(Sorted_value[i])
                        Splitting_point.append(i)
                        Sorted_conut += 1
                

            # else:
            #     for k in range(Sorted_conut - 1):
            #         for l in range(len(Sorted_value)):
            #         S1 = Sorted_value[]


                


            Splitting_interavls.append(max(Sorted_value))

            # 計算Goodness值
        goodness = Goodness(candidate_features, features_to_try)

            # 如果Goodness值更高，則更新候選特徵和Goodness指標
        if goodness > best_feature_goodness:
                best_feature_goodness = goodness
                feature_to_add = feature_index


    # 如果沒有更好的特徵可添加，則退出循環
    # if feature_to_add is None:
    if best_feature_goodness < fwd_best_goodness:
            break

    # 添加最佳特徵的索引到已選特徵中，並更新Goodness指標
    fwd_selected_features.append(feature_to_add)
    fwd_best_goodness = best_feature_goodness

    # 從所有特徵索引中刪除已選擇的特徵
    #Attributes.remove(feature_to_add)

      # 輸出已選特徵和Goodness值，使用列名而不是索引
    selected_feature_names = [column_names[i +1] for i in fwd_selected_features]
    print(f"Selected Features: {selected_feature_names}") #加入f可以表達式，print出{}內的值
    print(f"Best Goodness: {fwd_best_goodness:.4f}")

#**************************
#**************************
#**************************
#**************************
#**************************
