import numpy as np

def dist_ave(FEATURE_FI_1, FEATURE_FI_2, N):
    """
    Args:
        FEATURE_FI_1 ([list]): [句子的特徵向量]
        FEATURE_FI_2 ([list]): [句子的特徵向量]
        N ([int]): [特徵向量長度，其值由關鍵字個數決定]
    
    Returns:
        result : 數字
        
    此函式計算兩個句子的特徵向量的距離，距離定法為次數方相減的平方和 + 相對位置方先取平均，再相減的平方和
    """
    # 次數方的初始值
    x = 0
    # 相對位置方的初始值
    y = 0
    # 距離初始值
    result = 0
    
    # 次數相減的平方和 + 相對位置先取平均，再相減的平方和
    for i in range(N):
        x = x + (FEATURE_FI_1[i][0] - FEATURE_FI_2[i][0]) ** 2
        y = y + (sum(FEATURE_FI_1[i][1])/len(FEATURE_FI_1[i][1]) - sum(FEATURE_FI_2[i][1])/len(FEATURE_FI_2[i][1])) ** 2

    result = x + y
    return result

def kNNmodel(unknown_dist_list, type_list, k):
    # list to array
    unknown_dist_array = np.array(unknown_dist_list)
    # find the k smallest numbers in the array
    idx = np.argpartition(unknown_dist_array, k)
    # 取得type_list上對應的類別
    temp = []
    for ind in idx[:k]:
        temp.append(type_list[ind])
    
    # find the most common element in temp
    most_common = max(temp, key = temp.count)
    
    return most_common