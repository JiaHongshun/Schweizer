def agoNow(df,id_col,time_col):
    '''返回每一个ID类别的最近一条记录和最远一条记录(按time_col时间)'''
    tmp_sorted = df.sort_values(by = [id_col,time_col],ascending=True)
    tmp_ago = tmp_sorted.drop_duplicates(subset=['id_col'],keep='first')
    tmp_now = tmp_sorted.drop_duplicates(subset=['id_col'],keep='last')
    tmp_ago_now = pd.concat([tmp_ago,tmp_now],axis = 0,ignore_index =True)
    tmp_ago_now.sort_values(by=['name','created'],ascending=True,inplace=True)
    return tmp_ago_now


def varChi(df,var_list,target,alpha=0.05,detail=False):
    '''根据卡方值选择与目标关联较大的分类变量，默认以0.05为比较值'''
    import sklearn.feature_selection as feature_selection
    import pandas as pd
    data = churn.copy()
    for var in var_list:
        data[var] = data[var].astype('int')
    chi_result = feature_selection.chi2(data[var_list], data[target])
    chiResDf = pd.DataFrame({'var_name':cols,'chi2':chi_result[0],'p_value':chi_result[1]})
    chiResDf['selected'] = chiResDf['p_value'] <= alpha
    if detail:
        return chiResDf
    else:
        return list(chiResDf.loc[chiResDf['selected'],'var_name'])


def crossPercent(df,row,col,axis):
    '''分类变量交叉列联表行列百分比计算'''
    import pandas as pd
    cross = pd.crosstab(df[row],df[col],margins=True)
    return cross.apply(lambda x:x/float(x[-1]),axis=axis)


def get_sample(df, sampling="simple_random", k=1, stratified_col=None):
    """
    对输入的 dataframe 进行抽样的函数

    参数:
        - df: 输入的数据框 pandas.dataframe 对象

        - sampling:抽样方法 str
            可选值有 ["simple_random", "stratified", "systematic"]
            按顺序分别为: 简单随机抽样、分层抽样、系统抽样

        - k: 抽样个数或抽样比例 int or float
            (int, 则必须大于0; float, 则必须在区间(0,1)中)
            如果 0 < k < 1 , 则 k 表示抽样对于总体的比例
            如果 k >= 1 , 则 k 表示抽样的个数；当为分层抽样时，代表每层的样本量

        - stratified_col: 需要分层的列名的列表 list
            只有在分层抽样时才生效

    返回值:
        pandas.dataframe 对象, 抽样结果
    """
    import random
    import pandas as pd
    from functools import reduce
    import numpy as np
    import math
    
    len_df = len(df)
    if k <= 0:
        raise AssertionError("k不能为负数")
    elif k >= 1:
        assert isinstance(k, int), "选择抽样个数时, k必须为正整数"
        sample_by_n=True
        if sampling is "stratified":
            alln=k*df.groupby(by=stratified_col)[stratified_col[0]].count().count() # 有问题的
            #alln=k*df[stratified_col].value_counts().count() 
            if alln >= len_df:
                raise AssertionError("请确认k乘以层数不能超过总样本量")
    else:
        sample_by_n=False
        if sampling in ("simple_random", "systematic"):
            k = math.ceil(len_df * k)
        
    #print(k)

    if sampling is "simple_random":
        print("使用简单随机抽样")
        idx = random.sample(range(len_df), k)
        res_df = df.iloc[idx,:].copy()
        return res_df

    elif sampling is "systematic":
        print("使用系统抽样")
        step = len_df // k+1          #step=len_df//k-1
        start = 0                  #start=0
        idx = range(len_df)[start::step]  #idx=range(len_df+1)[start::step]
        res_df = df.iloc[idx,:].copy()
        #print("k=%d,step=%d,idx=%d"%(k,step,len(idx)))
        return res_df

    elif sampling is "stratified":
        assert stratified_col is not None, "请传入包含需要分层的列名的列表"
        assert all(np.in1d(stratified_col, df.columns)), "请检查输入的列名"
        
        grouped = df.groupby(by=stratified_col)[stratified_col[0]].count()
        if sample_by_n==True:
            group_k = grouped.map(lambda x:k)
        else:
            group_k = grouped.map(lambda x: math.ceil(x * k))
        
        res_df = pd.DataFrame(columns=df.columns)
        for df_idx in group_k.index:
            df1=df
            if len(stratified_col)==1:
                df1=df1[df1[stratified_col[0]]==df_idx]
            else:
                for i in range(len(df_idx)):
                    df1=df1[df1[stratified_col[i]]==df_idx[i]]
            idx = random.sample(range(len(df1)), group_k[df_idx])
            group_df = df1.iloc[idx,:].copy()
            res_df = res_df.append(group_df)
        return res_df

    else:
        raise AssertionError("sampling is illegal")