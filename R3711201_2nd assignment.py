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

# 创建一个字典来存储每个属性的分箱结果
discretized_row = []
discr_wid_data = []  #EquWid後的資料，List包含Dict裡面的value為str

# 循环处理每个属性
for class_selected in Attributes:  # 跳过第一个和最后一个列名
    valuesTodis = [float(row[class_selected]) for row in raw_data]
    discr_wid_values = equalwidth(valuesTodis, class_selected)  #執行EquWid

    discr_wid_str = []
    for value in discr_wid_values:
        str_value = str(value)
        discr_wid_str.append(str_value)

    discretized_row.append(discr_wid_str)

for values in zip(*discretized_row):
    discretized_dict = {key: value for key, value in zip(Attributes, values)}
    discr_wid_data.append(discretized_dict)

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
    probs = probability(data)
    probs_values = [prob[1] for prob in probs.items()]


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
    h_x = H_entropy(p_x)
    h_C = H_entropy(Ground_tru)
    h_xC = Hxy_entropy(p_x,Ground_tru)

    Uxy = 2 * (h_x + h_C - h_xC) / (h_x + h_C)
    return Uxy

def Goodness(class1,selected_f):
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
                den += sym_uncert(class1[i], class1[j])

    if den == 0:
        Gn = 0
    else:
        Gn = num / math.sqrt(den)
    return Gn

# 初始化已選Attributes和Goodness值
fwd_selected_features = []
fwd_best_goodness = 0.0

print("\n開始 Forward Feature Selection\n")

while True:
    feature_to_add = None
    best_feature_goodness = 0.0

    for feature_index in range(len(Attributes)):
        if feature_index not in fwd_selected_features:
            # 複製已選Attributes列表，並加入候選Attributes
            features_to_try = fwd_selected_features.copy()
            features_to_try.append(Attributes[feature_index])

            # 提取候選Attributes
            candidate_features = []
            for feature in features_to_try:
                all_feature = []
                for sample in discr_wid_data:
                    select_raw_data = sample[feature]
                    all_feature.append(select_raw_data)
                candidate_features.append(all_feature)

            # 計算Goodness值
            goodness = Goodness(candidate_features, features_to_try)

            # 如果Goodness值更高，則更新候選Attributes和Goodness值
            if goodness > best_feature_goodness:
                best_feature_goodness = goodness
                feature_to_add = feature_index


    # 如果沒有更好的Attributes可加入，則退出迴圈
    if best_feature_goodness < fwd_best_goodness:
            break

    # 增加最佳Attributes到已選Atttibutes中，並更新Goodness值
    fwd_selected_features.append(feature_to_add)
    fwd_best_goodness = best_feature_goodness


    # 輸出已選Attributes subset和Goodness值
    selected_feature_names = [column_names[i +1] for i in fwd_selected_features]
    print(f"Selected Features: {selected_feature_names}")
    print(f"Best Goodness: {fwd_best_goodness:.4f}")

print("\nForward Feature Selection完成。最佳特徵列名:\n", selected_feature_names)


# 初始化已選Attirbutes和Goodness值
bwd_selected_features = list(range(len(Attributes)))
bwd_best_goodness = 0.0

print("\n開始 Backward Feature Selection\n")
while True:
    feature_to_remove = None
    best_feature_goodness = 0.0

    for feature_index in bwd_selected_features:
        # 複製已選Attributes列表，並刪除候選Attributes
        features_to_try = bwd_selected_features.copy()
        features_to_try.remove(feature_index)

        # 提取候選Attributes
        candidate_features = []
        for feature in features_to_try:
            all_feature = []
            for sample in discr_wid_data:
                select_raw_data = sample[feature]
                all_feature.append(select_raw_data)
            candidate_features.append(all_feature)

        # 計算Goodness值
        goodness = Goodness(candidate_features, features_to_try)

        # 如果Goodness值更高，則更新候選Attributes和Goodness值
        if goodness > best_feature_goodness:
            best_feature_goodness = goodness
            feature_to_remove = feature_index
            


    # 如果没有更差的Attributes可以刪除，則退出迴圈
    if bwd_best_goodness >= best_feature_goodness:
        
        break

    # 增加最差的Attributes到已選Attributes中，並更新Goodness值
    bwd_selected_features.remove(feature_to_remove)
    bwd_best_goodness = best_feature_goodness

    selected_feature_names = [column_names[i + 1] for i in bwd_selected_features]
    print(f"Selected Features: {selected_feature_names}")
    print(f"Best Goodness: {bwd_best_goodness:.4f}")


print("\nBackward Feature Selection完成。最佳特徵列名:\n", selected_feature_names)