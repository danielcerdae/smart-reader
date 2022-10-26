import enum
from sahi.model import Yolov5DetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from IPython.display import Image
#### IMPORTAR EL MODELO CON LOS PESOS ####

trained_model_path = 'models/yolov5l6.pt'

### CORRO EL MODELO CON LOS PESOS INSTANCIADOS PREVIAMENTE

def modelo_yolov5(trained_model_path, confidence_threshold:(float)=0.6, device="cuda:"):
    detection_model = Yolov5DetectionModel(
                        model_path=trained_model_path,
                        confidence_threshold = confidence_threshold,
                        device= device) # or 'cuda:0'

    return detection_model


# Realizo la prediccion y la almaceno en una variable
def prediction():
    result = get_prediction("directorio_donde_guarda_la_imagen", detection_model)
