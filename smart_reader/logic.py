from sahi.model import Yolov5DetectionModel
from sahi.predict import get_prediction, get_sliced_prediction
import os
from google.cloud import storage


class PredictionModel:
    trained_model_path = "model/yolov5l6.pt"
    downloads_path = "smart_reader/converted"
    predictions_path = "smart_reader/predictions"

    def __init__(
        self, confidence_threshold: float = 0.6, computing_device: str = "cpu"
    ):
        self.prediction_model = Yolov5DetectionModel(
            model_path=self.trained_model_path,
            confidence_threshold=confidence_threshold,
            device=computing_device,
        )

    def predict(self, filename: str) -> list:
        filename_no_extension = filename.split(".")[0]

        prediction = get_prediction(
            f"{self.downloads_path}/{filename}", self.prediction_model
        )
        prediction.export_visuals(
            export_dir=self.predictions_path, file_name=f"{filename_no_extension}"
        )

        return prediction.to_coco_annotations()

    def predict_with_sahi(
        self, filename, slice_size: int = 1080, overlap_ratio: float = 0.1
    ) -> list:
        filename_no_extension = filename.split(".")[0]

        prediction_with_sahi = get_sliced_prediction(
            f"{self.downloads_path}/{filename}",
            self.prediction_model,
            slice_height=slice_size,
            slice_width=slice_size,
            overlap_height_ratio=overlap_ratio,
            overlap_width_ratio=overlap_ratio,
        )
        prediction_with_sahi.export_visuals(
            export_dir=self.predictions_path, file_name=f"{filename_no_extension}"
        )

        return prediction_with_sahi.to_coco_annotations()


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "application-credentials.json"


def upload_images(
    bucket_name,
    original_filename,
    original_file_path,
    predicted_filename,
    predicted_file_path,
):

    try:
        project_id = os.environ.get("GCP_PROJECT")

        storage_client = storage.Client(project_id)
        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(original_filename)
        blob.upload_from_filename(original_file_path)

        blob = bucket.blob(predicted_filename)
        blob.upload_from_filename(predicted_file_path)

    except Exception as err:
        print(err)
        return False

    return True
