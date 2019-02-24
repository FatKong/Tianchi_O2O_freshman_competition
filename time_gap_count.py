import pandas as pd
import numpy as np
def time_gap_count(label):
    '时间差与当月统计'
    def sec_diff(a, b):
        if (a is np.nan) | (b is np.nan):
            return -1
        return b - a
    # label['date_received'] = label['date_received'].map(         #加快速度，取消时间转换
    #     lambda x: datetime.datetime.strptime(str(x), "%Y%m%d"))  # 将日期转换为时间戳

    label = label.sort_values(by='date_received').reset_index(drop=True)
    label_tmp=label[['user_id','merchant_id','coupon_id','date_received']]

    def get_base_usr(index,row):
        if index%1000==0:
            print(index)
        feature = {}
        '-----------------用户时间特征--------------------'
        tmp = label_tmp[label_tmp['user_id'] == row['user_id']]  # 选取与该条user相关的样本
        tmp = tmp.reset_index(drop=True)
        diffs = []
        if len(tmp) == 1:
            diffs.append(-1)
        else:
            for ind in range(len(tmp) - 1):
                diffs.append(sec_diff(tmp.loc[ind + 1, 'date_received'], tmp.loc[ind, 'date_received']))
        usr_max_diff = np.max(diffs)
        usr_min_diff = np.min(diffs)
        usr_avg_diff = np.mean(diffs)
        usr_mid_diff = np.median(diffs)
        usr_diff_first_click = sec_diff(row['date_received'], tmp.loc[0, 'date_received'])
        usr_diff_last_click = sec_diff(row['date_received'], tmp.loc[len(tmp) - 1, 'date_received'])

        usr_previous_diff = sec_diff(np.max(tmp[(tmp['date_received'] < row['date_received'])]['date_received']),
                                     row['date_received'])

        usr_next_diff = sec_diff(row['date_received'],
                                 np.min(tmp[(tmp['date_received'] > row['date_received'])]['date_received']))

        mer_cnt = len(set(tmp['merchant_id']))
        usr_bf_mer_cnt = len(
            set(tmp[(tmp['date_received'] <= row['date_received']) & (tmp['merchant_id'] == row['merchant_id'])]))
        usr_af_mer_cnt = len(
            set(tmp[(tmp['date_received'] > row['date_received']) & (tmp['merchant_id'] == row['merchant_id'])]))
        usr_bf_mer_rate = usr_bf_mer_cnt / mer_cnt
        usr_af_mer_rate = 1 - usr_bf_mer_rate

        cp_cnt = len(set(tmp['coupon_id']))
        usr_bf_cp_cnt = len(
            set(tmp[(tmp['date_received'] <= row['date_received']) & (tmp['coupon_id'] == row['coupon_id'])]))
        usr_af_cp_cnt = len(
            set(tmp[(tmp['date_received'] > row['date_received']) & (tmp['coupon_id'] == row['coupon_id'])]))
        usr_bf_cp_rate = usr_bf_cp_cnt / cp_cnt
        usr_af_cp_rate = 1 - usr_bf_cp_rate

        feature['usr_max_diff'] = usr_max_diff
        feature['usr_min_diff'] = usr_min_diff
        feature['usr_avg_diff'] = usr_avg_diff
        feature['usr_mid_diff'] = usr_mid_diff
        feature['usr_diff_first_click'] = usr_diff_first_click
        feature['usr_diff_last_click'] = usr_diff_last_click
        feature['usr_previous_diff'] = usr_previous_diff
        feature['usr_next_diff'] = usr_next_diff
        feature['usr_bf_mer_cnt'] = usr_bf_mer_cnt
        feature['usr_af_mer_cnt'] = usr_af_mer_cnt
        feature['usr_bf_mer_rate'] = usr_bf_mer_rate
        feature['usr_af_mer_rate'] = usr_af_mer_rate
        feature['usr_bf_cp_cnt'] = usr_bf_cp_cnt
        feature['usr_af_cp_cnt'] = usr_af_cp_cnt
        feature['usr_bf_cp_rate'] = usr_bf_cp_rate
        feature['usr_af_cp_rate'] = usr_af_cp_rate

        return feature
        pass
    def get_base_mer(index,row):
        if index%1000==0:
            print(index)
        feature = {}
        '------------------商家时间特征--------------------'
        tmp = label_tmp[label_tmp['merchant_id'] == row['merchant_id']]  # 选取与该条merchant相关的样本
        tmp = tmp.reset_index(drop=True)
        diffs = []
        if len(tmp) == 1:
            diffs.append(-1)
        else:
            for ind in range(len(tmp) - 1):
                diffs.append(sec_diff(tmp.loc[ind + 1, 'date_received'], tmp.loc[ind, 'date_received']))

        mer_max_diff = np.max(diffs)
        mer_min_diff = np.min(diffs)
        mer_avg_diff = np.mean(diffs)
        mer_median_diff = np.median(diffs)
        mer_diff_first_click = sec_diff(row['date_received'], tmp.loc[0, 'date_received'])
        mer_diff_last_click = sec_diff(row['date_received'], tmp.loc[len(tmp) - 1, 'date_received'])

        mer_previous_diff = sec_diff(np.max(tmp[(tmp['date_received'] < row['date_received'])]['date_received']),
                                     row['date_received'])

        mer_next_diff = sec_diff(row['date_received'],
                                 np.min(tmp[(tmp['date_received'] > row['date_received'])]['date_received']))

        usr_cnt = len(set(tmp['user_id']))
        mer_bf_usr_cnt = len(
            set(tmp[(tmp['date_received'] <= row['date_received']) & (tmp['user_id'] == row['user_id'])]))
        mer_af_usr_cnt = len(
            set(tmp[(tmp['date_received'] > row['date_received']) & (tmp['user_id'] == row['user_id'])]))
        mer_bf_usr_rate = mer_bf_usr_cnt / usr_cnt
        mer_af_usr_rate = 1 - mer_bf_usr_rate

        cp_cnt = len(set(tmp['coupon_id']))
        mer_bf_cp_cnt = len(
            set(tmp[(tmp['date_received'] <= row['date_received']) & (tmp['coupon_id'] == row['coupon_id'])]))
        mer_af_cp_cnt = len(
            set(tmp[(tmp['date_received'] > row['date_received']) & (tmp['coupon_id'] == row['coupon_id'])]))
        mer_bf_cp_rate = mer_bf_cp_cnt / cp_cnt
        mer_af_cp_rate = 1 - mer_bf_cp_rate

        feature['mer_max_diff'] = mer_max_diff
        feature['mer_min_diff'] = mer_min_diff
        feature['mer_avg_diff'] = mer_avg_diff
        feature['mer_median_diff'] = mer_median_diff
        feature['mer_diff_first_click'] = mer_diff_first_click
        feature['mer_diff_last_click'] = mer_diff_last_click
        feature['mer_previous_diff'] = mer_previous_diff
        feature['mer_next_diff'] = mer_next_diff
        feature['mer_bf_usr_cnt'] = mer_bf_usr_cnt
        feature['mer_af_usr_cnt'] = mer_af_usr_cnt
        feature['mer_bf_usr_rate'] = mer_bf_usr_rate
        feature['mer_af_usr_rate'] = mer_af_usr_rate
        feature['mer_bf_cp_cnt'] = mer_bf_cp_cnt
        feature['mer_af_cp_cnt'] = mer_af_cp_cnt
        feature['mer_bf_cp_rate'] = mer_bf_cp_rate
        feature['mer_af_cp_rate'] = mer_af_cp_rate

        return feature
        pass
    def get_base_cp(index,row):
        if index%1000==0:
            print(index)
        feature = {}
        '-----------------优惠券时间特征--------------'
        tmp = label_tmp[label_tmp['coupon_id'] == row['coupon_id']]  # 选取与该条coupon相关的样本
        tmp = tmp.reset_index(drop=True)
        diffs = []
        if len(tmp) == 1:
            diffs.append(-1)
        else:
            for ind in range(len(tmp) - 1):
                diffs.append(sec_diff(tmp.loc[ind + 1, 'date_received'], tmp.loc[ind, 'date_received']))
        cp_max_diff = np.max(diffs)
        cp_min_diff = np.min(diffs)
        cp_avg_diff = np.mean(diffs)
        cp_median_diff = np.median(diffs)
        cp_diff_first_click = sec_diff(row['date_received'], tmp.loc[0, 'date_received'])
        cp_diff_last_click = sec_diff(row['date_received'], tmp.loc[len(tmp) - 1, 'date_received'])

        cp_previous_diff = sec_diff(np.max(tmp[(tmp['date_received'] < row['date_received'])]['date_received']),
                                    row['date_received'])

        cp_next_diff = sec_diff(row['date_received'],
                                np.min(tmp[(tmp['date_received'] > row['date_received'])]['date_received']))

        usr_cnt = len(set(tmp['user_id']))
        cp_bf_usr_cnt = len(
            set(tmp[(tmp['date_received'] <= row['date_received']) & (tmp['user_id'] == row['user_id'])]))
        cp_af_usr_cnt = len(
            set(tmp[(tmp['date_received'] > row['date_received']) & (tmp['user_id'] == row['user_id'])]))
        cp_bf_usr_rate = cp_bf_usr_cnt / usr_cnt
        cp_af_usr_rate = 1 - cp_bf_usr_rate

        mer_cnt = len(set(tmp['merchant_id']))
        cp_bf_mer_cnt = len(
            set(tmp[(tmp['date_received'] <= row['date_received']) & (tmp['merchant_id'] == row['merchant_id'])]))
        cp_af_mer_cnt = len(
            set(tmp[(tmp['date_received'] > row['date_received']) & (tmp['merchant_id'] == row['merchant_id'])]))
        cp_bf_mer_rate = cp_bf_mer_cnt / mer_cnt
        cp_af_mer_rate = 1 - cp_bf_mer_rate

        feature['cp_max_diff'] = cp_max_diff
        feature['cp_min_diff'] = cp_min_diff
        feature['cp_avg_diff'] = cp_avg_diff
        feature['cp_median_diff'] = cp_median_diff
        feature['cp_diff_first_click'] = cp_diff_first_click
        feature['cp_diff_last_click'] = cp_diff_last_click
        feature['cp_previous_diff'] = cp_previous_diff
        feature['cp_next_diff'] = cp_next_diff
        feature['cp_bf_usr_cnt'] = cp_bf_usr_cnt
        feature['cp_af_usr_cnt'] = cp_af_usr_cnt
        feature['cp_bf_usr_rate'] = cp_bf_usr_rate
        feature['cp_af_usr_rate'] = cp_af_usr_rate
        feature['cp_bf_mer_cnt'] = cp_bf_mer_cnt
        feature['cp_af_mer_cnt'] = cp_af_mer_cnt
        feature['cp_bf_mer_rate'] = cp_bf_mer_rate
        feature['cp_af_mer_rate'] = cp_af_mer_rate

        return feature

    '将dataframe遍历写成列表表达式，极大地提高速度'
    print('------user base start----------')
    usr_features = [get_base_usr(index,row) for index, row in label_tmp.iterrows()]
    usr_features = pd.DataFrame(usr_features)
    usr_features.fillna(-1, inplace=True)
    print('----user base finished-------')

    print('-------merchant base start--------')
    mer_features=[get_base_mer(index,row) for index,row in label_tmp.iterrows()]
    mer_features=pd.DataFrame(mer_features)
    mer_features.fillna(-1,inplace=True)
    print('-----merchant base finished---------')

    print('--------coupon base start----------')
    cp_features=[get_base_cp(index,row) for index,row in label_tmp.iterrows()]
    cp_features=pd.DataFrame(cp_features)
    cp_features.fillna(-1,inplace=True)
    print('--------coupon base finished--------')

    label = pd.concat([label, usr_features], axis=1)
    label = pd.concat([label,mer_features],axis=1)
    label = pd.concat([label,cp_features],axis=1)

    return label