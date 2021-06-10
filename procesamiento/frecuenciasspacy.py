import string

import spacy

class Frecuencias:
    def __init__(self, noticias=[]):
        self.init_nlp()

        self.noticias = {}
        self.resultados = []

        for n in noticias:
            sfecha = n.fecha.strftime('%Y%m%d')
            if sfecha not in self.noticias:
                self.noticias[sfecha] = {}

            if n.diario not in self.noticias[sfecha]:
                self.noticias[sfecha][n.diario] = {}

            if n.seccion not in self.noticias[sfecha][n.diario]:
                self.noticias[sfecha][n.diario][n.seccion] = []

            self.noticias[sfecha][n.diario][n.seccion].append(n)
    
    def init_nlp(self):
        self.nlp = spacy.load('es_core_news_sm')
        
        self.stopwords = []
        with open('stopwords.txt') as s:
           self.stopwords = s.read().split('\n')

        self.sustantivos_comunes = []
        with open('sustantivos.txt') as s:
           self.sustantivos_comunes = s.read().split('\n')

        self.puntuacion = string.punctuation + "¡¿\n"

    def calcular(self):
        notis = []
        for fecha, diarios in self.noticias.items():
            for diario, secciones in diarios.items():
                for seccion, noticias in secciones.items():
                    adjtit, sustit, vertit, enttit, adjtxt, sustxt, vertxt, enttxt = self.__noticias2freqs__(noticias)

                    resultado = {'fecha': fecha, 'diario': diario, 'seccion': seccion, 'total': len(noticias),
                    'adjtit': adjtit, 'sustit': sustit, 'vertit': vertit, 'enttit': enttit,
                    'adjtxt': adjtxt, 'sustxt': sustxt, 'vertxt': vertxt, 'enttxt': enttxt }
                    self.resultados.append(resultado)

    def tituloytexto2freqs(self, titulo, texto):

        doc_titulo = self.nlp(titulo)
        doc_texto = self.nlp(texto)

        adjtit = self.freq_adjetivos(doc_titulo, 50)
        sustit = self.freq_sustantivos(doc_titulo, 30)
        vertit = self.freq_verbos(doc_titulo, 15)
        enttit = self.freq_entidades(doc_titulo, 15)

        adjtxt = self.freq_adjetivos(doc_texto, 50)
        sustxt = self.freq_sustantivos(doc_texto, 50)
        vertxt = self.freq_verbos(doc_texto, 15)
        enttxt = self.freq_entidades(doc_texto, 15)

        return adjtit, sustit, vertit, enttit, adjtxt, sustxt, vertxt, enttxt

    def __noticias2freqs__(self, noticias):

        freq_adjetivos_texto = {}
        freq_sustantivos_texto = {}
        freq_verbos_texto = {}
        freq_entidades_texto = {}

        freq_adjetivos_titulo = {}
        freq_sustantivos_titulo = {}
        freq_verbos_titulo = {}
        freq_entidades_titulo = {}

        for noticia in noticias:

            doc_texto = self.nlp(noticia.texto)
            doc_titulo = self.nlp(noticia.titulo)

            nuevas_freq_adjetivos_titulo = self.freq_adjetivos(doc_titulo, 30)
            nuevas_freq_sustantivos_titulo = self.freq_sustantivos(doc_titulo, 30)
            nuevas_freq_verbos_titulo = self.freq_verbos(doc_titulo, 15)
            nuevas_freq_entidades_titulo = self.freq_entidades(doc_titulo, 15)

            nuevas_freq_adjetivos_texto = self.freq_adjetivos(doc_texto, 50)
            nuevas_freq_sustantivos_texto = self.freq_sustantivos(doc_texto, 50)
            nuevas_freq_verbos_texto = self.freq_verbos(doc_texto, 15)
            nuevas_freq_entidades_texto = self.freq_entidades(doc_texto, 15)

            freq_adjetivos_titulo = Frecuencias.sumar_freqs(freq_adjetivos_titulo, nuevas_freq_adjetivos_titulo, 30)
            freq_sustantivos_titulo = Frecuencias.sumar_freqs(freq_sustantivos_titulo, nuevas_freq_sustantivos_titulo, 30)
            freq_verbos_titulo = Frecuencias.sumar_freqs(freq_verbos_titulo, nuevas_freq_verbos_titulo, 15)
            freq_entidades_titulo = Frecuencias.sumar_freqs(freq_entidades_titulo, nuevas_freq_entidades_titulo, 15)

            freq_adjetivos_texto = Frecuencias.sumar_freqs(freq_adjetivos_texto, nuevas_freq_adjetivos_texto, 50)
            freq_sustantivos_texto = Frecuencias.sumar_freqs(freq_sustantivos_texto, nuevas_freq_sustantivos_texto, 50)
            freq_verbos_texto = Frecuencias.sumar_freqs(freq_verbos_texto, nuevas_freq_verbos_texto, 15)
            freq_entidades_texto = Frecuencias.sumar_freqs(freq_entidades_texto, nuevas_freq_entidades_texto, 15)

        return freq_adjetivos_titulo, freq_sustantivos_titulo, freq_verbos_titulo, freq_entidades_titulo, freq_adjetivos_texto, freq_sustantivos_texto, freq_verbos_texto, freq_entidades_texto

    def freq_adjetivos(self, doc, top):
        freqs = {}
        for p in doc:
            if p.pos_ == 'ADJ' and len(p.text) > 2 and not p.is_digit and p.text not in self.stopwords:
                k = p.text.lower().translate(str.maketrans('','', self.puntuacion))
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def freq_sustantivos(self, doc, top):
        freqs = {}
        for p in doc:
            if p.pos_ == 'NOUN' and len(p.text) > 2 and p.lemma_.lower() not in self.sustantivos_comunes and not p.is_digit and p.text not in self.stopwords:
                k = p.text.lower().translate(str.maketrans('','', self.puntuacion))
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def freq_verbos(self, doc, top):
        freqs = {}
        for p in doc:
            if p.pos_ == 'VERB':
                k = p.lemma_.lower().translate(str.maketrans('','', self.puntuacion))
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def freq_entidades(self, doc, top):
        freqs = {}
        for e in doc.ents:
            if e.label_ == 'PER':
                k = e.text.translate(str.maketrans('','', self.puntuacion))
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    @staticmethod
    def sumar_freqs(freqs, freqs_nuevas, top):
        for k, v in freqs_nuevas.items():
            if k in freqs:
                freqs[k] += v
            else:
                freqs[k] = v
        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    @staticmethod
    def top(freqs, top):
        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}


