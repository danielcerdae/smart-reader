import os
import time
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from smart_reader.logic import PredictionModel, upload_images
from pdf2image import convert_from_path
from starlette.background import BackgroundTasks
from uuid import uuid1
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.model = PredictionModel()


@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)) -> dict:
    try:
        contents = file.file.read()
        with open(f"smart_reader/downloads/{file.filename}", "wb") as f:
            f.write(contents)
    except Exception:
        return {"success": False, "message": "There was an error uploading the file"}
    finally:
        file.file.close()

        Image.MAX_IMAGE_PIXELS = 100000000
        images = convert_from_path(
            f"smart_reader/downloads/{file.filename}",
            dpi=300,
            grayscale=True,
            size=(2160, None),
        )
        filename_no_extension = file.filename.split(".")[0]
        filename = filename_no_extension + ".png"
        images[0].save(f"smart_reader/converted/{filename}")

    return {"success": True, "message": "File successfully uploaded", "filename": filename}


@app.get("/predict")
async def predict_endpoint(filename: str, slicing: bool, confidence_threshold: float) -> dict:

    if confidence_threshold != float(0.6):
        app.state.model = PredictionModel(confidence_threshold=confidence_threshold)

    if slicing is True:
        prediction = app.state.model.predict_with_sahi(filename)
    else:
        prediction = app.state.model.predict(filename)

    if prediction:
        filename_no_extension = filename.split(".")[0]

        custom_id = uuid1()

        original_filename = f"{custom_id}-original.png"
        original_file_path = f"smart_reader/converted/{filename_no_extension}.png"

        predicted_filename = f"{custom_id}-predicted.png"
        predicted_file_path = f"smart_reader/predictions/{filename_no_extension}.png"

        bucket_name = os.environ.get("GOOGLE_CLOUD_BUCKET")

        was_succesful = upload_images(
            bucket_name,
            original_filename,
            original_file_path,
            predicted_filename,
            predicted_file_path,
        )

        if was_succesful:
            os.remove(f"smart_reader/downloads/{filename_no_extension}.pdf")
            os.remove(f"smart_reader/converted/{filename_no_extension}.png")
            os.remove(f"smart_reader/predictions/{filename_no_extension}.png")

            original_image_url = (
                f"https://storage.googleapis.com/{bucket_name}/{original_filename}"
            )
            predicted_image_url = (
                f"https://storage.googleapis.com/{bucket_name}/{predicted_filename}"
            )

            return {
                "success": True,
                "message": "File succesfully processed",
                "image_id": custom_id,
                "original_image_url": original_image_url,
                "predicted_image_url": predicted_image_url,
                "data": prediction,
            }

    return {"success": False, "message": "There was an error"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# File sent via http request
# @app.get("/processed_image")
# async def main(filename: str,
#                background_tasks: BackgroundTasks) -> FileResponse:
#     filename_no_extension = filename.split(".")[0]
#     file_path = f"smart_reader/predictions/{filename_no_extension}.png"

#     file = FileResponse(file_path)

#     # background_tasks.add_task(remove_file, file_name)
#     return file
