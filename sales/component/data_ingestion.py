from sales.entity.config_entity import DataIngestionConfig
import sys,os
from sales.exception import SalesException
from sales.logger import logging
from sales.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import shutil

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise SalesException(e,sys)
    
    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            



            

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            "Train")

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        "Test")
            dataset_original_path= os.getcwd()

            train_file_original_path= os.path.join(dataset_original_path, "Dataset", "Train.csv")
            test_file_original_path= os.path.join(dataset_original_path, "Dataset", "Test.csv")                            
            
            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            shutil.copy(train_file_original_path, train_file_path)

            logging.info(f"Exporting training datset to file: [{train_file_path}]")
        
            os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
            shutil.copy(test_file_original_path, test_file_path)
            logging.info(f"Exporting test dataset to file: [{test_file_path}]")
            
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise SalesException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            
            return self.split_data_as_train_test()
        except Exception as e:
            raise SalesException(e,sys) from e
    


    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")