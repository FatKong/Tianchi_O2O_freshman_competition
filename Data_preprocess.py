import pandas as pd

def mk_lable():
    ccf_offline_stage1_train = pd.read_csv(r'..\ccf_offline_stage1_train.csv')

    # 筛选出领取优惠券的用户,因为线上测试集的用户都领券了
    ccf_offline_stage1_train = ccf_offline_stage1_train[
        ccf_offline_stage1_train['Date_received'].isnull().values == False]

    # 筛选出是否使用优惠券消费的用户，即正负样本

    # 用户有领取优惠券但没有消费，负样本，标0
    part1 = ccf_offline_stage1_train[ccf_offline_stage1_train['Date'].isnull().values == True]
    part1['label'] = 0
    part1['Date_received'] = part1['Date_received'].map(lambda x: str(int(x)))
    part1['Date_received'] = pd.to_datetime(part1['Date_received'], format='%Y-%m-%d')
    part1['Date'] = pd.to_datetime(part1['Date'], format='%Y-%m-%d')

    # 用户在领取优惠券后15天内使用则为正样本（标1），否则为负样本（标0）
    part2 = ccf_offline_stage1_train[ccf_offline_stage1_train['Date'].isnull().values == False]

    part2['Date_received'] = part2['Date_received'].map(lambda x: str(int(x)))
    part2['Date_received'] = pd.to_datetime(part2['Date_received'], format='%Y-%m-%d')

    part2['Date'] = part2['Date'].map(lambda x: str(int(x)))
    part2['Date'] = pd.to_datetime(part2['Date'], format='%Y-%m-%d')

    part2['label'] = [0 if int(i.days) > 15 else 1 for i in (part2['Date'] - part2['Date_received'])]

    ccf_offline_stage1_train = part1.append(part2)
    print(ccf_offline_stage1_train)

    ccf_offline_stage1_train.to_csv(r'..\row_train.csv', index=False)
    pass

def split():
    '数据预处理及数据集划分'
    row_train = pd.read_csv(r'..\row_train.csv')

    row_train['Distance'] = row_train['Distance'].fillna(-1)

    row_train['Date_received'] = [str(i)[:10].replace('-', '') for i in row_train['Date_received']]
    row_train['Date_received'] = row_train['Date_received'].map(lambda x: int(x))

    row_train.rename(columns={'User_id': 'user_id',
                              'Merchant_id': 'merchant_id',
                              'Coupon_id': 'coupon_id',
                              'Discount_rate': 'discount_rate',
                              'Date_received': 'date_received',
                              'Distance': 'distance',
                              'Date': 'date'}, inplace=True)  # inplace=True可以在内存原地替换，节省内存

    def getrate(x):
        if len(x) == 2:
            x[0] = int(x[0])
            x[1] = int(x[1])
            tmp = (x[0] - x[1]) / x[0]
            return tmp
        else:
            return float(x[0])
        pass

    row_train['discount'] = row_train['discount_rate'].map(lambda x: x.split(':'))
    row_train['dis_left'] = row_train['discount'].map(lambda x: int(x[0]) if len(x) == 2 else -1)
    row_train['dis_right'] = row_train['discount'].map(lambda x: int(x[1]) if len(x) == 2 else -1)
    row_train['dis_rate'] = row_train['discount'].map(lambda x: getrate(x))
    del row_train['discount']

    '按照领券日期划分数据集'

    '训练集'
    train_feat = row_train[(row_train['date_received'] >= 20160401) & (row_train['date_received'] <= 20160530)]
    train_feat.to_csv(r'..\train\feat.csv', index=False)
    train_label = row_train[(row_train['date_received'] >= 20160601) & (row_train['date_received'] <= 20160630)]
    train_label.to_csv(r'..\train\label.csv', index=False)

    '验证集'
    val_feat = row_train[(row_train['date_received'] >= 20160301) & (row_train['date_received'] <= 20160430)]
    val_feat.to_csv(r'..\val\feat.csv', index=False)
    val_label = row_train[(row_train['date_received'] >= 20160501) & (row_train['date_received'] <= 20160530)]
    val_label.to_csv(r'..\val\label.csv', index=False)

    '预测集'
    test_feat = row_train[(row_train['date_received'] >= 20160501) & (row_train['date_received'] <= 20160630)]
    test_feat.to_csv(r'..\test\feat.csv', index=False)

    '线上提交区间数据处理'
    testlabel = pd.read_csv(r'..\ccf_offline_stage1_test_revised.csv')

    testlabel['Distance'] = testlabel['Distance'].fillna(-1)

    testlabel.rename(columns={'User_id': 'user_id',
                              'Merchant_id': 'merchant_id',
                              'Coupon_id': 'coupon_id',
                              'Discount_rate': 'discount_rate',
                              'Distance': 'distance',
                              'Date_received': 'date_received'
                              }, inplace=True)

    testlabel['discount'] = testlabel['discount_rate'].map(lambda x: x.split(':'))
    testlabel['dis_left'] = testlabel['discount'].map(lambda x: int(x[0]) if len(x) == 2 else -1)
    testlabel['dis_right'] = testlabel['discount'].map(lambda x: int(x[1]) if len(x) == 2 else -1)
    testlabel['dis_rate'] = testlabel['discount'].map(lambda x: getrate(x))
    del testlabel['discount']

    testlabel.to_csv(r'..\test\label.csv', index=False)

    pass