from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
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
        with open(f"smart_reader/downloads/{file.filename}", "wb") as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"filename": file.filename, "message": "File successfully uploaded"}


@app.get("/predict")
async def predict_endpoint(filename: str, slicing: bool = True) -> dict:
    if slicing is not True:
        prediction = model.predict(filename)
    else:
        prediction = model.predict_with_sahi(filename)

    return {"data": prediction, "message": "File succesfully processed"}

@app.get("/processed_image")
async def main(filename: str, filename_ending: str):
    filename_no_extension = filename.split(".")[0]
    return FileResponse(f'smart_reader/predictions/{filename_no_extension}_{filename_ending}.png')
