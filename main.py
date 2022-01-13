import pandas as pd
import sentencetovector
import kNN
import matplotlib.pyplot as plt

### preprocessing ###
# read data
df = pd.read_excel("Autoggb_trainingdata.xlsx")

#擷取Sentence和Type欄位，並且轉換成list形式
sentence_list = df['Sentence'].tolist()
type_list = df['Type'].tolist()
#M = len(sentence_list)

# 關鍵字列表
feature_list = ['圓', '線段', '直線', '中垂線', '中點', '拋物線']
N = len(feature_list)
# 動詞、其他數學名詞列表
verb_list = ['作', '畫', '求']
otherwise_list = ['圓心', '半徑', '準線', '焦點', '交點', '原點', '斜率']
# 將sentence_list 轉換成向量
vector_list = []
for item1 in sentence_list:
    vector_list.append(sentencetovector.get_FEATURE_FI_2(item1, feature_list, verb_list, otherwise_list))

### training ###
# 欲分類資料
stest_list = ['畫一個1公分的線段', '畫一個半徑是r的圓', '作一條斜率為m的直線', 'test']
stype_list = ['Segment', 'Circle', 'Line', 'Otherwise']
# 預測list
pred_list = []
# value of 'k'
k = 5
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

print(pred_list)
print(stype_list)

# confusion matrix 分析
# 實際情況
y_actu = pd.Series(stype_list, name='Actual')
# 預測情況
y_pred = pd.Series(pred_list, name='Predicted')
# confusion matrix
df_confusion = pd.crosstab(y_actu, y_pred)
print(df_confusion)

# 訓練k
