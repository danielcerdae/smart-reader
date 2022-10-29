from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile

from smart_reader.logic import PredictionModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = PredictionModel()


@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)) -> dict:
    try:
        contents = file.file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}, 404
    finally:
        file.file.close()

    return {"filename": file.filename, "message": "File successfully uploaded"}, 201


@app.get("/predict")
async def predict_endpoint(filename: str) -> dict:
    prediction = model.predict(filename)
    print(prediction)
    return {""}
