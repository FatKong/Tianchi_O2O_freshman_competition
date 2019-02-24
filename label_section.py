import pandas as pd
import numpy as np
def getcount(x):
    return x.count()
def getset(x):
    return len(set(x))

def LabelSection(label):
    'label区间特征'
    '-------------------------------------------用户特征----------------------------------------------------------------'

    '******1.用户 领取  优惠券的次数，种类，及种类占所有优惠券的比重*********'

    '1.1用户 领取  优惠券的次数，种类'
    luc_cnt_set = pd.pivot_table(label, index='user_id', values='coupon_id', aggfunc=[getcount, getset]).reset_index()
    luc_cnt_set.columns = ['user_id', 'luc_cnt', 'luc_set']
    label = pd.merge(label, luc_cnt_set, on='user_id', how='left')

    '1.2领取优惠券占所有优惠券比重'
    couponset = len(set(label['coupon_id']))
    label['lugetc_ratio'] = label['luc_set'] / couponset

    '*******2.用户 领取 商家的次数，种类 及种类占所有商家的比重**************'

    '2.1用户 领取 商家的 次数 种类'
    lum_set = pd.pivot_table(label, index='user_id', values='merchant_id', aggfunc=[getcount,getset]).reset_index()
    lum_set.columns = ['user_id', 'lum_cnt','lum_set']
    label = pd.merge(label, lum_set, on='user_id', how='left')

    '2.1占所有商家比重'
    merchantset = len(set(label['merchant_id']))
    label['lugetm_ratio'] = label['lum_set'] / merchantset

    '**************3.用户 领取 距离的 最大，最小， 平均******************'
    lucdis_stat = pd.pivot_table(label, index='user_id', values='distance', aggfunc=[np.max, np.min, np.mean]).reset_index()
    lucdis_stat.columns = ['user_id', 'luc_dismax', 'luc_dismin', 'luc_dismean']
    label = pd.merge(label, lucdis_stat, on='user_id', how='left')

    '**************4.用户 领取   折扣率，左值/右值 最大，最小，平均***********'
    ludis_stat = pd.pivot_table(label, index='user_id', values=['dis_left', 'dis_right'],
                       aggfunc=[np.max, np.min, np.mean]).reset_index()
    ludis_stat.columns = ['user_id', 'ludisleftmax', 'ludisrightmax', 'ludisleftmin', 'ludisrightmin', 'ludisleftmean',
                 'ludisrightmean']
    label = pd.merge(label, ludis_stat, on='user_id', how='left')

    '************5.用户 领取 折扣率 最大，最小，平均*********************'
    ludr_stat= pd.pivot_table(label, index='user_id', values='dis_rate', aggfunc=[np.max, np.min, np.mean]).reset_index()
    ludr_stat.columns = ['user_id', 'ludisratemax', 'ludisratemin', 'ludisratemean']
    label = pd.merge(label, ludr_stat, on='user_id', how='left')

    '**********6.用户 领取 左值0-50 50-200 200-500 的核销次数/率 （discount离散化）***********'
    label['disleft0_50'] = label['dis_left'].map(lambda x: 1 if x <= 50 else 0)
    label['disleft50_200'] = label['dis_left'].map(lambda x: 1 if (x > 50) & (x <= 200) else 0)
    label['disleft200_500'] = label['dis_left'].map(lambda x: 1 if x > 200 else 0)

    dis_stat = pd.pivot_table(label, index='user_id', values=['disleft0_50', 'disleft50_200', 'disleft200_500'],
                       aggfunc=np.sum).reset_index()
    dis_stat.columns = ['user_id', 'dis0_50_cnt', 'dis50_200_cnt', 'dis200_500_cnt']
    label = pd.merge(label, dis_stat, on='user_id', how='left')
    '---------------------------------------------商家特征-------------------------------------------------------------'
    '****1.商家被 领取/核销/不核销 优惠券次数，种类，及领取/核销比例，及种类占所有优惠券的比重*********'

    '1.1商家被 领取 优惠券次数及种类'
    lmc_cnt_set = pd.pivot_table(label, index='merchant_id', values='coupon_id', aggfunc=[getcount, getset]).reset_index()
    lmc_cnt_set.columns = ['merchant_id', 'lmc_cnt', 'lmc_set']
    label = pd.merge(label, lmc_cnt_set, on='merchant_id', how='left')

    '1.2领取的优惠券占所有优惠券的比重'
    label['lmgetc_ratio']=label['lmc_set']/couponset


    '*******************2.商家被 领取 用户数 ********************************'

    '2.1商家被 领取 用户数'
    lmu_cnt = pd.pivot_table(label, index='merchant_id', values='user_id', aggfunc=getset).reset_index()
    lmu_cnt.columns = ['merchant_id', 'lmu_cnt']
    label = pd.merge(label, lmu_cnt, on='merchant_id', how='left')


    '**********3.商家被 领取 距离，最大，最小，平均***************************'

    '3.1商家被 领取 距离，最大，最小，平均'
    lmc_dist_stat = pd.pivot_table(label, index='merchant_id', values='distance',
                                        aggfunc=[np.max, np.min, np.mean]).reset_index()
    lmc_dist_stat.columns = ['merchant_id', 'lmc_distmax', 'lmc_distmin', 'lmc_distmean']
    label = pd.merge(label, lmc_dist_stat, on='merchant_id', how='left')

    '*********4.商家被 领取 折扣率，左值/右值 最大，最小，平均*******************'

    '4.1商家被 领取 折扣率，左值/右值 最大，最小，平均'
    lmc_disc_stat = pd.pivot_table(label, index='merchant_id', values=['dis_left', 'dis_right'],
                                 aggfunc=[np.max, np.min, np.mean]).reset_index()
    lmc_disc_stat.columns = ['merchant_id', 'lmcdisleftmax', 'lmcdisrightmax', 'lmcdisleftmin', 'lmcdisrightmin',
                           'lmcdisleftmean','lmcdisrightmean']
    label = pd.merge(label, lmc_disc_stat, on='merchant_id', how='left')

    '**********5.商家被 领取 折扣率 最大，最小，平均******************************'

    '5.1商家被 领取 折扣率  最大，最小，平均'
    lmc_dr_stat = pd.pivot_table(label, index='merchant_id', values='dis_rate',
                                aggfunc=[np.max, np.min, np.mean]).reset_index()
    lmc_dr_stat.columns = ['merchant_id', 'lmcdisratemax', 'lmcdisratemin', 'lmcdisratemean']
    label = pd.merge(label, lmc_dr_stat, on='merchant_id', how='left')

    '--------------------------------------------优惠券特征------------------------------------------------------------'

    '1.优惠券被 领取 次数及用户数'
    lcu_cnt_set = pd.pivot_table(label, index='coupon_id', values='user_id', aggfunc=[getcount, getset]).reset_index()
    lcu_cnt_set.columns = ['coupon_id', 'lcu_cnt', 'lcu_set']
    label = pd.merge(label, lcu_cnt_set, on='coupon_id', how='left')

    '2.优惠券 距离  最大/最小/平均'
    c_dist_stat=pd.pivot_table(label,index='coupon_id',values='distance',aggfunc=[np.max, np.min, np.mean]).reset_index()
    c_dist_stat.columns = ['merchant_id', 'lc_distmax', 'lc_distmin', 'lc_distmean']
    label = pd.merge(label, c_dist_stat, on='merchant_id', how='left')


    '-------------------------------------------用户*商家特征---------------------------------------------------------'
    '1.1用户商家 领取 次数'
    luminc_cnt = pd.pivot_table(label, index=['user_id', 'merchant_id'], values='coupon_id',
                               aggfunc='count').reset_index()
    luminc_cnt.columns = ['user_id', 'merchant_id', 'lUMinC_cnt']
    label = pd.merge(label, luminc_cnt, on=['user_id', 'merchant_id'], how='left')

    '------------------------------------------用户*优惠券特征---------------------------------------------------------'
    '1.1用户优惠券 领取 次数'
    lunin_cnt = pd.pivot_table(label, index=['user_id', 'coupon_id'], values='date_received',
                              aggfunc='count').reset_index()
    lunin_cnt.columns = ['user_id', 'coupon_id', 'lucin_cnt']
    label = pd.merge(label, lunin_cnt, on=['user_id', 'coupon_id'], how='left')

    '---------------------------------------------排序特征-------------------------------------------------------------'
    '                               (排序特征应该是转化率类比赛最强特征之一)                                              '
    '*************1.用户与距离，领券时间，优惠券左值/右值/折扣率排序(正倒序)**********************'

    '1.1用户与距离排序'
    label['UdisrankF']=label.groupby('user_id')['distance'].rank(ascending=False)
    label['UdisrankT']=label.groupby('user_id')['distance'].rank(ascending=True)

    '1.2用户与领券时间排序'
    label['UdaterankF']=label.groupby('user_id')['date_received'].rank(ascending=False)
    label['UdaterankT']=label.groupby('user_id')['date_received'].rank(ascending=True)

    '1.3用户与优惠券左值排序'
    label['UdisleftrankF']=label.groupby('user_id')['dis_left'].rank(ascending=False)
    label['UdisleftrankT']=label.groupby('user_id')['dis_left'].rank(ascending=True)

    '1.4用户与优惠券右值排序'
    label['UdisrightrankF']=label.groupby('user_id')['dis_right'].rank(ascending=False)
    label['UdisrightrankT']=label.groupby('user_id')['dis_right'].rank(ascending=True)

    '*************2.商家与距离，领券时间，优惠券左值/右值/折扣率排序(正倒序)********************'

    '2.1商家与距离排序'
    label['MdisrankF']=label.groupby('merchant_id')['distance'].rank(ascending=False)
    label['MdisrankT'] = label.groupby('merchant_id')['distance'].rank(ascending=True)

    '2.2用户与领券时间排序'
    label['MdaterankF']=label.groupby('merchant_id')['date_received'].rank(ascending=False)
    label['MdaterankT']=label.groupby('merchant_id')['date_received'].rank(ascending=True)

    '2.3商家与优惠券左值排序'
    label['MdisleftrankF']=label.groupby('merchant_id')['dis_left'].rank(ascending=False)
    label['MdisleftrankT']=label.groupby('merchant_id')['dis_left'].rank(ascending=True)

    '2.4商家与优惠券右值排序'
    label['MdisrightrankF']=label.groupby('merchant_id')['dis_right'].rank(ascending=False)
    label['MdisrightrankT']=label.groupby('merchant_id')['dis_right'].rank(ascending=True)

    '*************3.优惠券与距离，领券时间，优惠券左值/右值/折扣率排序(正倒序)********************'

    '3.1优惠券与距离排序'
    label['CdisrankF']=label.groupby('coupon_id')['distance'].rank(ascending=False)
    label['CdisrankT']=label.groupby('coupon_id')['distance'].rank(ascending=True)

    '3.2优惠券与领券时间排序'
    label['CdaterankF']=label.groupby('coupon_id')['date_received'].rank(ascending=False)
    label['CdaterankT']=label.groupby('coupon_id')['date_received'].rank(ascending=True)

    '3.3优惠券与优惠券左值排序'
    label['CdisleftrankF']=label.groupby('coupon_id')['dis_left'].rank(ascending=False)
    label['CdisleftrankT']=label.groupby('coupon_id')['dis_left'].rank(ascending=True)

    '3.4优惠券与优惠券右值排序'
    label['CdisrightrankF']=label.groupby('coupon_id')['dis_right'].rank(ascending=False)
    label['CdisrightrankT']=label.groupby('coupon_id')['dis_right'].rank(ascending=True)

    '*******************************4.用户 商家 联合 排序特征*******************************************'
    '4.1用户与距离排序'
    label['umdistrankF'] = label.groupby(['user_id','merchant_id'])['distance'].rank(ascending=False)
    label['umdistrankT'] = label.groupby(['user_id','merchant_id'])['distance'].rank(ascending=True)

    '4.2用户与领券时间排序'
    label['umdaterankF'] = label.groupby(['user_id','merchant_id'])['date_received'].rank(ascending=False)
    label['umdaterankT'] = label.groupby(['user_id','merchant_id'])['date_received'].rank(ascending=True)

    '4.3用户与优惠券左值排序'
    label['umdisleftrankF'] = label.groupby(['user_id','merchant_id'])['dis_left'].rank(ascending=False)
    label['umdisleftrankT'] = label.groupby(['user_id','merchant_id'])['dis_left'].rank(ascending=True)

    '4.4用户与优惠券右值排序'
    label['umdisrightrankF'] = label.groupby(['user_id','merchant_id'])['dis_right'].rank(ascending=False)
    label['umdisrightrankT'] = label.groupby(['user_id','merchant_id'])['dis_right'].rank(ascending=True)

    '**************************5.用户 优惠券 联合 排序特征************************************************'

    '5.1用户与距离排序'
    label['ucdisrankF']=label.groupby(['user_id','coupon_id'])['distance'].rank(ascending=False)
    label['UdisrankT']=label.groupby(['user_id','coupon_id'])['distance'].rank(ascending=True)

    '5.2用户与领券时间排序'
    label['ucdaterankF']=label.groupby(['user_id','coupon_id'])['date_received'].rank(ascending=False)
    label['ucdaterankT']=label.groupby(['user_id','coupon_id'])['date_received'].rank(ascending=True)

    '5.3用户与优惠券左值排序'
    label['ucdisleftrankF']=label.groupby(['user_id','coupon_id'])['dis_left'].rank(ascending=False)
    label['ucdisleftrankT']=label.groupby(['user_id','coupon_id'])['dis_left'].rank(ascending=True)

    '5.4用户与优惠券右值排序'
    label['ucdisrightrankF']=label.groupby(['user_id','coupon_id'])['dis_right'].rank(ascending=False)
    label['ucdisrightrankT']=label.groupby(['user_id','coupon_id'])['dis_right'].rank(ascending=True)

    '------------------------------------------时间特征---------------------------------------------------------------'
    label['date_received'] = label['date_received'].map(
        lambda x: datetime.datetime.strptime(str(x), "%Y%m%d"))

    '1.是否周末'
    label['ifweekend'] = label['date_received'].map(
        lambda x: 1 if (datetime.date.isoweekday(x) == 6) | (datetime.date.isoweekday(x) == 7) else 0
    )

    '2.是否周六'
    label['ifSat'] = label['date_received'].map(
        lambda x: 1 if datetime.date.isoweekday(x) == 6 else 0
    )

    '3.是否周日'
    label['ifSun'] = label['date_received'].map(
        lambda x: 1 if datetime.date.isoweekday(x) == 7 else 0
    )

    '4.是否工作日'
    label['ifweekday'] = label['ifweekend'].map(
        lambda x: 1 if x == 0 else 0
    )

    '5.是否上旬'
    label['first_ten_day']=label['date_received'].map(
        lambda x:1 if (x.day>=1)&(x.day<=10) else 0
    )

    '6.是否中旬'
    label['second_ten_day'] = label['date_received'].map(
        lambda x: 1 if (x.day >=11) & (x.day <= 20) else 0
    )

    '7.是否下旬'
    label['third_ten_day'] = label['date_received'].map(
        lambda x: 1 if (x.day >= 21) & (x.day <= 31) else 0
    )

    '8.是否五一'
    label['if51']=label['date_received'].map(
        lambda x: 1 if (x.month==5)&(x.day==1) else 0
    )

    '9.是否六一'
    label['if61']=label['date_received'].map(
        lambda x:1 if (x.month==6)&(x.day==1) else 0
    )

    '10.是否端午6.9'
    label['ifDuanWu']=label['date_received'].map(
        lambda x:1 if (x.month==6)&(x.day==9) else 0
    )

    '11.是否母亲节5.8'
    label['ifMomDay']=label['date_received'].map(
        lambda x:1 if (x.month==5)&(x.day==8) else 0
    )

    '12.是否父亲节6.19'
    label['ifDadyDay']=label['date_received'].map(
        lambda x:1 if (x.month==6)&(x.day==19) else 0
    )

    '13.是否夏至6.21'
    label['SummerSol']=label['date_received'].map(
        lambda x:1 if (x.month==6)&(x.day==21) else 0
    )

    return label
    pass
