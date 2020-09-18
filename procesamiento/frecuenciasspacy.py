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

            if n.categoria not in self.noticias[sfecha][n.diario]:
                self.noticias[sfecha][n.diario][n.categoria] = []

            self.noticias[sfecha][n.diario][n.categoria].append(n)
    
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
            for diario, categorias in diarios.items():
                for categoria, noticias in categorias.items():
                    f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt = self.__noticias2freqs__(noticias)

                    resultado = {'fecha': fecha, 'diario': diario, 'categoria': categoria, 'total': len(noticias), 'ter_tit':f_ter_tit, 'ver_tit': f_ver_tit, 'per_tit': f_per_tit, 'ter_txt': f_ter_txt, 'ver_txt': f_ver_txt, 'per_txt': f_per_txt }
                    self.resultados.append(resultado)

    def tituloytexto2freqs(self, titulo, texto):

        doc_titulo = self.nlp(titulo)
        doc_texto = self.nlp(texto)

        f_ter_tit = self.freq_terminos(doc_titulo, 30)
        f_ver_tit = self.freq_verbos(doc_titulo, 15)
        f_per_tit = self.freq_personas(doc_titulo, 15)

        f_ter_txt = self.freq_terminos(doc_texto, 50)
        f_ver_txt = self.freq_verbos(doc_texto, 15)
        f_per_txt = self.freq_personas(doc_texto, 15)

        return f_ter_tit, f_ver_tit, f_per_tit, f_ter_txt, f_ver_txt, f_per_txt

    def __noticias2freqs__(self, noticias):

        freq_terminos_texto = {}
        freq_personas_texto = {}
        freq_verbos_texto = {}

        freq_terminos_titulo = {}
        freq_personas_titulo = {}
        freq_verbos_titulo = {}

        for noticia in noticias:

            doc_texto = self.nlp(noticia.texto)
            doc_titulo = self.nlp(noticia.titulo)

            nuevas_freq_terminos_titulo = self.freq_terminos(doc_titulo, 30)
            nuevas_freq_verbos_titulo = self.freq_verbos(doc_titulo, 15)
            nuevas_freq_personas_titulo = self.freq_personas(doc_titulo, 15)

            nuevas_freq_terminos_texto = self.freq_terminos(doc_texto, 50)
            nuevas_freq_verbos_texto = self.freq_verbos(doc_texto, 15)
            nuevas_freq_personas_texto = self.freq_personas(doc_texto, 15)

            freq_terminos_titulo = Frecuencias.sumar_freqs(freq_terminos_titulo, nuevas_freq_terminos_titulo, 30)
            freq_verbos_titulo = Frecuencias.sumar_freqs(freq_verbos_titulo, nuevas_freq_verbos_titulo, 15)
            freq_personas_titulo = Frecuencias.sumar_freqs(freq_personas_titulo, nuevas_freq_personas_titulo, 15)

            freq_terminos_texto = Frecuencias.sumar_freqs(freq_terminos_texto, nuevas_freq_terminos_texto, 50)
            freq_verbos_texto = Frecuencias.sumar_freqs(freq_verbos_texto, nuevas_freq_verbos_texto, 15)
            freq_personas_texto = Frecuencias.sumar_freqs(freq_personas_texto, nuevas_freq_personas_texto, 15)

        return freq_terminos_titulo, freq_verbos_titulo, freq_personas_titulo, freq_terminos_texto, freq_verbos_texto, freq_personas_texto

    def freq_terminos(self, doc, top):
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

    def freq_personas(self, doc, top):
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


