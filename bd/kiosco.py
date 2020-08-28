import datetime
import dateutil
import logging

import sys

import yaml

import boto3
from boto3.dynamodb.conditions import Key

class Kiosco:
    def __init__(self, fecha=None):
        self.db = boto3.resource('dynamodb', region_name = 'us-east-1')

    def actualizar_diario(self, diario):
        # si no hay noticias, entonces no actualizo nada, salgo
        if len(diario.noticias) == 0:
            return False

        # recupero tabla del diario
        tabla = self.db.Table(diario.etiqueta)

        # recupero las urls del dia de hoy y de ayer para no subir dos veces la misma noticia
        hoy = int(datetime.date.today().strftime('%Y%m%d'))

        # filtro las noticias que ya estan: si la url esta en la anterior o si su fecha es de ayer, entonces no guardo
        noticias = [{'fecha': n.fecha.strftime('%Y%m%d%H%M%S'), 'url':n.url, 'diario':n.diario, 'cat':n.categoria,'titulo':n.titulo, 'texto':n.texto} for n in diario.noticias]
        urls = [{'url': n.url, 'cat': n.categoria} for n in diario.noticias]

        # guardo las noticias con clave=YYYMMDD particion=HHMM
        hoy_hms = int((datetime.datetime.today() - datetime.timedelta(hours=3)).strftime("%H%M%S"))
        item = {'fecha': hoy, 'hora': hoy_hms, 'noticias': noticias, 'urls': urls}

        rta = tabla.put_item(Item = item)

        if rta['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False


    def noticias(self, fecha=None, diario=None, categorias=None, fecha_in=True, url_in=True, diario_in=True, cat_in=True, tit_in=True, text_in=True):
        return []
        # query = {}

        # if fecha:
        #     if type(fecha) is dict:
        #         desde = datetime.datetime(fecha['desde'].year, fecha['desde'].month, fecha['desde'].day, 0,0,0)
        #         hasta = datetime.datetime(fecha['hasta'].year, fecha['hasta'].month, fecha['hasta'].day, 23,59,59)                
        #     else:
        #         desde = datetime.datetime(fecha.year, fecha.month, fecha.day, 0,0,0)
        #         hasta = datetime.datetime(fecha.year, fecha.month, fecha.day, 23,59,59)
        #     query['fecha']={"$gte":desde, "$lte":hasta}

        # if diario:
        #     query['diario']=diario

        # if categorias:
        #     if len(categorias) > 0:
        #         query['cat']={"$in":categorias}

        # projection = {'fecha':fecha_in, 'url':url_in, 'diario':diario_in, 'cat':cat_in, 'titulo':tit_in, 'texto':text_in }

        # return self.bd.noticias.find(query, projection)

    def contar_noticias(self, fecha=None, diario=None, categorias=None, url=None):
        rta = {}
        tabla = None
        desde, hasta = 0, 0

        if diario:
            if type(diario) is str:
                # recupero la tabla del diario
                tabla = self.db.Table(diario)
            else:
                # si no es string entonces error. 
                return -1
        else:
            # hay que especificar 1 diario. 
            return -1

        if fecha:
            if type(fecha) is dict:
                desde = int(fecha['desde'].strftime('%Y%m%d'))
                hasta = int(fecha['hasta'].strftime('%Y%m%d'))
                rta = tabla.scan(FilterExpression = Key('fecha').between(desde, hasta), ProjectionExpression = 'urls')       
            else:
                dia = int(fecha.strftime('%Y%m%d'))
                rta = tabla.scan(FilterExpression = Key('fecha').eq(dia), ProjectionExpression = 'urls')
        else:
            rta = tabla.scan(ProjectionExpression = 'urls')

        if categorias:
            if type(categorias) is list and len(categorias) > 0:
                cats = categorias
            else:
                cats = [categorias]

        if url:
            if type(url) is list and len(url) > 0:
                urls = url
            else:
                urls = [url]

        # cuento los items que cumplen con lo pedido
        conteo = 0
        for i in rta['Items']:
            if 'urls' not in i:
                # item mal formado
                continue
            for u in i['urls']:
                if 'cat' not in u or 'url' not in u:
                    # item mal formado
                    continue

                if categorias and u['cat'] not in cats:
                    # item no es de las categorias buscadas
                    continue
                

                if url and u['url'] not in urls:
                    # item no tiene url buscada
                    continue
                
                conteo += 1
            
        return conteo

    def urls (self, fecha=None, diario=None, categorias=None):
        rta = {}
        tabla = None
        desde, hasta = 0, 0

        if diario:
            if type(diario) is str:
                # recupero la tabla del diario
                tabla = self.db.Table(diario)
            else:
                # si no es string entonces error. 
                return -1
        else:
            # hay que especificar 1 diario. 
            return -1

        if fecha:
            if type(fecha) is dict:
                desde = int(fecha['desde'].strftime('%Y%m%d'))
                hasta = int(fecha['hasta'].strftime('%Y%m%d'))
                rta = tabla.scan(FilterExpression = Key('fecha').between(desde, hasta), ProjectionExpression = 'urls')       
            else:
                dia = int(fecha.strftime('%Y%m%d'))
                rta = tabla.scan(FilterExpression = Key('fecha').eq(dia), ProjectionExpression = 'urls')
        else:
            rta = tabla.scan(ProjectionExpression = 'urls')

        if categorias:
            if type(categorias) is list and len(categorias) > 0:
                cats = categorias
            else:
                cats = [categorias]

        # cuento los items que cumplen con lo pedido
        urls = []
        for i in rta['Items']:
            if 'urls' not in i:
                # item mal formado
                continue
            for u in i['urls']:
                if 'cat' not in u or 'url' not in u:
                    # item mal formado
                    continue

                if categorias and u['cat'] not in cats:
                    # item no es de las categorias buscadas
                    continue

                urls.append(u['url'])
            
        return urls

    def categorias_existentes(self, fecha=None, diario=None, url=None):
        return []
        # query = {}

        # if fecha:
        #     if type(fecha) is dict:
        #         desde = datetime.datetime(fecha['desde'].year, fecha['desde'].month, fecha['desde'].day, 0,0,0)
        #         hasta = datetime.datetime(fecha['hasta'].year, fecha['hasta'].month, fecha['hasta'].day, 23,59,59)                
        #     else:
        #         desde = datetime.datetime(fecha.year, fecha.month, fecha.day, 0,0,0)
        #         hasta = datetime.datetime(fecha.year, fecha.month, fecha.day, 23,59,59)
        #     query['fecha']={"$gte":desde, "$lte":hasta}

        # if diario:
        #     query['diario']=diario

        # if url:
        #     query['url']=url

        # return self.bd.noticias.distinct("cat", query)