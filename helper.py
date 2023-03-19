import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score, average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, KFold, TimeSeriesSplit, train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PowerTransformer
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from mlxtend.plotting import plot_confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import BaggingClassifier
from imblearn.over_sampling import RandomOverSampler,SMOTE,SMOTENC
from imblearn.under_sampling import RandomUnderSampler

from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import make_scorer
import optuna
from collections import Counter
import time
import warnings
import gc


import datetime

pd.set_option('display.max_columns', None)
warnings.filterwarnings('ignore') 


def performance_result(y_true, y_pred):
    '''an automated confusion matrix plotter with a selection of classifier metrics'''
    confusion_matrix_plot(y_true, y_pred)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    print('FP rate=FP/(FP+TN): ',"{:.4f}".format(fp/((fp+tn))))
    print('Precision=TP/(TP+FP) : ', "{:.4f}".format(precision_score(y_true, y_pred)))
    print('Recall=TP/(TP+FN) : ', "{:.4f}".format(recall_score(y_true, y_pred)))
    print('AUC-PR: ', "{:.4f}".format(average_precision_score(y_true, y_pred)))
    print('f1-score: ', "{:.4f}".format(f1_score(y_true, y_pred)))
    print('roc_auc: ', "{:.4f}".format(roc_auc_score(y_true, y_pred)))
    print('Accuracy: ', "{:.4f}".format(accuracy_score(y_true, y_pred))) 
    
def confusion_matrix_plot(y_true, y_pred):
    plt.rcParams['font.size'] = '12'
    fig, ax = plot_confusion_matrix(conf_mat=confusion_matrix(y_true, y_pred),
                                    show_absolute=True,
                                    show_normed=True,
                                    figsize=(4, 4))
    fig.suptitle('Confusion Matrix', fontsize=16)
    plt.show() 


def feature_importances(wrapped):
    '''The input is a wrapped and trained classifier with a .feature_importances_ method. Returns a sorted DataFrame of feature importances'''
    
    return(pd.DataFrame([wrapped.pipe.named_steps['classifier'].feature_importances_, wrapped.pipe.named_steps['col_transform'].get_feature_names_out()],
             index=['importance','feature']).T.sort_values(by='importance',
                                                           ascending=False).reset_index(drop=True))
    
    
    
class wrapper():
    
    def __init__(self,classifier):
        '''A helper class for managing transformation pipelines, predictors, as well as storing information on categorical and numerical columns'''
        self.num=['mager', 'riorlive', 'riordead', 'riorterm', 'revis', 'cig_0', 'cig_1', 'cig_2', 'cig_3', 'mhtr', 'bmi', 'wgt_r', 'wtgain', 'apgar5', 'dplural', 'fagecomb', 'combgest', 'brthwgt']
        self.cat=['dob_yy', 'dob_mm', 'mracehisp', 'dob_wk', 'bfacil3', 'mbstate_rec', 'mrace6', 'dmar', 'meduc', 'frace6', 'feduc', 'recare5', 'dmeth_rec', 'ay_rec', 'sex', 'rf_pdiab', 'rf_gdiab', 'rf_phype', 'rf_ghype', 'rf_ehype', 'rf_ppb', 'ab_anti', 'ab_aven1', 'ab_aven6', 'ab_nicu', 'ab_seiz', 'ab_surf', 'ca_anen', 'ca_cchd', 'ca_cdh', 'ca_cleft', 'ca_clpal', 'ca_disor', 'ca_down', 'ca_gast', 'ca_hypo', 'ca_limb', 'ca_mnsb', 'ca_omph', 'mtran', 'ld_anes', 'ld_antb', 'ld_augm', 'ld_chor', 'ld_indl', 'ld_ster', 'ip_chlam', 'ip_gon', 'ip_hepb', 'ip_hepc', 'ip_syph']
        self.target=['survival']
        self.num_scaler=StandardScaler()
        self.cat_scaler=OneHotEncoder()
        self.col_transform = ColumnTransformer([('num',self.num_scaler,self.num),
                               ('cat',self.cat_scaler, self.cat)])
        self.classifier=classifier
        self.pipe = Pipeline(steps=[('col_transform', self.col_transform),
                      ('classifier', self.classifier)])
    def fit(self,X,Y):
        self.pipe.fit(X,Y)
        return(self)
    
    def predict(self,xtesta):
        return(self.pipe.predict(xtesta))
