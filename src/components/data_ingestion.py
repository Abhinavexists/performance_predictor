import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from dataclasses import dataclass, field

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
            train_set.to_csv(self.ingestion_config.train_data_path, index=True, header=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=True, header=False)

            logging.info("Ingestion of data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            tb = sys.exc_info()[2]
            if tb is not None:
                CustomException(error_message=e, error_detail=tb)
            else:
                pass

if __name__ == "__main__":
    di = DataIngestion()
    di.initiate_data_ingestion()