
import json

from pymongo import MongoClient

from procesamiento.frecuenciasgcp import Frecuencias

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

            query = {'fecha': r['fecha'], 'diario': r['diario'], 'seccion':r['seccion']}
            r_actuales = self.bd.frecuencias.find_one(query)

            if not r_actuales: # si no existe, inserto directo el resultado.
                doc = {'fecha': r['fecha'], 'diario': r['diario'], 'seccion': r['seccion'], 'total': r['total'],
                'adjtit': r['adjtit'], 'sustit': r['sustit'], 'vertit': r['vertit'], 'enttit': r['enttit'],
                'adjtxt': r['adjtxt'], 'sustxt': r['sustxt'], 'vertxt': r['vertxt'], 'enttxt': r['enttxt']}
                self.bd.frecuencias.insert_one(doc)
                continue
                
            total = r_actuales['total'] + r['total']

            adjtit = Frecuencias.sumar_freqs(r_actuales['adjtit'], r['adjtit'], 30)
            sustit = Frecuencias.sumar_freqs(r_actuales['sustit'], r['sustit'], 15)
            vertit = Frecuencias.sumar_freqs(r_actuales['vertit'], r['vertit'], 15)
            enttit = Frecuencias.sumar_freqs(r_actuales['enttit'], r['enttit'], 15)

            adjtxt = Frecuencias.sumar_freqs(r_actuales['adjtxt'], r['adjtxt'], 50)
            sustxt = Frecuencias.sumar_freqs(r_actuales['sustxt'], r['sustxt'], 50)
            vertxt = Frecuencias.sumar_freqs(r_actuales['vertxt'], r['vertxt'], 50)
            enttxt = Frecuencias.sumar_freqs(r_actuales['enttxt'], r['enttxt'], 40)

            doc = {'fecha': r['fecha'], 'diario': r['diario'], 'seccion': r['seccion'], 'total': total,
            'adjtit': adjtit, 'sustit': sustit, 'vertit': vertit, 'enttit': enttit,
            'adjtxt': adjtxt, 'sustxt': sustxt, 'vertxt': vertxt, 'enttxt': enttxt
            }
            self.bd.frecuencias.find_one_and_replace(query, doc, upsert=True)
