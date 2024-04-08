import scrapy
from realstate.items import PropiedadItem


class ToppropSpider(scrapy.Spider):
    name = "topprop"
    allowed_domains = ["www.toppropiedades.cl"]
    start_urls = ["https://www.toppropiedades.cl/propiedades/venta/casa/los-lagos"]

    def parse(self, response):
        propiedades = response.css('.grid_propiedad_perfil')

        for propiedad in propiedades:
            prop_url = 'https://www.toppropiedades.cl/' + propiedad.css('.grid_propiedad_perfil ::attr(href)').get()

            # Se obtiene el src de la imagen en la página que lista todas las propiedades
            img_src_menu = propiedad.css('img.grid_propiedad_foto_i::attr(src)').get()

            # Se crea un diccionario para almacenar la información que se desea extraer
            property_info = {
                'url_origen': prop_url,
                'img_ref': ''  # Inicialmente, antes de obtener la URL de la imagen
            }

            # Si se encuentra el src de la imagen, actualiza el diccionario
            if img_src_menu:
                property_info['img_ref'] = 'https://www.toppropiedades.cl/' + img_src_menu

            # Sigue con la extracción de información específica de la propiedad
            yield scrapy.Request(url=prop_url, callback=self.parse_propiedad, meta={'property_info': property_info})

    def parse_propiedad(self, response):
        p_item = PropiedadItem()

        # Accede a la información almacenada en el diccionario 'property_info' desde meta
        property_info = response.meta.get('property_info', {})

        p_item['url_origen'] = property_info.get('url_origen', '')
        p_item['nombre'] = response.css('.property_titulo::text').get()
        p_item['valor'] = response.css('.property_conversion::text').get()
        p_item['dormitorios'] = response.xpath('/html/body/div/div[1]/div[2]/div[2]/div[2]/div[1]/p[4]/text()').get()
        p_item['baños'] = response.xpath('/html/body/div/div[1]/div[2]/div[2]/div[2]/div[1]/p[5]/text()').get()
        p_item['superficie'] = response.xpath('/html/body/div/div[1]/div[2]/div[2]/div[2]/div[1]/p[2]/text()').get()
        p_item['tipo_propiedad'] = response.xpath('/html/body/div/div[1]/div[1]/a[3]/text()').get()
        p_item['region'] = response.xpath('/html/body/div/div[1]/div[1]/a[4]/text()').get()
        p_item['comuna'] = response.xpath('/html/body/div/div[1]/div[2]/div[1]/div[1]/div[2]/text()').get()
        p_item['tipo_financiamiento'] = response.xpath('/html/body/div/div[1]/div[1]/a[2]/text()').get()
        p_item['img_ref'] = property_info.get('img_ref', '')

        yield p_item