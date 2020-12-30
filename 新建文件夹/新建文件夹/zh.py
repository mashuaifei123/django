import pandas as pd
from os import listdir
import re


def date_del(df):
    df.insert(1, 1_1, df['检测时间'])
    df[1_1].index = df[1_1].index + 1
    df['检测时间'] = df[1_1] + df['检测时间']
    df.drop([1_1], axis=1, inplace=True)
    df_mean = df.loc[[j for j in range(3, df.shape[0], 4)], :]
    df_mean['检测时间'] = df_mean['检测时间'].apply(lambda x: x[:-4])
    df_spss_ok, second_name_list, time = date_del_one(df_mean)
    return df_spss_ok, second_name_list, time


def date_del_1(df):
    df = df[:-1]
    df = df.dropna(axis=0)
    b = list(df['动物编号'])
    c = [i for i in range(len(b) - 1) if b[i] == b[i + 1]]
    df.drop(df.index[c], inplace=True)
    df = df.reset_index(drop=True)
    b = list(df['动物编号'])
    c = [i[0] for i in b]
    d = [i for i in range(len(c) - 1) if c[i] > c[i + 1]]
    # print(d)
    e = list(df['试验阶段'])
    df_time = list(set(e))
    df_time.remove('mean')
    df_time.sort(key=e.index)
    # print(xueya_time)
    df['试验阶段'][0:d[0]] = df_time[0]
    df['试验阶段'][d[-1] + 1:] = df_time[-1]
    for i in range(len(d) - 1):
        df['试验阶段'][d[i] + 1:d[i + 1] + 1] = df_time[i + 1]
    df.rename(columns={'试验阶段': '检测时间'}, inplace=True)
    return df


def date_del_one(df_mean):
    df_mean_list = df_mean.iloc[:, 1].tolist()
    PDR_set = list(set(df_mean_list))
    PDR_set.sort(key=df_mean_list.index)  # 保留顺序转换列表->去重复集合->列表原始顺序排序
    PDR_set_l = []
    for x, i in enumerate(PDR_set, 1):
        PDR_set_l.append((i, '{:02d}_{}'.format(x, i)))

    def id_to_idn(id, id_list):  # 根据及生成的列表加01- 用于排序
        for id_old in id_list:
            if id == id_old[0]:
                return id_old[1]

    # print(PDR_set)
    # print(PDR_set_l)
    df_mean['检测时间'] = df_mean[:]['检测时间'].map(lambda x: id_to_idn(str(x), PDR_set_l))
    df_mean.index = [df_mean['动物编号'].tolist(), df_mean['检测时间'].tolist()]
    df_mean.drop(['动物编号'], axis=1, inplace=True)
    df_mean.drop(['检测时间'], axis=1, inplace=True)
    df_mean = df_mean.unstack()
    CO1_name = list(df_mean.columns.levels[0])
    CO2_name = list(df_mean.columns.levels[1])
    RO2_name = list(df_mean.index)
    '''组合成一个列名字'''
    title_list = list(
        map(lambda x: '{}'.format(str(x), str(x)), [str(i) + '_' + str(j)[3:] for i in CO1_name for j in CO2_name]))
    df_spss_ok = pd.DataFrame(df_mean.values, columns=title_list, index=RO2_name)
    df_spss_ok = df_spss_ok.reset_index()
    df_spss_ok.rename(columns={'index': '动物编号'}, inplace=True)  # 重名命列名字
    df_spss_ok.insert(0, 'Group', df_spss_ok[:]['动物编号'].map(lambda x: str(x).strip()[:1]))  # 插入一列group
    '''
    for k in range(2+len(PDR_set),df_spss_ok.shape[1]): 
        df_spss_ok.iloc[:,k] = df_spss_ok.iloc[:,k].apply(lambda x :str('%.2f'%x) )
        df_spss_ok.iloc[:,k] = df_spss_ok.iloc[:,k].apply(pd.to_numeric,errors='errors')
    '''
    second_name_list = CO1_name
    time = PDR_set
    # print(second_name_list)
    # print(time)
    return df_spss_ok, second_name_list, time


def decimal(df, time, CC):
    if CC == '心电':
        for k in range(2 + len(time), df.shape[1]):
            df.iloc[:, k] = df.iloc[:, k].apply(lambda x: str('%.2f' % x))
            df.iloc[:, k] = df.iloc[:, k].apply(pd.to_numeric, errors='errors')

    if CC == '呼吸':
        for k in range(2, 2 + len(time)):
            df.iloc[:, k] = df.iloc[:, k].apply(lambda x: str('%.0f' % x))
            df.iloc[:, k] = df.iloc[:, k].apply(pd.to_numeric, errors='errors')
        for k1 in range(2 + len(time), df.shape[1]):
            df.iloc[:, k1] = df.iloc[:, k1].apply(lambda x: str('%.1f' % x))
            df.iloc[:, k1] = df.iloc[:, k1].apply(pd.to_numeric, errors='errors')

    if CC == '血压':
        for k in range(2, df.shape[1]):
            df.iloc[:, k] = df.iloc[:, k].apply(lambda x: str('%.0f' % x))
            df.iloc[:, k] = df.iloc[:, k].apply(pd.to_numeric, errors='errors')


