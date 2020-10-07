
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
            categoria = ""
            if sfecha >= "20191210":
                categoria = "alberto"

            if sfecha < "20191210" and sfecha >= "20151210":
                categoria = "macri"

            if sfecha < "20151210" and sfecha >= "20071210":
                categoria = "cristina"

            if sfecha < "20071210":
                categoria = "nestor"

            # if self.contar_noticias(diario=diario, categorias=categoria, url=url):
            #     continue
            if categoria != "nestor":
                continue

            if resultados.bd.frecuencias.find_one({'diario': diario, 'categoria': categoria, 'fecha': fecha.strftime('%Y%m%d%H%M%S'), 'url':url}):
                continue

            while resultados.bd.frecuencias.find_one({'diario': diario, 'categoria': categoria, 'fecha': fecha.strftime('%Y%m%d%H%M%S')}):
                fecha += datetime.timedelta(seconds=10)

            while existe_fecha(fecha, buffer_resultado):
                fecha += datetime.timedelta(seconds=10)

            # buffer_kiosco.append({'diario': diario, 'cat':categoria, 'fecha': fecha, 'url':url, 'titulo':titulo, 'texto':texto})

            # if len(buffer_kiosco) >= 100:
            #     self.bd.noticias.insert_many(buffer_kiosco)
            #     agregados += 100
            #     buffer_kiosco = []
            #     print('total procesados: ' + str(total) + '. agregados ' + str(agregados) + ' en total en Kiosco')

            f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt = freqs.tituloytexto2freqs(titulo,texto)

            buffer_resultado.append({'diario':diario, 'categoria': categoria, 'fecha': fecha.strftime('%Y%m%d%H%M%S'), 'url':url, 'f_ter_tit': f_ter_tit, 'f_ver_tit': f_ver_tit, 'f_per_tit': f_per_tit, 'f_ter_txt': f_ter_txt, 'f_ver_txt': f_ver_txt, 'f_per_txt': f_per_txt})

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
    categoria='editorial'
    editoriales = k.noticias(diario=diario, categorias=categoria)

    buffer_resultado = []
    for e in editoriales:
        f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt = freqs.tituloytexto2freqs(e.titulo,e.texto)
        buffer_resultado.append({'diario':diario, 'categoria': categoria, 'fecha': e.fecha.strftime('%Y%m%d%H%M%S'), 'url':e.url, 'f_ter_tit': f_ter_tit, 'f_ver_tit': f_ver_tit, 'f_per_tit': f_per_tit, 'f_ter_txt': f_ter_txt, 'f_ver_txt': f_ver_txt, 'f_per_txt': f_per_txt})

    resultados.bd.frecuencias.insert_many(buffer_resultado)