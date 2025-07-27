# !pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="aNGDdPqxW9e2rpMc9DWw")
project = rf.workspace("gaels-projects").project("surgitrack-rayo2")
version = project.version(1)
dataset = version.download("yolov11")
