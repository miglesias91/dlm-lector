import os
import json
import string

import spacy

class Procesador:
    def __init__(self):
        self.nlp = spacy.load('es_core_news_sm')
        
        self.stopwords = []
        with open('stopwords.txt') as s:
           self.stopwords = s.read().split('\n')

        self.sustantivos_comunes = []
        with open('sustantivos.txt') as s:
           self.sustantivos_comunes = s.read().split('\n')

    def sumar_freqs(self, medio):
        
        for categoria in medio.categorias:
            path = 'freqs/' + medio.etiqueta + '_' + categoria + '.json'

            freq_terminos_titulo, freq_verbos_titulo, freq_personas_titulo, freq_terminos_txt, freq_verbos_txt, freq_personas_txt = self.__levantar_freqs__(path)

            nuevas_f_ter_tit, nuevas_f_ver_tit, nuevas_f_per_tit, nuevas_f_ter_txt, nuevas_f_ver_txt, nuevas_f_per_txt = self.__noticias2freqs__(medio.noticias)

            freq_terminos_titulo = self.sumar_freqs(freq_terminos_titulo, nuevas_f_ter_tit, 10)
            freq_verbos_titulo = self.sumar_freqs(freq_verbos_titulo, nuevas_f_ver_tit, 5)
            freq_personas_titulo = self.sumar_freqs(freq_personas_titulo, nuevas_f_per_tit, 3)

            freq_terminos_txt = self.sumar_freqs(freq_terminos_txt, nuevas_f_ter_txt, 15)
            freq_verbos_txt = self.sumar_freqs(freq_verbos_txt, nuevas_f_ver_txt, 10)
            freq_personas_txt = self.sumar_freqs(freq_personas_txt, nuevas_f_per_txt, 5) 

            self.__serializar_freqs__(path, freq_terminos_titulo, freq_verbos_titulo, freq_personas_titulo, freqs_terminos_txt, freq_verbos_txt, freq_personas_txt)

    def __levantar_freqs__(self, p):
        if not os.path.exists(p):
            return {}, {}, {}, {}, {}, {}
        
        with open(p) as f:
            j = json.load(f)
        
        return j['fq_ter_titulo'], j['fq_ver_titulo'], j['fq_per_titulo'], j['fq_ter_txt'], j['fq_ver_txt'], j['fq_per_txt']

    def __serializar_freqs__(self, p, freq_terminos_titulo, freq_verbos_titulo, freq_personas_titulo, freq_terminos_txt, freq_verbos_txt, freq_personas_txt):
        if os.path.exists(p):
            os.remove(p)

        j = {'fq_ter_titulo': freq_terminos_titulo, 'fq_ver_titulo': freq_verbos_titulo, 'fq_per_titulo': freq_personas_titulo, 'fq_ter_txt': freq_terminos_txt, 'fq_ver_txt': freq_verbos_txt, 'fq_per_txt': freq_personas_txt}
        with open(p, 'w') as f:
            json.dump(j, f)

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

            nuevas_freq_terminos_titulo = self.freq_terminos(doc_titulo, 15)
            nuevas_freq_verbos_titulo = self.freq_verbos(doc_titulo, 10)
            nuevas_freq_personas_titulo = self.freq_personas(doc_titulo, 5)

            nuevas_freq_terminos_texto = self.freq_terminos(doc_texto, 15)
            nuevas_freq_verbos_texto = self.freq_verbos(doc_texto, 10)
            nuevas_freq_personas_texto = self.freq_personas(doc_texto, 5)

            freq_terminos_titulo = self.sumar_freqs(freq_terminos_titulo, nuevas_freq_terminos_titulo, 15)
            freq_verbos_titulo = self.sumar_freqs(freq_verbos_titulo, nuevas_freq_verbos_titulo, 10)
            freq_personas_titulo = self.sumar_freqs(freq_personas_titulo, nuevas_freq_personas_titulo, 5)

            freq_terminos_texto = self.sumar_freqs(freq_terminos_texto, nuevas_freq_terminos_texto, 15)
            freq_verbos_texto = self.sumar_freqs(freq_verbos_texto, nuevas_freq_verbos_texto, 10)
            freq_personas_texto = self.sumar_freqs(freq_personas_texto, nuevas_freq_personas_texto, 5)

        return freq_terminos_titulo, freq_verbos_titulo, freq_personas_titulo, freq_terminos_texto, freq_verbos_texto, freq_personas_texto

    def freq_terminos(self, doc, top):
        freqs = {}
        for p in doc:
            if p.pos_ == 'NOUN' and len(p.text) > 2 and p.lemma_.lower() not in self.sustantivos_comunes and not p.is_digit and p.text not in self.stopwords:
                k = p.text.lower()
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def freq_verbos(self, doc, top):
        freqs = {}
        for p in doc:
            if p.pos_ == 'VERB':
                k = p.lemma_.lower()
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def freq_personas(self, doc, top):
        freqs = {}
        for e in doc.ents:
            if e.label_ == 'PER':
                k = e.text.lower()
                if k in freqs:
                    freqs[k] += 1
                else:
                    freqs[k] = 1

        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}

    def sumar_freqs(self, freqs, freqs_nuevas, top):
        for k, v in freqs_nuevas.items():
            if k in freqs:
                freqs[k] += v
            else:
                freqs[k] = v
        return {k: v for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)[:top]}