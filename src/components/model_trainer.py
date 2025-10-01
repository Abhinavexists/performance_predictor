import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model, load_params

@dataclass
class ModelTrainerConfig:
    model_trainer_file_path: Path = field(default_factory=lambda: Path.cwd() / 'artifacts' / 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def init_model_trainer(self, train_array, test_array, preprocessor_obj_file_path):
        try:
            logging.info('Splitting train and test data')
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models: dict = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBoost Regressor": XGBRegressor(),
                "CatBoost Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

            # params = load_params(path=Path('/home/abhinav/Projects/Project-1-ML/src/config/params.yml'))
            params = {}

            try:
                print(f"Params file exists: {Path('/home/abhinav/Projects/Project-1-ML/src/config/params.yml').exists()}")
                params = load_params(Path('/home/abhinav/Projects/Project-1-ML/src/config/params.yml'))
                print(f"Loaded params: {params}")
            except Exception as e:
                print(f"Error loading params: {e}")

            model_report: Optional[dict] = evaluate_model(x_train=x_train, y_train=y_train, 
                                                x_test=x_test, y_test=y_test, models=models, params=params)
            
            best_model_score = max(model_report.values())

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            best_model.fit(x_train, y_train)

            if best_model_score < 0.6:
                raise CustomException(Exception("No Best Model Found"))
            
            save_object(
                file_path = self.model_trainer_config.model_trainer_file_path,
                obj = best_model
            )

            y_pred = best_model.predict(x_test)
            R2_score = r2_score(y_test, y_pred)

            logging.info(f"Best model found: {best_model_name}")
            logging.info(f"Best model score: {best_model_score}")
            logging.info(f"Final R2 score on test data: {R2_score}")

            return R2_score, preprocessor_obj_file_path

        except Exception as e:
            raise CustomException(error_message=e)