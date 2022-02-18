import pandas as pd
import numpy as np
import sentencetovector
import kNN
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.model_selection import train_test_split

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
# sentence_train: 訓練用的句子
# sentence_test: 測試用的句子
# type_train: 訓練用的分類
# type_test: 測試用的分類
sentence_train, sentence_test, type_train, type_test = train_test_split(
    sentence_list, type_list,
    train_size=0.8,
    test_size=0.2,
    random_state=777,
    stratify=type_list
    )
print(type_train)
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

### kNN分類器 ###
# 初始化預測列表
pred_list = []
# value of 'k'
k = 11

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
        pred_list.append(predict)
        #print('predict: ', predict)
        #print('real: ', stype_list[i])
    
    else:
        predict = 'Otherwise'
        pred_list.append(predict)
        #print('sentence: ', stest_list[i])
        #print('predict: ', predict)
        #print('real: ', stype_list[i])

#print(pred_list)
#print(type_test)

### 模型表現分析 ###
# 實際
y_actu = pd.Series(type_test, name='Actual')
# 預測
y_pred = pd.Series(pred_list, name='Predicted')
#print(y_actu)
#print(y_pred)

# confusion matrix
df_confusion = pd.crosstab(y_actu, y_pred, dropna=False)
raw_of_types = ['Circle', 'Segment', 'Line', 'Midpoint', 
                'Parabola', 'Otherwise']
# reorder columns
df_confusion = df_confusion.reindex(raw_of_types, axis="columns")
# reorder raws
df_confusion = df_confusion.reindex(raw_of_types)
print(df_confusion)

# # calculate the metrics
# df_confusion02 = df_confusion.to_numpy()
# metrics = kNN.metric4kNNmodel(df_confusion02)
# print(df_confusion02)
# print(metrics)
# # generate dataframe
# # array to dataframe
# column_names = ['Accuracy', 'Sensitivity(TPR)', 'Specificity(TNR)', 'FPR', 'FNR']
# df_metrics = pd.DataFrame(metrics, index = raw_of_types, columns = column_names)
# print(df_metrics)


# # find wrong predict
# # add 'predict' to the dataframe
# df2['predict'] = np.array(pred_list)
# # dataframe incorrect collect the wrong preditc
# incorrect = df2[df2['predict'] != df2['Type']]
# print(incorrect)

# draw confusion matrix
#specify size of heatmap
fig, ax = plt.subplots(figsize=(7, 5))
sn.heatmap(df_confusion, annot=True)
# add title and axe labels
plt.title('Confusion Matrix')
#plt.xlabel('Actual')
#plt.ylabel('Predict')
plt.show()

