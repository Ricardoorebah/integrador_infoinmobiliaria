import scrapy
from realstate.items import PropiedadItem

class UsatusubSpider(scrapy.Spider):
    name = "usatusub"
    allowed_domains = ["usatusubsidio.com"]
    start_urls = ["https://usatusubsidio.com/?filters=region[152]"]

    def parse(self, response):
        propiedades = response.css('li.product')

        for propiedad in propiedades:
            
            prop_url = propiedad.css('div a').attrib['href']
            yield response.follow(prop_url,  callback=self.parse_propiedad)

        #Método para recorrer siguientes páginas, si las hubiese    
        sgte_pag = response.css('li a.next ::attr(href)').get()

        if sgte_pag is not None:
            sgte_pag_url = 'https://usatusubsidio.com/' + sgte_pag
            yield response.follow(sgte_pag_url, callback=self.parse)
            
    
    def parse_propiedad(self, response):
        
        table_rows = response.css("table tr")
        p_item = PropiedadItem()

        p_item['url_origen'] = response.url
        p_item['nombre'] = response.css('.product_title::text').get()
        p_item['valor'] = response.css('.amount bdi::text').get()
        p_item['dormitorios'] = table_rows[0].css('td.woocommerce-product-attributes-item__value ::text').get() 
        p_item['baños'] = table_rows[1].css('td.woocommerce-product-attributes-item__value ::text').get()
        p_item['superficie'] = table_rows[2].css('td.woocommerce-product-attributes-item__value ::text').get()
        p_item['tipo_propiedad'] = table_rows[3].css('td.woocommerce-product-attributes-item__value ::text').get()
        p_item['region'] = table_rows[6].css('td.woocommerce-product-attributes-item__value ::text').get()
        p_item['comuna'] = table_rows[7].css('td.woocommerce-product-attributes-item__value ::text').get()
        p_item['tipo_financiamiento'] = table_rows[8].css('td.woocommerce-product-attributes-item__value ::text').get()
        p_item['img_ref'] = response.css('div.woocommerce-product-gallery__image a ::attr(href)').get()
        
        yield p_item
