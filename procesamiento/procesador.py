import nltk
import string


class Procesador:
    def __init__(self):
        pass

    def sumar_freqs(self, medio):
        # ver de como hacer con las categorias: un .json por diario o un .json por diario/categoria
        # CREO Q MEJOR un .json por diario/categoria, haciendo 'for cat in medio.categorias:', menos intensidad en el uso de memoria.
        for categoria in medio.categorias:
            path = medio.etiqueta + '_' + categoria + '.json'

            freqs_actuales_json = self.__levantar_freqs__(path)
            freqs_actuales = Freqs(freqs_actuales_json)

            freqs_nuevas_json = self.__noticias2freqs__(medio.noticias)
            freqs_nuevas = Freqs(freqs_nuevas_json)

            freqs_actuales.sumar(freqs_nuevas)

            self.__serializar_freqs__(path, freqs_actuales)

    def __noticias2freqs__(self, noticias):
        
        #for noticia in noticias:
        freqs = FreqDist()
        for noticia in noticias['noticias']:
            # txt = noticia.texto
            txt = noticia['texto']

            txt = txt.lower()

            signos = string.punctuation + "¡¿\n"
            txt = txt.translate(str.maketrans('áéíóúý', 'aeiouy', signos))

            palabras = nltk.tokenize.word_tokenize(txt)

            with open('stopwords.txt') as s:
                stopwords = s.read().split('\n')

            palabras = [p for p in palabras if p not in stopwords and len(p) > 2 and p and not p.isnumeric()]

            for p in palabras:
                freqs[p] += 1
        
        return freqs

    def __limpiar__(self, palabras):

        # saco numeros
        palabras = [palabra for palabra in palabras if not palabra.is_digit]

        # todo a minuscula
        palabras = [palabra.lower() for palabra in palabras]

        # saco signos de puntuacion
        signos = string.punctuation + "¡¿\n"
        palabras = [palabra.translate(str.maketrans('áéíóúý', 'aeiouy', signos)) for palabra in palabras]

        # saco stopwords
        locales_stopwords = codecs.open("stopwords.txt", 'r', encoding="utf-8").read().split("\r\n")

        palabras = [palabra for palabra in palabras if palabra not in locales_stopwords]

        # saco palabras de una sola letra y saco los espacios en blacno
        palabras = [palabra.strip() for palabra in palabras if len(palabra) > 1]

        # saco lugares vacios
        palabras = [palabra for palabra in palabras if palabra]

        return palabras