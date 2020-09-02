



class Procesador:
    def __init__(self):
        pass

    def sumar_freqs(self, medio):

        freqs_actuales_json = self.__levantar_freqs__(path)
        freqs_actuales = Freqs(freqs_actuales_json)

        
        freqs_nuevas_json = medio.freqs()
        freqs_nuevas = Freqs(freqs_nuevas_json)

        freqs_actuales.sumar(freqs_nuevas) 


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