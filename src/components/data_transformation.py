from pathlib import Path
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
 
from src.utils import save_object
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: Path = field(default_factory=lambda: Path.cwd() / 'artifacts' / 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer(self):
        try:
            numerical_columns = [
                    'writing_score',
                    'reading_score',
                ]
            
            categorical_columns = [
                    'gender',
                    'race_ethnicity',
                    'lunch',
                    'test_preparation_course',
                ]

            num_pipeline = Pipeline(
                steps=[
                    ('Imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            # The issue i faced was with StandardScaler in the categorical pipeline. 
            # Since OneHotEncoder outputs a sparse matrix, the scaler couldn’t center it by default.
            # leading to failure of data_transformation pieline 
            # fixed it by setting with_mean=False, which makes it compatible with sparse matrices.
            
            cat_pipeline = Pipeline(
               steps=[
                   ('Imputer', SimpleImputer(strategy='most_frequent')),
                   ('one_hot_encoder', OneHotEncoder()),
                   ('Scaler', StandardScaler(with_mean=False))
               ] 
            )

            logging.info('Numerical column Standard scaling completed')
            logging.info('Categorical column encoding completed')

            preprocessor = ColumnTransformer(
                [
                   ('num_pipeline', num_pipeline, numerical_columns),
                   ('cat_pipeline', cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e) from e

    def init_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read Train and Test Data Completed')
            logging.info('Obtaining preprocessing object')

            preprocessor_obj = self.get_data_transformer()

            target_column = 'math_score'

            input_feature_train_df = train_df.drop(columns=target_column, axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=target_column, axis=1)
            target_feature_test_df = test_df[target_column]

            input_feature_train = preprocessor_obj.fit_transform(input_feature_train_df)

            logging.info("Completed fit_transform on training data")

            input_feature_test = preprocessor_obj.transform(input_feature_test_df)

            logging.info("Completed transform on test data")

            train_array = np.c_[
                input_feature_train, np.array(target_feature_train_df)
            ]

            test_array = np.c_[
                input_feature_test, np.array(target_feature_test_df)
            ]

            logging.info('Saving preprocessing Object')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            return [
                train_array,
                test_array,
                self.data_transformation_config.preprocessor_obj_file_path,
            ]
        
        except Exception as e:
            raise CustomException(e) from e