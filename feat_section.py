import pandas as pd
import numpy as np
def getcount(x):
    return x.count()
def getset(x):
    return len(set(x))

def FeatSection(data, label):
    'Feature区间特征'

    '--------------------------------------------用户特征--------------------------------------------------------------'

    '********1.用户 领取/核销/不核销 优惠券的次数，种类，及领取/核销比例，及领取优惠券种类占所有优惠券的比重*********'

    '1.1用户领取的优惠券次数及种类'
    uc_cnt_set = pd.pivot_table(data, index='user_id', values='coupon_id', aggfunc=[getcount, getset]).reset_index()
    uc_cnt_set.columns = ['user_id', 'UC_cnt', 'UC_set']
    label = pd.merge(label, uc_cnt_set, on='user_id', how='left')

    usecp = data[data['date'].isnull() == False]  # 核销优惠券的数据
    dropcp = data[data['date'].isnull() == True]  # 不核销优惠券的数据

    '1.2用户核销优惠券的次数及种类'
    uuseC_cnt_set = pd.pivot_table(usecp, index='user_id', values='coupon_id', aggfunc=[getcount, getset]).reset_index()
    uuseC_cnt_set.columns = ['user_id', 'UuseC_cnt', 'UuseC_set']
    label = pd.merge(label, uuseC_cnt_set, on='user_id', how='left')

    '1.3用户不核销优惠券的次数及种类'
    udropc_cnt_set = pd.pivot_table(dropcp, index='user_id', values='coupon_id',
                                    aggfunc=[getcount, getset]).reset_index()
    udropc_cnt_set.columns = ['user_id', 'UdropC_cnt', 'UdropC_set']
    label = pd.merge(label, udropc_cnt_set, on='user_id', how='left')

    '1.4用户核销/领取比'
    label['UuseC_ratio'] = label['UuseC_cnt'] / label['UC_cnt']

    '1.5领取优惠券种类占所有种类的比例'
    couponset = len(set(data['coupon_id']))
    label['UgetC_ratio'] = label['UC_set'] / couponset

    '********2.用户 领取/核销/不核销 商家的种类， 及领取/核销比例， 及领券商家种类占所有商家的比重********'

    '2.1用户领取商家种类'
    um_set = pd.pivot_table(data, index='user_id', values='merchant_id', aggfunc=getset).reset_index()
    um_set.columns = ['user_id', 'UM_set']
    label = pd.merge(label, um_set, on='user_id', how='left')

    '2.2用户核销的商家种类'
    uusem_set = pd.pivot_table(usecp, index='user_id', values='merchant_id', aggfunc=getset).reset_index()
    uusem_set.columns = ['user_id', 'UuseM_set']
    label = pd.merge(label, uusem_set, on='user_id', how='left')

    '2.3用户不核销的商家种类'
    udropm_set = pd.pivot_table(dropcp, index='user_id', values='merchant_id', aggfunc=getset).reset_index()
    udropm_set.columns = ['user_id', 'UdropM_set']
    label = pd.merge(label, udropm_set, on='user_id', how='left')

    '2.4用户核销/领取商家比'
    label['UuseM_ratio'] = label['UuseM_set'] / label['UM_set']

    '2.5领券商家占所有商家的比重'
    merchantset = len(set(data['merchant_id']))
    label['UgetM_ratio'] = label['UM_set'] / merchantset

    '**********3.用户 领取/核销/不核销 距离的 最大，最小，平均 *************'

    '3.1用户领券 距离 最大，最小，平均'
    uc_dismax_dismin_dismean = pd.pivot_table(data, index='user_id', values='distance',
                                              aggfunc=[np.max, np.min, np.mean]).reset_index()
    uc_dismax_dismin_dismean.columns = ['user_id', 'UC_dismax', 'UC_dismin', 'UC_dismean']
    label = pd.merge(label, uc_dismax_dismin_dismean, on='user_id', how='left')

    '3.2用户核销 距离 最大，最小，平均'
    uusec_dismax_min_mean = pd.pivot_table(usecp, index='user_id', values='distance',
                                           aggfunc=[np.max, np.min, np.mean]).reset_index()
    uusec_dismax_min_mean.columns = ['user_id', 'UuseC_dismax', 'UuseC_dismin', 'UuseC_dismean']
    label = pd.merge(label, uusec_dismax_min_mean, on='user_id', how='left')

    '3.3用户不核销 距离 最大，最小，平均'
    udropc_dismax_min_mean = pd.pivot_table(dropcp, index='user_id', values='distance',
                                            aggfunc=[np.max, np.min, np.mean]).reset_index()
    udropc_dismax_min_mean.columns = ['user_id', 'UdropC_dismax', 'UdropC_dismin', 'UdropC_dismean']
    label = pd.merge(label, udropc_dismax_min_mean, on='user_id', how='left')

    '***********4.用户 领取/核销/不核销 折扣率，左值/右值 最大，最小，平均***********'

    '4.1用户 领券 折扣率 左值/右值 最大，最小，平均'
    disc_get_stat = pd.pivot_table(data, index='user_id', values=['dis_left', 'dis_right'],
                                   aggfunc=[np.max, np.min, np.mean]).reset_index()
    disc_get_stat.columns = ['user_id', 'disleftmax', 'disrightmax', 'disleftmin', 'disrightmin', 'disleftmean',
                             'disrightmean']
    label = pd.merge(label, disc_get_stat, on='user_id', how='left')

    '4.2用户 核销 折扣率 左值/右值 最大，最小，平均'
    disc_use_stat = pd.pivot_table(usecp, index='user_id', values=['dis_left', 'dis_right'],
                                   aggfunc=[np.max, np.min, np.mean]).reset_index()
    disc_use_stat.columns = ['user_id', 'UuseCdisleftmax', 'UuseCdisrightmax', 'UuseCdisleftmin', 'UuseCdisrightmin',
                             'UuseCdisleftmean', 'UuseCdisrightmean']
    label = pd.merge(label, disc_use_stat, on='user_id', how='left')

    '4.3用户 不核销 折扣率 左值/右值 最大，最小，平均'
    disc_drop_stat = pd.pivot_table(dropcp, index='user_id', values=['dis_left', 'dis_right'],
                                    aggfunc=[np.max, np.min, np.mean]).reset_index()
    disc_drop_stat.columns = ['user_id', 'UdropCdisleftmax', 'UdropCdisrightmax', 'UdropCdisleftmin',
                              'UdropCdisrightmin',
                              'UdropCdisleftmean', 'UdropCdisrightmean']
    label = pd.merge(label, disc_drop_stat, on='user_id', how='left')

    '4.3用户 领取 折扣率 最大，最小，平均'
    ucdr_max_min_mean = pd.pivot_table(data, index='user_id', values='dis_rate',
                                       aggfunc=[np.max, np.min, np.mean]).reset_index()
    ucdr_max_min_mean.columns = ['user_id', 'UCdisratemax', 'UCdisratemin', 'UCdisratemean']
    label = pd.merge(label, ucdr_max_min_mean, on='user_id', how='left')

    '4.4用户 核销 折扣率 最大，最小，平均'
    uusedrmax_min_mean = pd.pivot_table(usecp, index='user_id', values='dis_rate',
                                        aggfunc=[np.max, np.min, np.mean]).reset_index()
    uusedrmax_min_mean.columns = ['user_id', 'UuseCdisratemax', 'UuseCdisratemin', 'UuseCdisratemean']
    label = pd.merge(label, uusedrmax_min_mean, on='user_id', how='left')

    '4.5用户 不核销 折扣率 最大，最小，平均'
    udropdrmax_min_mean = pd.pivot_table(dropcp, index='user_id', values='dis_rate',
                                         aggfunc=[np.max, np.min, np.mean]).reset_index()
    udropdrmax_min_mean.columns = ['user_id', 'UdropCdisratemax', 'UdropCdisratemin', 'UdropCdisratemean']
    label = pd.merge(label, udropdrmax_min_mean, on='user_id', how='left')

    '**********5.用户 领取/核销/不核销 左值0-50 50-200 200-500 的核销次数/率 （discount离散化）*************'

    '-----------------------------------------------商家特征-----------------------------------------------------------'

    '****1.商家被 领取/核销/不核销 优惠券次数，种类，及领取/核销比例，及种类占所有优惠券的比重*********'

    '1.1商家被 领取 优惠券次数及种类'
    mc_cnt_set = pd.pivot_table(data, index='merchant_id', values='coupon_id', aggfunc=[getcount, getset]).reset_index()
    mc_cnt_set.columns = ['merchant_id', 'MC_cnt', 'MC_set']
    label = pd.merge(label, mc_cnt_set, on='merchant_id', how='left')

    '1.2商家被 核销 优惠券次数及种类'
    museC_cnt_set = pd.pivot_table(usecp, index='merchant_id', values='coupon_id',
                                   aggfunc=[getcount, getset]).reset_index()
    museC_cnt_set.columns = ['merchant_id', 'MuseC_cnt', 'MuseC_set']
    label = pd.merge(label, museC_cnt_set, on='merchant_id', how='left')

    '1.3商家被 不核销 优惠券次数及种类'
    mdropC_cnt_set = pd.pivot_table(dropcp, index='merchant_id', values='coupon_id',
                                    aggfunc=[getcount, getset]).reset_index()
    mdropC_cnt_set.columns = ['merchant_id', 'MdropC_cnt', 'MdropC_set']
    label = pd.merge(label, mdropC_cnt_set, on='merchant_id', how='left')

    '1.4商家 核销/领取比'
    label['MuseC_rate'] = label['MuseC_cnt'] / label['MC_cnt']

    '********2.商家被 领取/核销/不核销 用户数，及平均每个用户核销多少张********'

    '2.1商家被 领取 用户数'
    mu_cnt = pd.pivot_table(data, index='merchant_id', values='user_id', aggfunc=getset).reset_index()
    mu_cnt.columns = ['merchant_id', 'MU_cnt']
    label = pd.merge(label, mu_cnt, on='merchant_id', how='left')

    '2.2商家被 核销 用户数'
    museu_cnt = pd.pivot_table(usecp, index='merchant_id', values='user_id', aggfunc=getset).reset_index()
    museu_cnt.columns = ['merchant_id', 'MuseU_cnt']
    label = pd.merge(label, museu_cnt, on='merchant_id', how='left')

    '2.3商家被 不核销 用户数'
    mdropu_cnt = pd.pivot_table(dropcp, index='merchant_id', values='user_id', aggfunc=getset).reset_index()
    mdropu_cnt.columns = ['merchant_id', 'MdropU_cnt']
    label = pd.merge(label, mdropu_cnt, on='merchant_id', how='left')

    '**********3.商家被 领取/核销/不核销 距离，最大，最小，平均***************'

    '3.1商家被 领取 距离，最大，最小，平均'
    mc_dismax_min_mean = pd.pivot_table(data, index='merchant_id', values='distance',
                                        aggfunc=[np.max, np.min, np.mean]).reset_index()
    mc_dismax_min_mean.columns = ['merchant_id', 'MC_dismax', 'MC_dismin', 'MC_dismean']
    label = pd.merge(label, mc_dismax_min_mean, on='merchant_id', how='left')

    '3.2商家被 核销 距离，最大，最小，平均'
    musec_dis_stat = pd.pivot_table(usecp, index='merchant_id', values='distance',
                                    aggfunc=[np.max, np.min, np.mean]).reset_index()
    musec_dis_stat.columns = ['merchant_id', 'MuseC_dismax', 'MuseC_dismin', 'MuseC_dismean']
    label = pd.merge(label, musec_dis_stat, on='merchant_id', how='left')

    '3.3商家被 不核销 距离，最大，最小，平均'
    mdropc_dis_stat = pd.pivot_table(dropcp, index='merchant_id', values='distance',
                                     aggfunc=[np.max, np.min, np.mean]).reset_index()
    mdropc_dis_stat.columns = ['merchant_id', 'MdropC_dismax', 'MdropC_dismin', 'MdropC_dismean']
    label = pd.merge(label, mdropc_dis_stat, on='merchant_id', how='left')

    '***************4.商家被 领取/核销/不核销 折扣率，左值/右值 最大，最小，平均*******************'

    '4.1商家被 领取 折扣率，左值/右值 最大，最小，平均'
    mc_dis_stat = pd.pivot_table(data, index='merchant_id', values=['dis_left', 'dis_right'],
                                 aggfunc=[np.max, np.min, np.mean]).reset_index()
    mc_dis_stat.columns = ['merchant_id', 'MCdisleftmax', 'MCdisrightmax', 'MCdisleftmin', 'MCdisrightmin',
                           'MCdisleftmean',
                           'MCdisrightmean']
    label = pd.merge(label, mc_dis_stat, on='merchant_id', how='left')

    '4.2商家被 核销 折扣率，左值/右值 最大，最小，平均'
    musec_dr_stat = pd.pivot_table(usecp, index='merchant_id', values=['dis_left', 'dis_right'],
                                   aggfunc=[np.max, np.min, np.mean]).reset_index()
    musec_dr_stat.columns = ['merchant_id', 'MuseCdisleftmax', 'MuseCdisrightmax', 'MuseCdisleftmin',
                             'MuseCdisrightmin',
                             'MuseCdisleftmean', 'MuseCdisrightmean']
    label = pd.merge(label, musec_dr_stat, on='merchant_id', how='left')

    '4.3商家被 不核销 折扣率，左值/右值 最大，最小，平均'
    mdroc_dr_stat = pd.pivot_table(dropcp, index='merchant_id', values=['dis_left', 'dis_right'],
                                   aggfunc=[np.max, np.min, np.mean]).reset_index()
    mdroc_dr_stat.columns = ['merchant_id', 'MdropCdisleftmax', 'MdropCdisrightmax', 'MdropCdisleftmin',
                             'MdropCdisrightmin',
                             'MdropCdisleftmean', 'MdropCdisrightmean']
    label = pd.merge(label, mdroc_dr_stat, on='merchant_id', how='left')

    '**********5.商家被 领取/核销/不核销 折扣率 最大，最小，平均**********************'

    '5.1商家被 领取 折扣率  最大，最小，平均'
    mc_dr_stat = pd.pivot_table(data, index='merchant_id', values='dis_rate',
                                aggfunc=[np.max, np.min, np.mean]).reset_index()
    mc_dr_stat.columns = ['merchant_id', 'MCdisratemax', 'MCdisratemin', 'MCdisratemean']
    label = pd.merge(label, mc_dr_stat, on='merchant_id', how='left')

    '5.2商家被 核销 折扣率  最大，最小，平均'
    musec_dr_stat = pd.pivot_table(usecp, index='merchant_id', values='dis_rate',
                                   aggfunc=[np.max, np.min, np.mean]).reset_index()
    musec_dr_stat.columns = ['merchant_id', 'MuseCdisratemax', 'MuseCdisratemin', 'MuseCdisratemean']
    label = pd.merge(label, musec_dr_stat, on='merchant_id', how='left')

    '5.3商家被 不核销 折扣率  最大，最小，平均'
    mdropc_dr_stat = pd.pivot_table(dropcp, index='merchant_id', values='dis_rate',
                                    aggfunc=[np.max, np.min, np.mean]).reset_index()
    mdropc_dr_stat.columns = ['merchant_id', 'MdropCdisratemax', 'MdropCdisratemin', 'MdropCdisratemean']
    label = pd.merge(label, mdropc_dr_stat, on='merchant_id', how='left')

    '-------------------------------------------------优惠券特征--------------------------------------------------------'
    '********************1.优惠券 领取/核销/不核销 次数 用户数*********************'
    '1.1优惠券被 领取 次数及用户数'
    cu_cnt_set = pd.pivot_table(data, index='coupon_id', values='user_id', aggfunc=[getcount, getset]).reset_index()
    cu_cnt_set.columns = ['coupon_id', 'CU_cnt', 'CU_set']
    label = pd.merge(label, cu_cnt_set, on='coupon_id', how='left')

    '1.2优惠券被 核销 次数及用户数'
    cusec_cnt_set = pd.pivot_table(usecp, index='coupon_id', values='user_id', aggfunc=[getcount, getset]).reset_index()
    cusec_cnt_set.columns = ['coupon_id', 'CuseU_cnt', 'CuseU_set']
    label = pd.merge(label, cusec_cnt_set, on='coupon_id', how='left')

    '1.3优惠券被 不核销 次数及用户数'
    cdropu_cnt_set = pd.pivot_table(dropcp, index='coupon_id', values='user_id',
                                    aggfunc=[getcount, getset]).reset_index()
    cdropu_cnt_set.columns = ['coupon_id', 'CdropU_cnt', 'CdropU_set']
    label = pd.merge(label, cdropu_cnt_set, on='coupon_id', how='left')

    '4.优惠券 核销/领取次数比'
    label['CuseU_rate'] = label['CuseU_cnt'] / label['CU_cnt']

    '***********************2.优惠券 领取/核销/不核销 距离  最大/最小/平均**********************'
    '2.1优惠券 领取 距离 最大/最小/平均'
    c_dist_stat = pd.pivot_table(label, index='coupon_id', values='distance',
                                 aggfunc=[np.max, np.min, np.mean]).reset_index()
    c_dist_stat.columns = ['coupon_id', 'c_distmax', 'c_distmin', 'c_distmean']
    label = pd.merge(label, c_dist_stat, on='coupon_id', how='left')

    '2.2优惠券 核销 距离 最大/最小/平均'
    cuse_dist_stat = pd.pivot_table(label, index='coupon_id', values='distance',
                                 aggfunc=[np.max, np.min, np.mean]).reset_index()
    cuse_dist_stat.columns = ['coupon_id', 'cuse_distmax', 'cuse_distmin', 'cuse_distmean']
    label = pd.merge(label, cuse_dist_stat, on='coupon_id', how='left')

    '2.3优惠券 不核销 距离 最大/最小/平均'
    cdrop_dist_stat = pd.pivot_table(label, index='coupon_id', values='distance',
                                    aggfunc=[np.max, np.min, np.mean]).reset_index()
    cdrop_dist_stat.columns = ['coupon_id', 'cdrop_distmax', 'cdrop_distmin', 'cdrop_distmean']
    label = pd.merge(label, cdrop_dist_stat, on='coupon_id', how='left')

    '---------------------------------------------用户*商家特征--------------------------------------------------------'

    '*************1.用户商家 领取/核销/不核销 次数，领取/核销比*************'

    '1.1用户商家 领取 次数'
    uminc_cnt = pd.pivot_table(data, index=['user_id', 'merchant_id'], values='coupon_id',
                               aggfunc='count').reset_index()
    uminc_cnt.columns = ['user_id', 'merchant_id', 'UMinC_cnt']
    label = pd.merge(label, uminc_cnt, on=['user_id', 'merchant_id'], how='left')

    '1.2用户商家 核销 次数'
    umincuse_cnt = pd.pivot_table(usecp, index=['user_id', 'merchant_id'], values='coupon_id',
                                  aggfunc='count').reset_index()
    umincuse_cnt.columns = ['user_id', 'merchant_id', 'UMinCuse_cnt']
    label = pd.merge(label, umincuse_cnt, on=['user_id', 'merchant_id'], how='left')

    '1.3用户商家 不核销 次数'
    umincdrop = pd.pivot_table(usecp, index=['user_id', 'merchant_id'], values='coupon_id',
                               aggfunc='count').reset_index()
    umincdrop.columns = ['user_id', 'merchant_id', 'UMinCdrop_cnt']
    label = pd.merge(label, umincdrop, on=['user_id', 'merchant_id'], how='left')

    '1.4用户商家 核销/领取比'
    label['UMinC_rate'] = label['UMinCuse_cnt'] / label['UMinC_cnt']

    '***********2.用户商家 核销/不核销 次数 占 总的核销/不核销比重*************'

    '2.1用户商家 核销/总核销'
    label['UMin_get/sum'] = label['UMinCuse_cnt'] / label['UuseC_cnt']

    '2.2用户商家 不核销/总不核销'
    label['UMin_drop/sum'] = label['UMinCdrop_cnt'] / label['UdropC_cnt']

    '------------------------------------------用户*优惠券特征---------------------------------------------------------'

    '***********1.用户优惠券 领取/核销/不核销 次数，领取/核销比***************'

    '1.1用户优惠券 领取 次数'
    unin_cnt = pd.pivot_table(data, index=['user_id', 'coupon_id'], values='date_received',
                              aggfunc='count').reset_index()
    unin_cnt.columns = ['user_id', 'coupon_id', 'UCin_cnt']
    label = pd.merge(label, unin_cnt, on=['user_id', 'coupon_id'], how='left')

    '1.2用户优惠券 核销 次数'
    ucin_use = pd.pivot_table(usecp, index=['user_id', 'coupon_id'], values='date_received',
                              aggfunc='count').reset_index()
    ucin_use.columns = ['user_id', 'coupon_id', 'UCin_use']
    label = pd.merge(label, ucin_use, on=['user_id', 'coupon_id'], how='left')

    '1.3用户优惠券 不核销 次数'
    ucin_drop = pd.pivot_table(dropcp, index=['user_id', 'coupon_id'], values='date_received',
                               aggfunc='count').reset_index()
    ucin_drop.columns = ['user_id', 'coupon_id', 'UCin_drop']
    label = pd.merge(label, ucin_drop, on=['user_id', 'coupon_id'], how='left')

    '1.4用户优惠券 核销/领取比'
    label['UCin_rate'] = label['UCin_use'] / label['UCin_cnt']

    '***********2.用户优惠券 核销/不核销 次数 占 总的核销/不核销比重***********'

    '2.1用户优惠券核销/总核销比'
    label['UCin_userate'] = label['UCin_use'] / label['UuseC_cnt']

    '2.2用户优惠券不核销/总不核销比'
    label['UCin_droprate'] = label['UCin_drop'] / label['UdropC_cnt']

    return label
    pass
