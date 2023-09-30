from dotenv import load_dotenv
import os
from fastapi import FastAPI
import pandas as pd
from sqlalchemy import create_engine
from typing import Union
from datetime import datetime, date
import re
from flask import Flask
import time

app = Flask(__name__)


app = FastAPI()

load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_URL = os.getenv("DB_URL")

@app.get("/")
def read_root():
    return {"Hello": "MiTAnto"}

cadena_conexion = f"mysql://{DB_USER}:{DB_PASS}@{DB_URL}/mitanto"

conexion = create_engine(cadena_conexion)

@app.get("/codigo/&{codigo}")
def read_item(codigo: str):  
    while True:
        #try:
            sql = "SELECT Nombre, Creado, Usuario_creador,Actualizado, Actualizar_usuario FROM clients_export__2_ WHERE Código = '%s'" % codigo.upper()
            df = pd.read_sql_query(sql, con = conexion)
            return { 'State'                : 0,
                    'Descripción'           :"Consulta realizada exitosamente.",
                    'Fecha actual'          : datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Nombre'                : df['Nombre'][0],
                    'Creado'                : df['Creado'][0],
                    'Usuario creador'       : df['Usuario_creador'][0],
                    'Actualizado'           : df['Actualizado'][0],
                    'Actualizar usuario'    : df['Actualizar_usuario'][0] }
        
        #except Exception as e:
        #    return {'State': 1, 'Descripción': e, 'Intento': 2}

    #    except:
     #      return {'State': 1 , 'Descripción': 'Ruta no encontrada, pruebe con otra revisando la BBDD.'}
