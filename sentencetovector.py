def get_FEATURE_FI(sentence,feature_list):
    """
    依據給定的關鍵字(feature_list)，將句子(sentence)轉換成向量
    參數：
    sentence  (string) 想要轉換的句子
    feature_list  (list)  與幾何繪圖有關的關鍵字
    輸出：
    FEATURE_FI  (list)  轉換後的向量，包含關鍵字出現在句子中的次數與相對位置
    """

    # 句子的長度
    N = len(sentence)

    # features 關鍵字出現次數
    KEY_FREQUENCY = []
    # features 關鍵字出現位置
    KEY_INDEX = []
    ### 找出關鍵字在句子當中的位置 ###
    for j in range(len(feature_list)):
        # 找尋關鍵字的起始位置
        i = 0
        # 分段找到關鍵字的 index
        key_k = 0
        # 關鍵字出現次數
        key_frequency = 0
        # 關鍵字出現index的向量
        key_k_list = [0]

        # 從頭往後找，找到關鍵字就記下次數跟index，然後下一次從關鍵字的下一個位置開始找
        while i < N:
            if feature_list[j] in sentence[i:N]:
                key_k = sentence[i:N].find(feature_list[j]) + i
                key_frequency = key_frequency + 1
                key_k_list.append(key_k)
                i = i + sentence[i:N].find(feature_list[j]) + len(feature_list[j])
            else:
                break
    
        KEY_FREQUENCY.append(key_frequency)
        KEY_INDEX.append(key_k_list)

    ### 將次數和位置的向量組在一起 ###
    # 最終的feature向量
    FEATURE_FI = []
    # 合併
    for i in range(len(feature_list)):
        # 各feature分量
        feature_fi_component = []
        feature_fi_component.append(KEY_FREQUENCY[i])
        feature_fi_component.append(KEY_INDEX[i])
        FEATURE_FI.append(feature_fi_component)
    #print('feature頻率與位置向量: ', FEATURE_FI)


    ### feature向量以相對位置表示 ###
    # 儲存 KEY_INDEX 裡有值的分量
    temp1 = []
    # 儲存 KEY_FREQUENCY 裡大於零的分量的index
    temp2 = []

    for i in range(len(feature_list)):
        if KEY_INDEX[i] != [] and KEY_FREQUENCY[i] > 0:
            temp1.append(KEY_INDEX[i])
            temp2.append(i)


    # 將temp1由小到大變成123順序
    # 排序用的陣列
    temp = []
    for i in range(len(temp1)):
        for j in range(len(temp1[i])):
            temp.append(temp1[i][j])
    # 排序      
    temp.sort()

    for i in range(len(temp1)):
        for j in range(len(temp1[i])):
            temp1[i][j] = temp.index(temp1[i][j]) + 1


    # 用temp2對比FEATURE_FI裡的key，將新的temp1放入相對應的key
    for i in range(len(temp2)):
        for j in range(len(temp1[i])):
            FEATURE_FI[temp2[i]][1][j] = temp1[i][j]

    #print('句子: ', sentence)
    #print('feature頻率與相對位置向量: ', FEATURE_FI)
    return FEATURE_FI