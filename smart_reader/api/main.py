from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
import os
from fastapi.responses import FileResponse
from smart_reader.logic import PredictionModel
from pdf2image import convert_from_path
from PIL import Image


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

        Image.MAX_IMAGE_PIXELS = 100000000
        images = convert_from_path(f'smart_reader/downloads/{file.filename}', dpi=300, grayscale=True, size=(2160,None))
        filename_no_extension = file.filename.split('.')[0]
        filename = filename_no_extension + '.png'
        images[0].save(f'smart_reader/converted/{filename}')

    return {"filename": filename, "message": "File successfully uploaded"}



@app.get("/predict")
async def predict_endpoint(filename: str) -> dict:
    prediction = model.predict_with_sahi(filename)

    return {"data": prediction, "message": "File succesfully processed"}


@app.get("/processed_image")
async def main(filename: str) -> FileResponse:
    filename_no_extension = filename.split(".")[0]
    file_path = f"smart_reader/predictions/{filename_no_extension}.png"

    file = FileResponse(file_path)

    #if file:
    #    os.remove(file_path)

    return file
