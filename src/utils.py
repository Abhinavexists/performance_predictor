import dill
from pathlib import Path

from src.exception import CustomException, tb

def save_object(file_path: Path, obj):
    try:
        dir_path = file_path.parent
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'wb') as file:
            dill.dump(obj, file)

    except Exception as e:
        if tb is not None:
            raise CustomException(error_message=e, error_detail=tb)
        else:
            pass