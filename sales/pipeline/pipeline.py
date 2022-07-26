from sales.config.configuration import Configuration
from sales.logger import logging
from sales.exception import SalesException

from sales.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from sales.entity.config_entity import DataIngestionConfig
from sales.component.data_ingestion import DataIngestion
import os,sys
from sales.component.data_validation import DataValidation

class Pipeline:

    def __init__(self,config: Configuration = Configuration()) -> None:
        try:
            self.config=config

        except Exception as e:
            raise SalesException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise SalesException(e,sys) from e    


    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation= DataValidation(data_validation_config= self.config.get_data_validation_config(), data_ingestion_artifact= data_ingestion_artifact)
            return data_validation.initiate_data_validation()

        except Exception as e:
            raise SalesException(e,sys) from e    

    def start_data_transformation(self):
        pass

    def start_model_trainer(self):
        pass

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass

    def run_pipeline(self):
        try:
            #data ingestion

            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact= self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)




        except Exception as e:
            raise SalesException(e,sys) from e 