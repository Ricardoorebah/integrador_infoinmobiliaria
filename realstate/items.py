# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

#Item por defecto
class RealstateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PropiedadItem(scrapy.Item):
    url_origen = scrapy.Field()
    nombre = scrapy.Field()
    valor = scrapy.Field()
    dormitorios = scrapy.Field()
    baños = scrapy.Field()
    superficie = scrapy.Field()
    tipo_propiedad = scrapy.Field()
    region = scrapy.Field()
    comuna = scrapy.Field()
    tipo_financiamiento = scrapy.Field()
    img_ref = scrapy.Field()
    