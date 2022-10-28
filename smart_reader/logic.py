from sahi.model import Yolov5DetectionModel
from sahi.predict import get_prediction, get_sliced_prediction


class PredictionModel:
    trained_weights_path = "data/yolov5l6.pt"
    image_store_path = "smart_reader/downloads"

    def __init__(
        self, confidence_threshold: float = 0.6, computing_device: str = "cpu"
    ):
        self.prediction_model = Yolov5DetectionModel(
            model_path=self.trained_weights_path,
            confidence_threshold=confidence_threshold,
            device=computing_device,
        )

    def predict(self, filename):
        filename_no_extension = filename.split(".")[0]

        prediction = get_prediction(
            f"{self.image_store_path}/{filename}", self.prediction_model
        )
        prediction.export_visuals(export_dir=f"{filename_no_extension}_yolo.png")

        return prediction

    def predict_with_sahi(
        self, filename, slice_size: int = 1080, overlap_ratio: float = 0.1
    ):
        filename_no_extension = filename.split(".")[0]

        prediction_with_sahi = get_sliced_prediction(
            f"{self.image_store_path}/{filename}",
            self.prediction_model,
            slice_height=slice_size,
            slice_width=slice_size,
            overlap_height_ratio=overlap_ratio,
            overlap_width_ratio=overlap_ratio,
        )
        prediction_with_sahi.export_visuals(
            export_dir=f"{filename_no_extension}_sahi.png"
        )

        return prediction_with_sahi
