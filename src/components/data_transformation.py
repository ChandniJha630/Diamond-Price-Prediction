import os
import sys
from src.logger import logging
from src.exception import CustomException
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from src.utils import save_object
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    def get_data_transformation_object(self):
        try:
            logging.info('Data transformation initiated')
            
            #Categorical and Numerical columns
            num_cols=['carat', 'depth', 'table', 'x', 'y', 'z']
            cat_cols=['cut', 'color', 'clarity']
        
            #Define Custom Rankings
            cut_categories=['Fair','Good','Very Good','Premium','Ideal']
            color_categories=['D','E','F','G','H','I','J']
            clarity_categories=['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info('Data Transformation Pipeline Initiated')
            num_pipeline=Pipeline(
            steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('OrdinalEncoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                    ('scaler',StandardScaler())
                ]
            )
            reprocessor=ColumnTransformer([
                ('num_pipeline',num_pipeline,num_cols),
                ('cat_pipeline',cat_pipeline,cat_cols)
            ])
            logging.info('Data Transformation Completed')
            return reprocessor
        
        except Exception as e:
            logging.info('Exception Occured In Data Transformation')
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_data_path,test_data_path):
        try:
            train_df=pd.read_csv(train_data_path)
            test_df=pd.read_csv(test_data_path)
            logging.info("Reading train and Test Data Completed")
            logging.info('obtaining preprocessing object')
            preprocessing_obj=self.get_data_transformation_object()
            target_cols='price'
            drop_cols=[target_cols,'id']
            input_features_train_df=train_df.drop(columns=drop_cols,axis=1)
            output_feature_train_df=train_df[target_cols]
            input_features_test_df=train_df.drop(columns=drop_cols,axis=1)
            output_feature_test_df=train_df[target_cols]
            
            #Data Transformation
            input_feature_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_features_test_df)
            
            logging.info('Completed applying preprocessing on training and testing data')
            
            train_arr=np.c_[input_feature_train_arr,np.array(output_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(output_feature_test_df)]
            
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
           
            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
        except Exception as e:
            raise CustomException(e,sys)   