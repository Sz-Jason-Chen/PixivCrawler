
# Press the green button in the gutter to run the script.
import pandas as pd
from Apriori import *
import time
#删除字符串首尾的中括号和引号
def remove_first_and_last(x):
    x = x.replace("'","")
    x = x.replace(" ","")
    return x[1:-1]
#从原始数据集提取tags和id并生成新的数据集
def get_data():
    df = pd.read_csv('../output/illust_info_001.csv',encoding='gbk')
    #print(df)

    df2 = df[['id','tags']]

    df2.to_csv('../output/output.csv',encoding='gbk',index=False)
#统计频率
def freq():
    raw = pd.read_csv('../output/sample_raw.csv',encoding='gbk')
    raw['tags'] = raw['tags'].apply(remove_first_and_last)
    raw_id = raw.drop('tags',axis=1)
    #此处raw_tags是list
    raw_tags = raw.tags.str.split(',')
    freq_dict = {}

    for item in raw_tags:
        for str in item:
            if str in freq_dict:
                freq_dict[str] += 1
            else:
                freq_dict[str] = 1

    for key, value in freq_dict.items():
        print(f"{key}: {value}")

    key_list = []
    value_list = []
    items = freq_dict.items()
    for key, value in items:
        if value >= 20:
            key_list.append(key)
            value_list.append(value)
    res_dict = {'tag':key_list,'freq':value_list}


    df_freq = pd.DataFrame.from_dict(res_dict)
    df_freq.to_csv('../output/freq.csv', index=False, sep=',',encoding= 'gbk')



#抽样
def sample():
    new_sample = pd.read_csv('../output/output.csv',encoding='gbk')
    new_sample = new_sample.sample(n=30000)
    new_sample.to_csv('../output/sample_raw.csv',encoding='gbk',index=False)
#空列表置为None
def remove_empty_list(x):
    if x == []:
        return None
    else:
        return x

#在采样后数据集的基础上删除不满足频率要求的tags
def cut():
    raw = pd.read_csv('../output/sample_raw.csv', encoding='gbk')
    raw['tags'] = raw['tags'].apply(remove_first_and_last)
    raw_id = raw.drop('tags', axis=1)
    # 此处raw_tags是list
    raw_tags = raw.tags.str.split(',')

    frequency = pd.read_csv('../output/freq.csv',encoding='gbk')
    freq_dict = dict(zip(frequency['tag'],frequency['freq']))
    for list in raw_tags:
        for str in list:
            if str not in freq_dict:
                list.remove(str)
    raw_tags = raw_tags.apply(remove_empty_list)
    raw = raw_id.join(raw_tags)

    raw.dropna(axis=0,subset=['tags'],how='any',inplace=True)
    raw_tags = raw_tags.dropna()
    raw.to_csv('../output/cut_raw.csv',encoding='gbk',index=False)






'''
def dum():
    cut_raw = pd.read_csv('cut_raw.csv',encoding='gbk')
    cut_raw_id = cut_raw.drop('tags',axis=1)
    #print(cut_raw_id)
    cut_raw_tags = cut_raw.tags.apply(remove_first_and_last)
    #print(cut_raw_tags)
    cut_raw_tags = cut_raw_tags.str.get_dummies(',')
    cut_raw = pd.concat([cut_raw_id,cut_raw_tags],axis=1)
    #print(cut_raw)
    cut_raw.to_csv('cut_raw_dum.csv',encoding='gbk',index=False)
'''







if __name__ == '__main__':
#从源数据集获取数据,写入output.csv
    get_data()
#对数据集进行采样，减少数据数量，生成sample_raw.csv
    sample()
#统计tag出现频率，生成freq.csv
    freq()
#对数据进行裁剪，裁掉不符合频率要求的tag,生成cut_raw.csv
    cut()
#使用cut_raw.csv以及apriori算法分析tag关联性
    s = time.time()
    ap_data = pd.read_csv('../output/cut_raw.csv',encoding='gbk')
    ap_data['tags'] = ap_data['tags'].apply(remove_first_and_last)
    raw_tags = ap_data.tags
    raw_tags = raw_tags.str.split(',')

    input_data = []

    for item in raw_tags:
        input_data.append(item)

    item_set = get_item_set(input_data)
    infrequent_list, frequent_list, frequent_support_list = apriori(item_set, input_data, min_support=0.001)

    rule_set = generate_rules(frequent_list, input_data, min_confidence=0.30)
    print("总用时:", (time.time() - s), "s")
