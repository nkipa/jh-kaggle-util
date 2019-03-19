import config
import jhkaggle
import jhkaggle.train_xgboost
import jhkaggle.train_keras
import jhkaggle.train_sklearn
import jhkaggle.train_lightgbm
from jhkaggle.joiner import perform_join
from jhkaggle.ensemble_glm import ensemble
import time
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neighbors import KNeighborsClassifier

# Modify the code in this function to build your own XGBoost trainers
# It will br executed only when you run this file directly, and not when
# you import this file from another Python script.s
def run_xgboost():
    COMMON = {
        'objective': 'binary:logistic',
        'eval_metric': 'auc',
        'silent': 1,
        'n_jobs': -1
    }

    params = {'learning_rate': 0.02, 'seed': 4242, 'max_depth': 2,  'colsample_bytree': 0.3}


    params = {**params, **COMMON}
    print(params)

    start_time = time.time()
    train = jhkaggle.train_xgboost.TrainXGBoost("1",params=params,run_single_fold=False)
    train.early_stop = 50
    train.rounds = 10000
    #train.run_cv()
    train.run()

    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(jhkaggle.util.hms_string(elapsed_time)))

def run_keras():
  # "all the time" to "always"
  # reall short ones that are dead wrong
  # [100]	train-logloss:0.288795	eval-logloss:0.329036
  # [598]	train-logloss:0.152968	eval-logloss:0.296854
  # [984]	train-logloss:0.096444	eval-logloss:0.293915

  start_time = time.time()
  train = jhkaggle.train_keras.TrainTensorFlow("1",False)
  train.zscore = False
  train.run()

  elapsed_time = time.time() - start_time
  print("Elapsed time: {}".format(jhkaggle.util.hms_string(elapsed_time)))

def run_sklearn():
  n_trees = 100
  n_folds = 3

  # https://www.analyticsvidhya.com/blog/2015/06/tuning-random-forest-model/
  alg_list = [
      ['rforest',RandomForestClassifier(n_estimators=5000, n_jobs=-1, verbose=1, max_depth=3)],
      ['extree',ExtraTreesClassifier(n_estimators = 5000,max_depth=3,n_jobs=-1)],
 #     ['adaboost',AdaBoostClassifier(base_estimator=None, n_estimators=600, learning_rate=1.0, random_state=20160703)],
 #     ['knn', sklearn.neighbors.KNeighborsClassifier(n_neighbors=5,n_jobs=-1)]
  ]

  start_time = time.time()
  for name,alg in alg_list:
      train = jhkaggle.train_sklearn.TrainSKLearn("1",name,alg,False)
      train.run()
      train = None
  elapsed_time = time.time() - start_time
  print("Elapsed time: {}".format(jhkaggle.util.hms_string(elapsed_time)))

def run_lgb():
  params = {
    'bagging_freq': 5,          
    'bagging_fraction': 0.38,   'boost_from_average':'false',   
    'boost': 'gbdt',             'feature_fraction': 0.04,     'learning_rate': 0.0085,
    'max_depth': -1,             'metric':'auc',                'min_data_in_leaf': 80,     'min_sum_hessian_in_leaf': 10.0,
    'num_leaves': 13,            'num_threads': 8,              'tree_learner': 'serial',   'objective': 'binary',
    'reg_alpha': 0.1302650970728192, 'reg_lambda': 0.3603427518866501,'verbosity': 1
  }

  start_time = time.time()
  train = jhkaggle.train_lightgbm.TrainLightGBM("1",params=params,run_single_fold=False)
  train.early_stop = 50
  #train.run_cv()
  train.run()

  elapsed_time = time.time() - start_time
  print("Elapsed time: {}".format(jhkaggle.util.hms_string(elapsed_time)))


if __name__ == "__main__":
    #run_xgboost()
    run_sklearn()
    #run_lgb()