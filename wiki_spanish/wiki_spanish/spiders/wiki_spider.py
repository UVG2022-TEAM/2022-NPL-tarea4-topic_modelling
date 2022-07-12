import scrapy
import re
import unihandecode
import pipe
from collections import Counter
import matplotlib.pyplot as plt
from pipe import select
from wiki_spanish.items import WikipediaItem

class wikiSpider(scrapy.Spider):
    name = 'wiki_spanish'
    allowed_domains = ['es.wikipedia.org']
    start_urls = ['https://es.wikipedia.org/wiki/Wikipedia:Art%C3%ADculos_destacados']

    def parse(self, response):
        i = 0
        table = response.css('table')[2]
        links = table.css('tr')[2]

        for link in links.css('a'):
            yield response.follow(link.attrib.get('href'), callback=self.parse_article_data)
            #i += 1
            #if i == 10: # Solo leer el primer link
             #   break

    def parse_article_data(self, response):

        def conv(org_list, seperator=' '):
            return seperator.join(org_list).lower()

        contenido = response.xpath('/html/body')
        parrafo_grande = ''
        for parrafo in contenido:
            lista_parrafo_grande = parrafo.xpath('//p//text()').getall()
            sin_unicode = list(lista_parrafo_grande | select(lambda x: unihandecode.unidecode(x)))
            sin_especial = [re.sub('[^a-zA-Z0-9]+|[\]\[\b\d+\b]', ' ', _) for _ in sin_unicode]
            sin_espacios = list(sin_especial | select(lambda x: x.strip()))
            sin_blancos = [x for x in sin_espacios if x]
            sin_dobles = [re.sub(r' +', ' ', string) for string in sin_blancos]
            parrafo_grande += conv(sin_dobles) + ' '

        yield WikipediaItem (
            parrafo = parrafo_grande
            )
