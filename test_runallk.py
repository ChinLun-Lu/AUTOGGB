import pandas as pd
import numpy as np
import sentencetovector
import kNN

### 跑全部的k ###

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
print(type_test)

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

# run all `k`
# set range of k
mink, maxk = 1, len(sentence_train)
pred_test = []
# 分類模型
for i in range(len(sentence_test)):
    pred_test02 = []
    # 用feature_list先做篩選
    if any(ext in sentence_test[i] for ext in feature_list):
        # 計算所有test與train的距離
        unknown_dist_list = []
        for item3 in feature_vector_train:
            unknown_dist_list.append(kNN.dist_ave(feature_vector_test[i], item3, N+2))
    
        # 用kNN分類
        for k in range(mink, maxk):
            predict = kNN.kNNmodel(unknown_dist_list, type_train, k)
            pred_test02.append(predict)
        pred_test.append(pred_test02)
    else:
        for k in range(mink, maxk):
            predict = 'Otherwise'
            pred_test02.append(predict)
        pred_test.append(pred_test02)
        
# turning list into array
pred_test = np.array(pred_test)
print(pred_test)

# calculating accuracy
# importing accuracy_score
from sklearn.metrics import accuracy_score
accuracy = []
for i in range(pred_test.shape[1]):
    temp = accuracy_score(type_test, pred_test[:,i])
    accuracy.append(temp)
    
#print(accuracy)

# plot k values and accuracy
# importing matplotlib
import matplotlib.pyplot as plt

k_values = [k for k in range(mink, maxk)]
plt.scatter(k_values, accuracy, s = 10)
#plt.title('Graphical presentation of accuracy with different k values.')
plt.xlabel('k values')
plt.ylabel('accuracy')
plt.show()