import os
import sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
import pandas as pd

if __name__=='__main__':
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initialize_data_ingestion()
    print(train_data_path,test_data_path)
    