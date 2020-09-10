import string

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

class Frecuencias:
    def __init__(self, noticias):
        self.cliente = language.LanguageServiceClient()

        self.stopwords = []
        with open('stopwords.txt') as s:
           self.stopwords = s.read().split('\n')

        self.sustantivos_comunes = []
        with open('sustantivos.txt') as s:
           self.sustantivos_comunes = s.read().split('\n')

        self.puntuacion = string.punctuation + "¡¿\n"

        self.noticias = {}
        self.resultados = []

        for n in noticias:
            sfecha = n.fecha.strftime('%Y%m%d')
            if sfecha not in self.noticias:
                self.noticias[sfecha] = {}

            if n.diario not in self.noticias[sfecha]:
                self.noticias[sfecha][n.diario] = {}

            if n.categoria not in self.noticias[sfecha][n.diario]:
                self.noticias[sfecha][n.diario][n.categoria] = []

            self.noticias[sfecha][n.diario][n.categoria].append(n)

    def calcular(self):
        notis = []
        for fecha, diarios in self.noticias.items():
            for diario, categorias in diarios.items():
                for categoria, noticias in categorias.items():
                    f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt = self.__noticias2freqs__(noticias)

                    resultado = {'fecha': fecha, 'diario': diario, 'categoria': categoria, 'total': len(noticias), 'ter_tit':f_ter_tit, 'ver_tit': f_ver_tit, 'per_tit': f_per_tit, 'ter_txt': f_ter_txt, 'ver_txt': f_ver_txt, 'per_txt': f_per_txt }
                    self.resultados.append(resultado)

    def tokens(self, texto):
        texto =  texto.replace('.', '. ')

        doc = types.Document(content=texto, type= enums.Document.Type.PLAIN_TEXT, language='es')

        return self.cliente.analyze_syntax(doc, encoding_type = enums.EncodingType.UTF8)
    
    def entidades(self, texto):
        texto =  texto.replace('.', '. ')

        doc = types.Document(content=texto, type= enums.Document.Type.PLAIN_TEXT, language='es')

        return self.cliente.analyze_entities(doc, encoding_type = enums.EncodingType.UTF8)

    def __noticias2freqs__(self, noticias):

        freq_terminos_texto = {}
        freq_personas_texto = {}
        freq_verbos_texto = {}

        freq_terminos_titulo = {}
        freq_personas_titulo = {}
        freq_verbos_titulo = {}

        for noticia in noticias:

            tokens_titulo = self.tokens(noticia.titulo)
            entidades_titulo = self.entidades(noticia.titulo)

            tokens_texto = self.tokens(noticia.texto)
            entidades_texto = self.entidades(noticia.texto)

            nuevas_freq_terminos_titulo = self.freq_terminos(tokens_titulo, 30)
            nuevas_freq_verbos_titulo = self.freq_verbos(tokens_titulo, 15)
            nuevas_freq_personas_titulo = self.freq_personas(entidades_titulo, 15)

            nuevas_freq_terminos_texto = self.freq_terminos(tokens_texto, 50)
            nuevas_freq_verbos_texto = self.freq_verbos(tokens_texto, 15)
            nuevas_freq_personas_texto = self.freq_personas(entidades_texto, 15)

            freq_terminos_titulo = Frecuencias.sumar_freqs(freq_terminos_titulo, nuevas_freq_terminos_titulo, 30)
            freq_verbos_titulo = Frecuencias.sumar_freqs(freq_verbos_titulo, nuevas_freq_verbos_titulo, 15)
            freq_personas_titulo = Frecuencias.sumar_freqs(freq_personas_titulo, nuevas_freq_personas_titulo, 15)

            freq_terminos_texto = Frecuencias.sumar_freqs(freq_terminos_texto, nuevas_freq_terminos_texto, 50)
            freq_verbos_texto = Frecuencias.sumar_freqs(freq_verbos_texto, nuevas_freq_verbos_texto, 15)
            freq_personas_texto = Frecuencias.sumar_freqs(freq_personas_texto, nuevas_freq_personas_texto, 15)

        return freq_terminos_titulo, freq_verbos_titulo, freq_personas_titulo, freq_terminos_texto, freq_verbos_texto, freq_personas_texto

    def freq_terminos(self, doc, top):
        freqs = {}
        for t in doc.tokens:
            if t.part_of_speech.tag == types.PartOfSpeech.Tag.NOUN and t.part_of_speech.proper == types.PartOfSpeech.Proper.NOT_PROPER and len(t.text.content) > 2 and t.lemma.lower() not in self.sustantivos_comunes and t.text.content.lower() not in self.stopwords:
                k = t.lemma.lower().translate(str.maketrans('','', self.puntuacion))
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def freq_verbos(self, doc, top):
        freqs = {}
        for t in doc.tokens:
            if t.part_of_speech.tag == types.PartOfSpeech.Tag.VERB:
                k = t.lemma.lower().translate(str.maketrans('','', self.puntuacion))
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def freq_personas(self, doc, top):
        freqs = {}
        for e in doc.entities:
            if e.type == types.Entity.PERSON:
                k = e.name.translate(str.maketrans('','', self.puntuacion))
                if k in freqs:
                    freqs[k] += len(e.mentions)
                else:
                    freqs[k] = len(e.mentions)

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    @staticmethod
    def sumar_freqs(freqs, freqs_nuevas, top):
        for k, v in freqs_nuevas.items():
            if k in freqs:
                freqs[k] += v
            else:
                freqs[k] = v
        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}


