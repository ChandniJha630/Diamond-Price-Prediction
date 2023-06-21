import os
import sys
from src.logger import logging
from src.exception import CustomException

import pandas as pd
from sklearn.model_selection import train_test_split

##Initialise data ingestion configuration
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv')
    raw_data_path:str=os.path.join('artifacts','raw.csv')
    
#create data ingestion class
class DataIngestion:
    def __init__(self):
        self.Ingestion_config=DataIngestionConfig()
        
    def initialize_data_ingestion(self):
        logging.info('Data ingestion methods starts')
        
        try:
            df=pd.read_csv(os.path.join('Notebook/data','gemstone.csv'))
            logging.info('Dataset read as pandas Dataframe')
        
            os.makedirs(os.path.dirname(self.Ingestion_config.raw_data_path),exist_ok=True)
            df.to_csv(self.Ingestion_config.raw_data_path,index=False)
            logging.info('Raw data created')
        
            train_set, test_set =train_test_split(df, test_size=0.30, random_state=42)
            train_set.to_csv(self.Ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.Ingestion_config.test_data_path,index=False,header=True)
            logging.info("Ingestion of data is completed")
        
            return(
                self.Ingestion_config.train_data_path,
                self.Ingestion_config.test_data_path
            )
        
        except Exception as e:
            logging.info("Exception occured at Data ingestion stage") 
            raise CustomException(e,sys)
