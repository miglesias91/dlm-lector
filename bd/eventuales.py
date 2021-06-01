import json
import datetime

from pymongo import MongoClient

from bd.kioscomongo import Kiosco

from bd.resultados import Resultados
from procesamiento.frecuenciasspacy import Frecuencias

def subir_historicos(path_discursos_historicos):
    buffer_kiosco = []
    buffer_resultado = []

    resultados = Resultados()
    freqs = Frecuencias()
    k = Kiosco()
    bd = k.bd
    total = 0
    agregados = 0
    with open(path_discursos_historicos) as f:
        for linea in f:
            total += 1
            jdiscurso = json.loads(linea)

            texto = jdiscurso['texto']

            if not texto:
                continue

            diario = jdiscurso['diario']
            url = jdiscurso['url']
            titulo = jdiscurso['titulo']

            fecha = datetime.datetime.strptime(jdiscurso['fecha']['$date'], '%Y-%m-%dT%H:%M:%SZ')

            # if fecha.strftime('%Y%m%d%H%M%S') > '20071206233745':
            #     continue

            sfecha = fecha.strftime('%Y%m%d')
            seccion = ""
            if sfecha >= "20191210":
                seccion = "alberto"

            if sfecha < "20191210" and sfecha >= "20151210":
                seccion = "macri"

            if sfecha < "20151210" and sfecha >= "20071210":
                seccion = "cristina"

            if sfecha < "20071210":
                seccion = "nestor"

            # if self.contar_noticias(diario=diario, secciones=seccion, url=url):
            #     continue
            if seccion != "nestor":
                continue

            if resultados.bd.frecuencias.find_one({'diario': diario, 'seccion': seccion, 'fecha': fecha.strftime('%Y%m%d%H%M%S'), 'url':url}):
                continue

            while resultados.bd.frecuencias.find_one({'diario': diario, 'seccion': seccion, 'fecha': fecha.strftime('%Y%m%d%H%M%S')}):
                fecha += datetime.timedelta(seconds=10)

            while existe_fecha(fecha, buffer_resultado):
                fecha += datetime.timedelta(seconds=10)

            # buffer_kiosco.append({'diario': diario, 'cat':seccion, 'fecha': fecha, 'url':url, 'titulo':titulo, 'texto':texto})

            # if len(buffer_kiosco) >= 100:
            #     self.bd.noticias.insert_many(buffer_kiosco)
            #     agregados += 100
            #     buffer_kiosco = []
            #     print('total procesados: ' + str(total) + '. agregados ' + str(agregados) + ' en total en Kiosco')

            f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt = freqs.tituloytexto2freqs(titulo,texto)

            buffer_resultado.append({'diario':diario, 'seccion': seccion, 'fecha': fecha.strftime('%Y%m%d%H%M%S'), 'url':url, 'f_ter_tit': f_ter_tit, 'f_ver_tit': f_ver_tit, 'f_per_tit': f_per_tit, 'f_ter_txt': f_ter_txt, 'f_ver_txt': f_ver_txt, 'f_per_txt': f_per_txt})

            if len(buffer_resultado) >= 100:
                resultados.bd.frecuencias.insert_many(buffer_resultado)
                agregados += 100
                buffer_resultado = []
                print('total procesados: ' + str(total) + '. agregados ' + str(agregados) + ' en total en Resultados')

    if len(buffer_resultado):
        bd.noticias.insert_many(buffer_resultado)
        print('total procesados: ' + str(total) + '. agregados ' + str(agregados+len(buffer_kiosco)) + ' en total en Resultados')

    print('fin')

def existe_fecha(echa, buffer_resultado):
    sfecha = fecha.strftime('%Y%m%d%H%M%S')
    for r in buffer_resultado:
        if sfecha == r['fecha']:
            return True
    return False

def resultados_editoriales():
    resultados = Resultados()
    freqs = Frecuencias()
    k = Kiosco()
    total = 0
    agregados = 0

    diario='diariodeleuco'
    seccion='editorial'
    editoriales = k.noticias(diario=diario, secciones=seccion)

    buffer_resultado = []
    for e in editoriales:
        f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt = freqs.tituloytexto2freqs(e.titulo,e.texto)
        buffer_resultado.append({'diario':diario, 'seccion': seccion, 'fecha': e.fecha.strftime('%Y%m%d%H%M%S'), 'url':e.url, 'f_ter_tit': f_ter_tit, 'f_ver_tit': f_ver_tit, 'f_per_tit': f_per_tit, 'f_ter_txt': f_ter_txt, 'f_ver_txt': f_ver_txt, 'f_per_txt': f_per_txt})

    resultados.bd.frecuencias.insert_many(buffer_resultado)

def discursos_freqs():
    freqs = Frecuencias()

    with open('/home/manu/repos/dlm/lector/conexiones-oracle.json') as c:
        j = json.load(c)
        
    usuario = j['resultados']['usuario']
    pwd = j['resultados']['pwd']
    server = j['resultados']['server']

    conexion = "mongodb://" + usuario + ":" + pwd + "@" + server + "/"

    with open('/home/manu/repos/dlm/discursos.json') as f:
        discursos = f.readlines()

    print('discursos totales: ' + str(len(discursos)))
    buffer_resultado = []
    i = 1
    for discurso in discursos:
        d = json.loads(discurso)

        fecha = datetime.datetime.strptime(d['fecha']['$date'], '%Y-%m-%dT%H:%M:%SZ')

        sfecha = fecha.strftime('%Y%m%d')
        shora = fecha.strftime('%H%M%S')
        presidente = ""
        if sfecha >= "20191210":
            presidente = "alberto"

        if sfecha < "20191210" and sfecha >= "20151210":
            presidente = "macri"

        if sfecha < "20151210" and sfecha >= "20071210":
            presidente = "cristina"

        if sfecha < "20071210":
            presidente = "nestor"
        
        adjtit, sustit, vertit, enttit, adjtxt, sustxt, vertxt, enttxt = freqs.tituloytexto2freqs(d['titulo'], d['texto'])
        buffer_resultado.append({
            'presidente': presidente, 'fecha': sfecha, 'hora': shora,'url':d['url'],
            'adjtit': adjtit, 'sustit': sustit, 'vertit': vertit, 'enttit': enttit,
            'adjtxt': adjtxt, 'sustxt': sustxt, 'vertxt': vertxt, 'enttxt': enttxt
            })
        
        print(str(i))
        i = i + 1

    bd = MongoClient(conexion).resultados
    bd.frecuencias_discursos.insert_many(buffer_resultado)
