from src.exception import CustomException
from src.logger import logging
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from dataclasses import dataclass, field

from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

@dataclass
class DataIngestionConfig:
    train_data_path: Path = field(default_factory=lambda: Path.cwd() / 'artifacts' / 'train.csv')
    test_data_path: Path = field(default_factory=lambda: Path.cwd() / 'artifacts' / 'test.csv')
    raw_data_path: Path = field(default_factory=lambda: Path.cwd() / 'artifacts' / 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data Ingestion method or component")

        try:
            df = pd.read_csv("notebooks/data/Student.csv")
            
            logging.info("Read the dataset as dataframe")

            self.ingestion_config.train_data_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train-Test Split Initiated")
            
            train_set, test_set = train_test_split(df, train_size=0.8, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
                raise CustomException(e) from e

if __name__ == "__main__":
    di = DataIngestion()
    train_data, test_data = di.initiate_data_ingestion()

    dt = DataTransformation()
    train_array, test_array, preprocessor_obj_file_path = dt.init_data_transformation(train_data, test_data)

    mt = ModelTrainer()
    mt.init_model_trainer(train_array, test_array, preprocessor_obj_file_path)
