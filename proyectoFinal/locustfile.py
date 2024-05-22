from locust import HttpUser, task, between,constant
from pydantic import BaseModel
import json
class CoverType(BaseModel):
    # Aquí debes definir las características de entrada que espera el modelo.
    Elevation: int = 2596
    Aspect: int = 51
    Slope: int = 3
    Horizontal_Distance_To_Hydrology: int =  258
    Vertical_Distance_To_Hydrology: int  = 0
    Horizontal_Distance_To_Roadways: int = 510
    Hillshade_9am: int = 211
    Hillshade_Noon: int = 232
    Hillshade_3pm: int = 148
    Horizontal_Distance_To_Fire_Points: int =  6279
    Wilderness_Area: str =" Rawah"
    Soil_Type: str =" C7745"

class MLModelLoadTester(HttpUser):
    wait_time = constant(1)  # Tiempo entre tareas ejecutadas por cada usuario simulado.
    host = "http://10.43.101.156:8085"

    @task
    def predict(self):
        # Datos de entrada para el modelo
        payload = {
            "Elevation": 2596,
            "Aspect": 51,
            "Slope": 3,
            "Horizontal_Distance_To_Hydrology": 258,
            "Vertical_Distance_To_Hydrology": 0,
            "Horizontal_Distance_To_Roadways": 510,
            "Hillshade_9am": 211,
            "Hillshade_Noon": 232,
            "Hillshade_3pm": 148,
            "Horizontal_Distance_To_Fire_Points": 6279,
            "Wilderness_Area": "Rawah",
            "Soil_Type": "C7745"  
                  }
        headers = {'Content-Type': 'application/json'}
        
        # Enviar solicitud POST al endpoint /predict
        self.client.post("/predict", data=json.dumps(payload), headers=headers)

