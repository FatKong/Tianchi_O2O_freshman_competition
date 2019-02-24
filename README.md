# Tianchi_O2O_freshman_competition
天池O2O新手赛    AUC=0.7961 排名前段时间有30+，现在估计40+，随着后面越来越多人提交且结果会越来越好，如果不做了排名会掉的

     Data_preprocess.py 数据预处理部分，包括数据集打标和数据集划分;
     feat_section.py    特征区间的特征工程代码
     label_section.py   预测区间的特征工程代码
     time_gap_count.py  预测区间的某些时间差特征和leak特征
     model.py           xgb,lgb模型训练和使用RFE做特征选择

## 一.数据集划分
   使用时间窗口划分法划分数据
   ||特征区间|预测区间|
   |:---|:---|:---|
   |测试集|20160501~20160630|20160701~20160731|
