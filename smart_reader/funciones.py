import enum
from sahi.model import Yolov5DetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from IPython.display import Image
#### ****    IMPORTAR EL MODELO CON LOS PESOS **** ####

#!git clone https://github.com/ultralytics/yolov5  # clone repo
#%cd yolov5
#%pip install -qr requirements.txt # install dependencies
#%pip install -q roboflow

#print(f"Setup complete. Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

trained_model_path = 'data/yolov5l6.pt'

### CORRO EL MODELO CON LOS PESOS INSTANCIADOS PREVIAMENTE

def initialize_yolov5_model(trained_model_path, confidence_threshold:(float)=0.6, device="cuda:"):
    detection_model = Yolov5DetectionModel(
                        model_path=trained_model_path,
                        confidence_threshold = confidence_threshold,
                        device= device) # or 'cuda:0'

    return detection_model


# Realizo la prediccion y la almaceno en una variable

yolov5_model = initialize_yolov5_model(trained_model_path)

def predict_yolov5_model(yolov5_model):
    result = get_prediction("directorio_donde_guarda_la_imagen", yolov5_model)

    return result


# Visualizo las Predicciones con el modelo Yolov5l6

def visualize_yolov5_model(result):

    visualize_yolov5 = result.export_visuals(export_dir="directorio_donde_guardo_la_imagen")

    return visualize_yolov5

# Paso el modelo de yolov5 por sahi

def predict_sahi_model(yolov5_model):
    result = get_sliced_prediction(
            "nombre_del_directorio_donde_se_encuentra_la_imagen",
            yolov5_model,
            slice_height = 1080,
            slice_width = 1080,
            overlap_height_ratio = 0.1,
            overlap_width_ratio = 0.1
)
    return result


# Visualizo la prediccion del modelo realizado con sahi

def visualize_sahi_model(result):
    visualize_sahi = result.export_visuals(export_dir="directorio_donde_guarde_el_modelo_realizado")

    return visualize_sahi

# Accedo a las predicciones a traves de una lista

def prediction_list(result):
    object_prediction_list = result.object_prediction_list
