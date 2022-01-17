import pandas as pd
import numpy as np
import sentencetovector
import kNN
import matplotlib.pyplot as plt
import seaborn as sn

### preprocessing ###
# read data
df1 = pd.read_csv("Autoggb_trainingdata.csv")

#擷取Sentence和Type欄位，並且轉換成list形式
sentence_list = df1['Sentence'].tolist()
type_list = df1['Type'].tolist()

# 關鍵字列表
feature_list = ['圓', '線段', '直線', '中垂線', '中點', '拋物線']
N = len(feature_list)
# 動詞、其他數學名詞列表
verb_list = ['作', '畫', '求']
otherwise_list = ['圓心', '半徑', '點', '直徑', '準線', '焦點', '交點', 
                  '原點', '斜率', '三角形', '正方形', '橢圓', '長方形',
                  'x軸', 'y軸', '外接圓']
# 將sentence_list 轉換成向量
vector_list = []
for item1 in sentence_list:
    vector_list.append(sentencetovector.get_FEATURE_FI_2(item1, feature_list, verb_list, otherwise_list))

### predict ###
# 讀取欲分類資料
df2 = pd.read_csv('Autoggb_testdata.csv')
stest_list = df2['Sentence'].tolist()
stype_list = df2['Type'].tolist()
# 預測list
pred_list = []
# value of 'k'
k = 7

# predict model
for i in range(len(stype_list)):
    # 用feature_list先做篩選
    if any(ext in stest_list[i] for ext in feature_list):
        #print('sentence: ', stest_list[i])
        v = sentencetovector.get_FEATURE_FI_2(stest_list[i], feature_list, verb_list, otherwise_list)

        # 計算與所有已分類資料的距離
        unknown_dist_list = []
        for item2 in vector_list:
            unknown_dist_list.append(kNN.dist_ave(v, item2, N+2))
    
        # 用kNN分類
        predict = kNN.kNNmodel(unknown_dist_list, type_list, k)
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
#print(stype_list)

# confusion matrix 分析
# 實際
y_actu = pd.Series(stype_list, name='Actual')
# 預測
y_pred = pd.Series(pred_list, name='Predicted')

#print(y_actu)
#print(y_pred)
# confusion matrix
df_confusion = pd.crosstab(y_actu, y_pred)
#print(df_confusion)
# draw confusion matrix
sn.heatmap(df_confusion, annot=True)
plt.show()

# find wrong predict
# add 'predict' to the dataframe
df2['predict'] = np.array(pred_list)
# dataframe incorrect collect the wrong preditc
incorrect = df2[df2['predict'] != df2['Type']]
print(incorrect)