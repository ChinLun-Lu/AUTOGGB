import numpy as np
import pandas as pd

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
        unknown_dist_list ([list]): [欲分類資料與訓練資料的距離列表]
        type_list ([list]): [訓練資料的繪圖項目列表]
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


def metric4kNNmodel_display(x_test, y_test, target_names):
    ### 模型表現分析 ###
    # importing confusion_matrix
    from sklearn.metrics import confusion_matrix
    confusionmatrix = confusion_matrix(x_test, y_test)
    print('Confusion Matrix\n')
    print(confusionmatrix)

    # importing accuracy_score, precision_score, recall_score, f1_score
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    print('\nAccuracy: {:.2f}\n'.format(accuracy_score(x_test, y_test)))

    # Micro : global
    print('Micro Precision: {:.2f}'.format(precision_score(x_test, y_test, average='micro')))
    print('Micro Recall: {:.2f}'.format(recall_score(x_test, y_test, average='micro')))
    print('Micro F1-score: {:.2f}\n'.format(f1_score(x_test, y_test, average='micro')))

    # macro : each class and takes unweighted mean
    print('Macro Precision: {:.2f}'.format(precision_score(x_test, y_test, average='macro')))
    print('Macro Recall: {:.2f}'.format(recall_score(x_test, y_test, average='macro')))
    print('Macro F1-score: {:.2f}\n'.format(f1_score(x_test, y_test, average='macro')))

    # weighted : weight from number of each class
    print('Weighted Precision: {:.2f}'.format(precision_score(x_test, y_test, average='weighted')))
    print('Weighted Recall: {:.2f}'.format(recall_score(x_test, y_test, average='weighted')))
    print('Weighted F1-score: {:.2f}'.format(f1_score(x_test, y_test, average='weighted')))

    # importing classification_report
    from sklearn.metrics import classification_report

    print('\nClassification Report\n')
    print(classification_report(x_test, y_test, target_names=target_names))