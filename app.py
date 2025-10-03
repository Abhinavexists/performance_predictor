import pandas as pd
import numpy as np
import uvicorn
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import PredictPipeline, CustomData

app = FastAPI()


templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

@app.get('/predict', response_class=HTMLResponse, name='predict')
async def get_predict(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/predict', response_class=HTMLResponse)
async def post_predict(request: Request,
                       gender: str = Form(...),
                       race_ethnicity: str = Form(...), 
                       parent_level_of_education: str = Form(...), 
                       lunch: str = Form(...), 
                       test_preparation_course:str = Form(...), 
                       reading_score: int = Form(...), 
                       writing_score: int = Form(...)):
    data = CustomData(gender=gender,
                      race_ethnicity=race_ethnicity,
                      parent_level_of_education=parent_level_of_education,
                      lunch=lunch,
                      test_preparation_course=test_preparation_course,
                      reading_score=reading_score,
                      writing_score=writing_score)
    
    pred_df = data.get_data_as_df()
    print(pred_df)

    predict_pipeline = PredictPipeline()
    results = predict_pipeline.predict(pred_df)
    return templates.TemplateResponse('index.html', {'request': request, 'results': results})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)