
import json

from pymongo import MongoClient

from procesamiento.frecuencias import Frecuencias

class Resultados:
    def __init__(self):
        with open('conexiones.json') as c:
            j = json.load(c)
            
        usuario = j['resultados']['usuario']
        pwd = j['resultados']['pwd']
        server = j['resultados']['server']

        conexion = "mongodb://" + usuario + ":" + pwd + "@" + server + "/"

        self.bd = MongoClient(conexion).resultados

        
    def actualizar_freqs(self, resultados):

        for r in resultados:

            query = {'fecha': r['fecha'], 'diario': r['diario'], 'categoria':r['categoria']}
            r_actuales = self.bd.frecuencias.find_one(query)

            if not r_actuales: # si no existe, inserto directo el resultado.
                doc = {'fecha': r['fecha'], 'diario': r['diario'], 'categoria': r['categoria'], 'total': r['total'],'ter_tit': r['ter_tit'], 'ver_tit': r['ver_tit'], 'per_tit': r['per_tit'], 'ter_txt': r['ter_txt'], 'ver_txt': r['ver_txt'], 'per_txt': r['per_txt']}
                self.bd.frecuencias.insert_one(doc)
                continue
                
            total = r_actuales['total'] + r['total']

            ter_tit = Frecuencias.sumar_freqs(r_actuales['ter_tit'], r['ter_tit'], 30)
            ver_tit = Frecuencias.sumar_freqs(r_actuales['ver_tit'], r['ver_tit'], 15)
            per_tit = Frecuencias.sumar_freqs(r_actuales['per_tit'], r['per_tit'], 15)

            ter_txt = Frecuencias.sumar_freqs(r_actuales['ter_txt'], r['ter_txt'], 50)
            ver_txt = Frecuencias.sumar_freqs(r_actuales['ver_txt'], r['ver_txt'], 15)
            per_txt = Frecuencias.sumar_freqs(r_actuales['per_txt'], r['per_txt'], 15)

            doc = {'fecha': r['fecha'], 'diario': r['diario'], 'categoria': r['categoria'], 'total': total,'ter_tit': ter_tit, 'ver_tit': ver_tit, 'per_tit': per_tit, 'ter_txt':ter_txt, 'ver_txt': ver_txt, 'per_txt': per_txt}
            self.bd.frecuencias.find_one_and_replace(query, doc, upsert=True)
