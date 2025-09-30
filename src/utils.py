import dill
from pathlib import Path
from sklearn.metrics import r2_score

from src.exception import CustomException, tb

def save_object(file_path: Path, obj):
    try:
        dir_path = file_path.parent
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'wb') as file:
            dill.dump(obj, file)

    except Exception as e:
            raise CustomException(error_message=e, error_detail=tb)

def evaluate_model(x_train, y_train, x_test, y_test, models):
    try:
        report: dict = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(x_train, y_train)

            # y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            # train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
            raise CustomException(error_message=e, error_detail=tb)