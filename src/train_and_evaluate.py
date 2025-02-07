import os
import yaml
import pandas as pd
import numpy as np
import argparse
from pkgutil import get_data
from getData import get_data,read_param
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
import joblib
import json
import mlflow
from urllib.parse import urlparse

def train_and_evaluate(config_path):
    config = read_param(config_path)
    train_data_path = config["split_data"]["train_path"]
    test_data_path = config["split_data"]["test_path"]
    raw_data_path = config["load_data"]["clean_data"]
    split_data = config["split_data"]["test_size"]
    random_state = config["base"]["random_state"]
    df=pd.read_csv(raw_data_path,sep=',')
    model_dir = config["model_path"]

    alpha = config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = config["estimators"]["ElasticNet"]["params"]["l1_ratio"]

    target = config["base"]["target_col"]
    train = pd.read_csv("train_data_path")
    test = pd.read_csv("test_data_path")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target,axis=1)
    test_x = test.drop(target,axis=1)

    #Model Creation - 
    lr = ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=random_state)
    lr.fit(train_x,train_y)

    predict = lr.predict(test_x)

    (rmse, mse, r2) = eval_metrics(test_y,predict)
    print("ElasticNet Model (alpha=%f,l1_score=%f)" % (alpha,l1_ratio))