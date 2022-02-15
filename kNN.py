from matplotlib import transforms
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
    """[summary]
    用kNN的概念來做分類
    Args:
        unknown_dist_list ([list]): [欲分類資料與全體資料的距離列表]
        type_list ([list]): [全體資料的繪圖項目列表]
        k ([type]): [kNN的k]

    Returns:
        [string]: [用kNN分類，得到的繪圖項目]
    """
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


def metric4kNNmodel(confusion_mat):
    """summary
    Calculate performance of kNN model.
    Including:
    Accuracy
    Precision
    Sensitivity(TPR)
    Specificity(TNR)
    FPR
    FNR
    ================
    variable:
    confusion_matrix: [ndarray] confusion matrix of kNNmodel
    
    return:
    metrics: [array] containing Accuracy, TPR, FPR, TNR, FNR
    """
    # colunm sum and row sum
    colunm_sums = np.sum(confusion_mat, axis = 0)
    row_sums = np.sum(confusion_mat, axis = 1)
    # all array elements sum
    arr_sums = np.sum(confusion_mat)
    
    # calculate the metrics
    metrics = []
    for i in range(confusion_mat.shape[0]):
        metric = []
        # TP
        tp = confusion_mat[i,i]
        # FP
        fp = colunm_sums[i] - tp
        # FN
        fn = row_sums[i] - tp
        # TN
        tn = arr_sums - (fn + fp + tp)
        # accuracy: (TP + TN)/(TP + FP + FN + TN)
        acc = (tp + tn)/(tp + fp + fn + tn)
        # TPR,FPR,TNR,FNR
        tpr = tp/(tp + fn)
        fpr = fp/(fp + tn)
        tnr = 1 - fpr
        fnr = 1 - tpr
        metric.append(acc)
        metric.append(tpr)
        metric.append(fpr)
        metric.append(tnr)
        metric.append(fnr)
        metrics.append(metric)
    metrics = np.array(metrics)
    
    return metrics