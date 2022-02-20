import pandas as pd
import numpy as np
import sentencetovector
import kNN
import matplotlib.pyplot as plt
import seaborn as sn

### 修改classification用 ###

### 資料前處理 ###
# 讀取原始資料
autoggb = pd.read_csv("Autoggb_data.csv")
# 擷取Sentence和Type欄位，轉換成list形式
sentence_list = autoggb['Sentence'].tolist()
type_list = autoggb['Type'].tolist()
# 設定關鍵字列表
feature_list = ['圓', '線段', '直線', '中點', '拋物線']
N = len(feature_list)
# 設定動詞、其他數學名詞列表
verb_list = ['作', '畫', '求']
otherwise_list = ['圓心', '半徑', '點', '直徑', '準線', '焦點', '交點', 
                  '原點', '斜率', '三角形', '正方形', '橢圓', '長方形',
                  'x軸', 'y軸', '外接圓']

# 將資料分成train和test兩塊
# importing train_test_split
from sklearn.model_selection import train_test_split
sentence_train, sentence_test, type_train, type_test = train_test_split(
    sentence_list, type_list,
    train_size=0.8,
    test_size=0.2,
    random_state=0,
    stratify=type_list
    )
#print(type_train)
#print(type_test)

# 將sentence_train 和 sentence_test 轉換成特徵向量
feature_vector_train = []
for item1 in sentence_train:
    feature_vector_train.append(
        sentencetovector.get_FEATURE_FI_2(item1, feature_list, verb_list, otherwise_list)
        )

feature_vector_test = []
for item2 in sentence_test:
    feature_vector_test.append(
        sentencetovector.get_FEATURE_FI_2(item2, feature_list, verb_list, otherwise_list)
        )

### kNN分類器 ###
# 初始化預測列表
pred_test = []
# value of 'k'
k = 13
# 分類模型
for i in range(len(sentence_test)):
    # 用feature_list先做篩選
    if any(ext in sentence_test[i] for ext in feature_list):
        # 計算所有test與train的距離
        unknown_dist_list = []
        for item3 in feature_vector_train:
            unknown_dist_list.append(kNN.dist_ave(feature_vector_test[i], item3, N+2))
    
        # 用kNN分類
        predict = kNN.kNNmodel(unknown_dist_list, type_train, k)
        pred_test.append(predict)
    
    else:
        predict = 'Otherwise'
        pred_test.append(predict)
        
#print(pred_test)
#print(type_test)

### 模型表現分析 ###
target_names=['Circle', 'Segment', 'Line','Midpoint', 'Parabola', 'Otherwise']
kNN.metric4kNNmodel_display(type_test, pred_test, target_names)

# find wrong predict
# # add 'predict' to the dataframe
# df_confusion['predict'] = np.array(pred_list)
# # dataframe incorrect collect the wrong preditc
# incorrect = df_confusion[df_confusion['predict'] != df_confusion['Type']]
# print(incorrect)



