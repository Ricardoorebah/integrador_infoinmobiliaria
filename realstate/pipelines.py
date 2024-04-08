import re
import pymongo
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

def clean_valor(valor):
    if valor:
        cleaned_valor = valor.strip()
        return cleaned_valor
    return None

def clean_valor_topprop(valor):
    if valor:
        cleaned_valor = re.search(r'([\d,\.]+)\s*UF', valor)
        if cleaned_valor:
            return cleaned_valor.group(1).replace(',', '.')
    return None

def clean_superficie_usatusub(superficie):
    if superficie:
        cleaned_superficie = re.search(r'([\d,\.]+)\s*[m²]', superficie)
        if cleaned_superficie:
            return cleaned_superficie.group(1).replace(',', '.')
    return None

def clean_superficie_topprop(superficie):
    if superficie:
        cleaned_superficie = re.search(r'([\d,\.]+)\s*[Mm²]', superficie)
        if cleaned_superficie:
            return cleaned_superficie.group(1).replace(',', '.')
    return None

def clean_dormitorios_topprop(dormitorios):
    if dormitorios:
        cleaned_dormitorios = re.search(r'(\d+)', dormitorios)
        if cleaned_dormitorios:
            return cleaned_dormitorios.group(1)
    return None

def clean_baños_topprop(baños):
    if baños:
        cleaned_baños = re.search(r'(\d+)', baños)
        if cleaned_baños:
            return cleaned_baños.group(1)
    return None

class MongoDBPipeline(object):

    def __init__(self):
        self.settings = get_project_settings()
        connection = pymongo.MongoClient(
            self.settings['MONGODB_SERVER'],
            self.settings['MONGODB_PORT']
        )
        self.db = connection[self.settings['MONGODB_DB']]
    
    def open_spider(self, spider):
        # Antes de abrir la araña, elimina todos los documentos en la colección
        if spider.name == 'usatusub':
            self.collection = self.db['propiedades']
            self.clean_valor_function = clean_valor
        elif spider.name == 'topprop':
            self.collection = self.db['proptopprop']
            self.clean_valor_function = clean_valor_topprop
        else:
            raise ValueError(f"Spider '{spider.name}' no tiene una colección asociada.")

        self.collection.delete_many({})

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            # Limpia el valor antes de insertar
            item['valor'] = self.clean_valor_function(item['valor'])
            
            # Limpia la superficie antes de insertar
            if spider.name == 'usatusub':
                item['superficie'] = clean_superficie_usatusub(item['superficie'])
            elif spider.name == 'topprop':
                item['superficie'] = clean_superficie_topprop(item['superficie'])
            else:
                raise ValueError(f"Spider '{spider.name}' no tiene una función de limpieza de superficie asociada.")
            
            # Limpia los dormitorios antes de insertar
            if spider.name == 'topprop':
                item['dormitorios'] = clean_dormitorios_topprop(item['dormitorios'])
            
            # Limpia los baños antes de insertar
            if spider.name == 'topprop':
                item['baños'] = clean_baños_topprop(item['baños'])

            # Inserta en la colección específica para la araña
            self.collection.insert_one(dict(item))
                
        return item
