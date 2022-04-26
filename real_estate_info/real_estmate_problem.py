import pandas as pd

# Function for converting chinese to number
def convert_floor(chinese):
    numbers = {'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9}
    units = {'十':10}
    number, pureNumber = 0, True
    for i in range(len(chinese)):
        if chinese[i] in units:
            pureNumber = False
            break
        if chinese[i] in numbers:
            number = number * 10 + numbers[chinese[i]]
    if pureNumber:
        return number
        
    number = 0
    for i in range(len(chinese)):
        base = 10
        if chinese[i] in numbers and len(chinese)==3:
            number = numbers[chinese[i]]*base + numbers[chinese[i+2]]
            break
        elif chinese[i] == '十':
            number = base + numbers[chinese[i+1]]
            break
        elif chinese[i+1] == '十' and len(chinese)==2:
            number = numbers[chinese[i]]*base
            break
    return number

# filter_a
def to_filter_a(data):
    filter_a_1 = (data['主要用途']=='住家用')
    tmp = data.loc[filter_a_1]

    tmp = tmp.loc[tmp['建物型態'].str.contains('住宅大樓', na=False)]

    tmp['總樓層數'] = tmp['總樓層數'].str.replace('層','')
    tmp['總樓層數'] = tmp['總樓層數'].apply(convert_floor)

    filter_a = tmp.loc[tmp['總樓層數']>=13]
    filter_a.reset_index(drop=True)
    return filter_a

#filter_b
def to_filter_b(data):
    total_count = len(data)
    total_spot_count = 0
    for i in range(len(data)):
        num = int(data['交易筆棟數'].loc[i][-1])
        total_spot_count += num

    average_price = data['總價元'].astype(int).mean()
    num = 0
    for i in range(len(data)):
        if data['交易筆棟數'].loc[i][-1] != '0':
            #print(data['車位總價元'].loc[i])
            num += int(data['車位總價元'].loc[i])
    average_spot_price = num/total_spot_count

    df_ = {'總件數':[total_count],'總車位數':[total_spot_count],\
        '平均總價元':[average_price], '平均車位總價元':[average_spot_price]}
    filter_b = pd.DataFrame(data=df_,index=['答案'])
    return filter_b

def main(path):
    df_a = pd.read_csv(path+'a_lvr_land_a.csv').drop([0])
    df_b = pd.read_csv(path+'b_lvr_land_a.csv').drop([0])
    df_e = pd.read_csv(path+'e_lvr_land_a.csv').drop([0])
    df_f = pd.read_csv(path+'f_lvr_land_a.csv').drop([0])
    df_h = pd.read_csv(path+'h_lvr_land_a.csv').drop([0])
    total = [df_a, df_b, df_e, df_f, df_h]
    df_all = pd.concat(total).reset_index(drop=True)
    ans_1 = to_filter_a(df_all)
    ans_1.to_csv('filter_a.csv')
    ans_2 = to_filter_b(df_all)
    ans_2.to_csv('filter_b.csv')

if __name__ == '__main__':
    # -------- configurable parameter -------- #
    path = 'C:\\Users\\bruce\\Desktop\\project\\real_estate_info\\'
    main(path)
    print('\nfinish!')





