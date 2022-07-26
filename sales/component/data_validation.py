from sales.logger import logging
from sales.exception import SalesException
from sales.entity.config_entity import DataTransformationConfig, DataValidationConfig
from sales.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
import os,sys
import pandas  as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig,data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact

        except Exception as e:
            raise SalesException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise SalesException(e,sys) from e        

    def does_train_test_file_exists(self) -> bool:
        try:
            logging.info("Checking if train and test files are available.")
            does_train_file_exists= False
            does_test_file_exists= False

            train_file_path= self.data_ingestion_artifact.train_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path

            does_train_file_exists= os.path.exists(train_file_path)
            does_test_file_exists= os.path.exists(test_file_path)
            
            is_available=  does_test_file_exists and does_train_file_exists
            logging.info (f" Do train and test files exist? -> {is_available}")
            return is_available

        except Exception as e:
            raise SalesException(e,sys) from e  

    def validate_dataset_schema(self) -> bool:
        try:
            validation_status= False



            return validation_status

        except Exception as e:
            raise SalesException(e,sys) from e

    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report
        except Exception as e:
            raise SalesException(e,sys) from e


    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)
        except Exception as e:
            raise SalesException(e,sys) from e

    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise SalesException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            self.does_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successully."
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SalesException(e,sys) from e


    def __del__(self):
        logging.info(f"{'>>'*30}Data Valdaition log completed.{'<<'*30} \n\n")