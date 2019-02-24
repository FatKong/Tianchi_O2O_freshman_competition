import pandas as pd
import xgboost as xgb
from xgboost import plot_importance
import lightgbm as lgb
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFE
def XgbTest(train, test):
    train_y = train['label']
    train_x = train.drop(['user_id', 'merchant_id', 'coupon_id', 'discount_rate', 'date_received', 'date', 'label'],
                         axis=1)

    test_id = test[['user_id', 'coupon_id', 'date_received']]
    test_x = test.drop(['user_id', 'merchant_id', 'coupon_id', 'discount_rate', 'date_received'], axis=1)

    xgb_train = xgb.DMatrix(train_x, label=train_y.values)
    xgb_test = xgb.DMatrix(test_x)

    params = {'booster': 'gbtree',
              'objective': 'binary:logistic',  # rank:pairwise binary:logistic
              'eta': '0.01',
              'eval_metric': 'auc',
              'subsample': 0.8,
              'colsample_bytree': 0.8,
              'scale_pos_weight': 1,
              'min_child_weight': 18,
              # 'max_delta_step':10
              }
    model = xgb.train(params, xgb_train, num_boost_round=1200)
    result = model.predict(xgb_test)
    test_id['Probability'] = result

    test_id.rename(columns={'user_id': 'User_id',
                            'coupon_id': 'Coupon_id',
                            'date_received': 'Date_received'}, inplace=True)

    test_id.to_csv(r'..\xgb.csv', index=False)

    plot_importance(model)
    plt.show()
    pass
def LgbTest(train, test):
    train_y = train[['label']]
    train_x = train.drop(['user_id', 'merchant_id', 'coupon_id', 'discount_rate', 'date_received', 'date', 'label'],
                         axis=1)

    test_id = test[['user_id', 'coupon_id', 'date_received']]
    test_x = test.drop(['user_id', 'merchant_id', 'coupon_id', 'discount_rate', 'date_received'], axis=1)

    '特征确定'
    feat_select = pd.read_csv(r'..\feat_select.csv')
    feat_select = feat_select.head(180)
    feat_select = feat_select['selected feat'].tolist()
    train_x=train_x[feat_select]
    test_x=test_x[feat_select]

    feat_names = list(train_x.columns.values)

    lgb_train = lgb.Dataset(train_x.values, label=train_y['label'].tolist())
    params = {'boosting_type': 'gbdt',
              'objective': 'binary',
              'metric': 'auc',
              'learning_rate': 0.01,
              # 'min_child_weight': 10,
              # 'feature_fraction': 0.8,
              # 'min_split_gain': 0.1,
              'silent': True
              }
    gbm = lgb.train(params, train_set=lgb_train, num_boost_round=800)
    result = gbm.predict(test_x)

    test_id['Probability'] = result

    test_id.rename(columns={'user_id': 'User_id',
                            'coupon_id': 'Coupon_id',
                            'date_received': 'Date_received'}, inplace=True)

    test_id['Date_received'] = [str(i)[:10].replace('-', '') for i in test_id['Date_received']]
    test_id['Date_received'] = test_id['Date_received'].map(lambda x: int(x))

    test_id['Probability']=test_id['Probability'].map(lambda x:x*0.98)
    test_id.to_csv(r'..\lgb.csv', index=False)

    feat_imp = pd.DataFrame({
        'feat_names': feat_names,
        'importance': gbm.feature_importance(),
    }).sort_values(by='importance')

    feat_imp.plot(x='feat_names', kind='barh')
    plt.show()
    feat_imp.to_csv(r'..\lgb_feat.csv',index=False)
    pass
def featselect():
    train = pd.read_csv(r'..\train.csv')
    # val = pd.read_csv(r'..\val.csv')
    # train_val = pd.concat([train, val], axis=0)
    train_y = train[['label']]
    train_x = train.drop(['user_id', 'merchant_id', 'coupon_id', 'discount_rate', 'date_received', 'date', 'label'],
                             axis=1)

    params = {'boosting_type': 'gbdt',
              'objective': 'binary',
              'metric': 'auc',
              'learning_rate': 0.01,
              'min_child_weight': 10,
              'feature_fraction': 0.8,
              'min_split_gain': 0.1,
              'silent': True
              }

    feat_names = pd.Series(train_x.columns.values.tolist())

    model = xgb.XGBClassifier(learning_rate=0.01, n_estimators=800)

    rfe = RFE(model, n_features_to_select=180)
    rfe.fit(train_x, train_y)
    print("Features sorted by their rank:")
    feat_selected=sorted(zip(map(lambda x: x, rfe.ranking_), feat_names))
    feat_selet_names=[]
    for i in feat_selected:
        feat_selet_names.append(i[1])
    final_feat=pd.DataFrame({'selected feat':feat_selet_names})
    final_feat.to_csv(r'..\feat_select.csv',index=False)