import numpy as np
import pandas as pd
from src.exception import CustomException
from src.logger import logging

from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

from src.utils import save_object,evaluate_models
from dataclasses import dataclass

import sys,os

@dataclass
class ModelTrainerconfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')
class Model_Trainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerconfig()
    def initiate_model_training(self,train_array,test_array):
        try:
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )
            
            models = {
                'LinearRegression': LinearRegression(),
                'Lasso': Lasso(),
                'Ridge': Ridge(),
                'ElasticNet': ElasticNet(),
                'DecisionTree':DecisionTreeRegressor(),
                'RandomForest':RandomForestRegressor(),
                'KNeighborsRegressor': KNeighborsRegressor()
            }
            model_report:dict=evaluate_models(X_train,y_train,X_test,y_test,models)
            logging.info(f'Model Report: (model_report)')
            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]
            logging.info(f'Best Model is {best_model}')
            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
        except Exception as e:
            raise CustomException(e,sys)