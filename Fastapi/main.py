from fastapi import FastAPI, Query
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware


MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "proyectov1"

client = MongoClient("mongodb://localhost:27017/")
db = client[MONGODB_DB]
collection_prop = db["propiedades"]
collection_proptoctoc = db["proptoctoc"]
collection_topprop = db["proptopprop"]

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_all")
async def get_all():
    propiedades = list(collection_prop.find())
    proptoctoc = list(collection_proptoctoc.find())
    proptopprop = list(collection_topprop.find())
    documentos_list = [document_to_dict(documento) for documento in propiedades + proptoctoc + proptopprop]
   
    formated_list = formater_uf(documentos_list) 
    
    return JSONResponse(content=formated_list)


def document_to_dict(document):
    # Convierte el ObjectId a su representación de cadena
    document["_id"] = str(document["_id"])
    return document


def formater_uf(documentos):
    for item in documentos:
        if(item["valor"] == str):
            d = item["valor"]
            d = d[:-3]
            d = d.replace(".","")
            d = int(d)
            item["valor"]=d

        if(item["dormitorios"] == str):
            dorm = item["dormitorios"]
            dorm = int(dorm)
            item["dormitorios"] = dorm

        if(item["baños"] == str):
            b = item["baños"]
            b = int(b)
            item["baños"] = b

        if(item["superficie"] == str):
            s = item["superficie"]
            s = s[:-3]
            s = float(s)
            item["superficie"] = s

    return documentos

 