def split_excel(df, time, second_name_list, first_name, sex):
    # 开始拆分excel
    file_number = int((df.shape[1] - 2) / len(time))  # 导出文件数
    fn = df.columns  # df的所有指标名 很多带时间的
    second_name_list2 = []
    for name in second_name_list:
        result = re.sub(u"\\(.*?\\)", "", name)
        second_name_list2.append(result)  # 导出excel的第二层名字
    second_name_list2 = [x.strip() for x in second_name_list2]
    # print(second_name_list2)
    for f in range(0, file_number):
        col_list = [fn[0], fn[1]]
        for col in range(0, len(time)):
            col_list.append(fn[f * len(time) + col + 2])
        # print(col_list)
        new_df = pd.DataFrame(df, columns=col_list)  # 重组构成需要导出的excel
        new_df.to_excel(out_path + first_name + sex + second_name_list2[f] + '.xlsx', index=None)


def read_excel(inpath, outpath):
    # 读取路径中的所有excel，放入列表等待处理
    xlsx_list = [fn for fn in listdir(inpath) if fn.endswith('.xlsx')]
    xlsx_list.sort()
    xlsx_list_path = list(map(lambda y: inpath + y, xlsx_list))
    for i in xlsx_list_path:
        if '心电' in i:
            xindian_F = pd.read_excel(i, skiprows=1, usecols='B:L')
            xindian_F_ok, second_name_list, time = date_del(xindian_F)
            decimal(xindian_F_ok, time, '心电')
            split_excel(xindian_F_ok, time, second_name_list, '心电', '雄')

            xindian_M = pd.read_excel(i, skiprows=1, usecols='O:Y')
            xindian_M_ok, second_name_list, time = date_del(xindian_M)
            decimal(xindian_M_ok, time, '心电')
            split_excel(xindian_M_ok, time, second_name_list, '心电', '雌')
            print('心电finished')

        if '呼吸' in i:
            huxi_F = pd.read_excel(i, skiprows=1, usecols='B:G')
            huxi_F_ok, second_name_list, time = date_del(huxi_F)
            print(huxi_F)
            decimal(huxi_F_ok, time, '呼吸')
            split_excel(huxi_F_ok, time, second_name_list, '呼吸', '雄')

            huxi_M = pd.read_excel(i, skiprows=1, usecols='J:O')
            print(huxi_M)
            huxi_M_ok, second_name_list, time = date_del(huxi_M)
            print(huxi_M)
            decimal(huxi_M_ok, time, '呼吸')
            split_excel(huxi_M_ok, time, second_name_list, '呼吸', '雌')
            print('呼吸finished')

        if '体温' in i:
            tiwen_F = pd.read_excel(i, skiprows=1, usecols='B:G')
            a = list(tiwen_F.columns[1:])
            new_column = ['体温_' + x for x in a]
            new_column.insert(0, '动物编号')
            tiwen_F.columns = new_column
            tiwen_F.replace('/', '', inplace=True)
            tiwen_F.insert(0, 'Group', tiwen_F[:]['动物编号'].map(lambda x: str(x).strip()[:1]))
            tiwen_F.to_excel(out_path + '体温雄.xlsx', index=None)
            tiwen_M = pd.read_excel(i, skiprows=1, usecols='J:O')
            a1 = list(tiwen_M.columns[1:])
            new_column = ['体温_' + x for x in a]
            new_column.insert(0, '动物编号')
            tiwen_M.columns = new_column
            tiwen_M.replace('/', '', inplace=True)
            tiwen_M.insert(0, 'Group', tiwen_M[:]['动物编号'].map(lambda x: str(x).strip()[:1]))
            tiwen_M.to_excel(out_path + '体温雌.xlsx', index=None)
            print('体温finished')

        if '血压' in i:
            xueya_F = pd.read_excel(i, skiprows=1, usecols='B:F')
            xueya_F = date_del_1(xueya_F)
            xueya_F_ok, second_name_list, time = date_del_one(xueya_F)
            decimal(xueya_F_ok, time, '血压')
            split_excel(xueya_F_ok, time, second_name_list, '血压', '雄')

            xueya_M = pd.read_excel(i, skiprows=1, usecols='I:M')
            xueya_M = date_del_1(xueya_M)
            xueya_M_ok, second_name_list, time = date_del_one(xueya_M)
            decimal(xueya_M_ok, time, '血压')
            split_excel(xueya_M_ok, time, second_name_list, '血压', '雌')
            print('血压finished')


if __name__ == "__main__":
    in_path = r'K:\mashuaifei\20200314excel拆分\Fw_A2019027-T014-01健康检查个体数就和方案\\'
    out_path = r'K:\mashuaifei\20200314excel拆分\22\\'
    read_excel(in_path, out_path)
    print('all finished')