import os
import cProfile
from . import model

model_dir= os.path.dirname(model.__file__)
os.makedirs(f"{model_dir}/cache_dir", exist_ok= True)

translate_engine= model.Translate_Model(cache_dir= f"{model_dir}/cache_dir")