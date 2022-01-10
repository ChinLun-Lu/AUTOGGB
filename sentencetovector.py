def get_FEATURE_FI(sentence, feature_list):
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
        key_i = 0
        # 關鍵字出現次數
        key_i_frequency = 0
        # 關鍵字出現index的向量
        key_i_list = []

        # 從頭往後找，找到關鍵字就記下次數跟index，然後下一次從關鍵字的下一個位置開始找
        while i < N:
            if feature_list[j] in sentence[i:N]:
                key_i = sentence[i:N].find(feature_list[j]) + i
                key_i_frequency = key_i_frequency + 1
                key_i_list.append(key_i)
                i = i + sentence[i:N].find(feature_list[j]) + len(feature_list[j])
            else:
                break
    
        KEY_FREQUENCY.append(key_i_frequency)
        KEY_INDEX.append(key_i_list)

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
            
    # 相對位置空格補0
    for item in FEATURE_FI:
        if item[0] == 0:
            item[1].append(0)

    #print('句子: ', sentence)
    #print('feature頻率與相對位置向量: ', FEATURE_FI)
    return FEATURE_FI

def get_FEATURE_FI_2(sentence, feature_list, verb_list, otherwise_list):
    """
    依據給定的關鍵字(feature_list)，並且考慮動詞與其他數學名詞，將句子(sentence)轉換成向量
    參數：
    sentence  (string) 想要轉換的句子
    feature_list  (list)  與幾何繪圖有關的關鍵字
    verb_list  (list)  畫圖動詞
    otherwise_list  (list)  非關鍵字的其他數學名詞
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
        key_i = 0
        # 關鍵字出現次數
        key_i_frequency = 0
        # 關鍵字出現index的向量
        key_i_list = []

        # 從頭往後找，找到關鍵字就記下次數跟index，然後下一次從關鍵字的下一個位置開始找
        while i < N:
            if feature_list[j] in sentence[i:N]:
                key_i = sentence[i:N].find(feature_list[j]) + i
                key_i_frequency = key_i_frequency + 1
                key_i_list.append(key_i)
                i = i + sentence[i:N].find(feature_list[j]) + len(feature_list[j])
            else:
                break
            
        KEY_FREQUENCY.append(key_i_frequency)
        KEY_INDEX.append(key_i_list)
        
    
    # 分段找到動詞的 index
    key_v = 0
    # 出現次數
    key_v_frequency = 0
    # 出現index的向量
    key_v_list = []
    for j in range(len(verb_list)):
        # 找尋動詞的起始位置
        v = 0
        
        # 從頭往後找，找到就記下次數跟index，然後下一次從下一個位置開始找
        while v < N:
            if verb_list[j] in sentence[v:N]:
                key_v = sentence[v:N].find(verb_list[j]) + v
                key_v_frequency = key_v_frequency + 1
                key_v_list.append(key_v)
                v = v + sentence[v:N].find(verb_list[j]) + len(verb_list[j])
            else:
                break
    
    # 這個迴圈跑完再接入主要列表
    KEY_FREQUENCY.append(key_v_frequency)
    KEY_INDEX.append(key_v_list)

    # 分段找到其他數學名詞的 index
    key_k = 0
    # 出現次數
    key_k_frequency = 0
    # 出現index的向量
    key_k_list = []
    for j in range(len(otherwise_list)):
        # 找尋其他數學名詞(otherwise)的起始位置
        k = 0

        # 從頭往後找，找到就記下次數跟index，然後下一次從下一個位置開始找
        while k < N:
            if otherwise_list[j] in sentence[k:N]:
                key_k = sentence[k:N].find(otherwise_list[j]) + k
                key_k_frequency = key_k_frequency + 1
                key_k_list.append(key_k)
                k = k + sentence[k:N].find(otherwise_list[j]) + len(otherwise_list[j])
            else:
                break
    
    # 這個迴圈跑完再接入主要列表
    KEY_FREQUENCY.append(key_k_frequency)
    KEY_INDEX.append(key_k_list)

    ### 將次數和位置的向量組在一起 ###
    # 最終的feature向量
    FEATURE_FI = []
    # 合併
    for i in range(len(feature_list) + 2):
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

    for i in range(len(feature_list) + 2):
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
            
    # 相對位置空格補0
    for item in FEATURE_FI:
        if item[0] == 0:
            item[1].append(0)

    #print('句子: ', sentence)
    #print('feature頻率與相對位置向量: ', FEATURE_FI)
    return FEATURE_FI