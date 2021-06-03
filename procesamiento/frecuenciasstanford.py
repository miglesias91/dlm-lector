import string
import json

from difflib import SequenceMatcher

from apertium import Translator
from nltk.stem import WordNetLemmatizer

from stanfordcorenlp import StanfordCoreNLP

class Frecuencias:
    def __init__(self, noticias, config = None):
        
        if config is None:
            # ajusto la config para usar stanforcorenlp
            self.config = {'leer':['adjetivos','sustantivos','verbos','entidades'], 'lemma':['']}
        else:
            self.config = config

        with open('conexiones.json') as c:
            j = json.load(c)
            
        servidor = j['corenlp']['servidor']
        puerto = j['corenlp']['puerto']

        self.nlp = StanfordCoreNLP(servidor, port=puerto)
        self.traductor_a_espaniol = Translator('eng', 'spa')
        self.traductor_a_ingles = Translator('spa', 'eng')

        self.lemmatizador = WordNetLemmatizer()

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

            if n.seccion not in self.noticias[sfecha][n.diario]:
                self.noticias[sfecha][n.diario][n.seccion] = []

            self.noticias[sfecha][n.diario][n.seccion].append(n)

    def calcular(self):
        notis = []
        for fecha, diarios in self.noticias.items():
            for diario, secciones in diarios.items():
                for seccion, noticias in secciones.items():
                    adj_tit, sus_tit, ver_tit, ent_tit, adj_txt, sus_txt, ver_txt, ent_txt = self.__noticias2freqs__(noticias)

                    # resultado = {'fecha': fecha, 'diario': diario, 'seccion': seccion, 'total': len(noticias), 'ter_tit':f_ter_tit, 'ver_tit': f_ver_tit, 'per_tit': f_per_tit, 'ter_txt': f_ter_txt, 'ver_txt': f_ver_txt, 'per_txt': f_per_txt }
                    resultado = {
                        'fecha': fecha, 'diario': diario, 'seccion': seccion, 'total': len(noticias),
                        'adjtit': adj_tit, 'sustit': sus_tit, 'vertit': ver_tit, 'enttit': ent_tit, 
                        'adjtxt': adj_txt, 'sustxt': sus_txt, 'vertxt': ver_txt, 'enttxt': ent_txt, 
                        }
                    self.resultados.append(resultado)

    def tokens(self, titulo, texto):
        todo = titulo.replace('.',' ') + '. ' + texto.replace('.', '. ')

        # reemplazo caracteres que dan conflicto
        todo = todo.translate(str.maketrans('','', '%'))

        anotado = json.loads(self.nlp.annotate(todo))
        
        titulo_anotado = anotado['sentences'][0]
        texto_anotado = {'entitymentions':[], 'tokens':[]}

        for oracion in anotado['sentences'][1:]:
            texto_anotado['entitymentions'].extend(oracion['entitymentions'])
            texto_anotado['tokens'].extend(oracion['tokens'])
        
        return self.contar_anotaciones(titulo_anotado), self.contar_anotaciones(texto_anotado)
        

    def contar_anotaciones(self, anotado):

        conteo = {'adjetivos':{}, 'sustantivos':{}, 'verbos':{}, 'entidades':{}}

        for t in anotado['tokens']:
            if 'adjetivos' in self.config['leer'] and t['pos'] == 'ADJ' and len(t['originalText']) > 2 and t['originalText'].lower() not in self.stopwords:
                
                lemma = t['lemma']
                if 'adjetivos' in self.config['lemma']:
                    lemma = self.lemmatizar(t['lemma'], 'a')
                # if lemma in self.adjetivos_comunes:
                #     continue

                k = lemma.lower().translate(str.maketrans('','', self.puntuacion))
                
                # filtro los numeros q no son años
                if k.isdigit() and len(k) is not 4:
                    continue

                if k in conteo['adjetivos']:
                    conteo['adjetivos'][k] += 1
                else:
                    conteo['adjetivos'][k] = 1

            if 'sustantivos' in self.config['leer'] and t['pos'] == 'NOUN' and len(t['originalText']) > 2 and t['originalText'].lower() not in self.stopwords:
                
                lemma = t['lemma']
                if 'sustantivos' in self.config['lemma']:
                    lemma = self.lemmatizar(t['lemma'], 'n')
                    if lemma in self.sustantivos_comunes:
                        continue

                k = lemma.lower().translate(str.maketrans('','', self.puntuacion))
                
                # filtro los numeros q no son años
                if k.isdigit() and len(k) is not 4:
                    continue

                if k in conteo['sustantivos']:
                    conteo['sustantivos'][k] += 1
                else:
                    conteo['sustantivos'][k] = 1

            if 'verbos' in self.config['leer'] and t['pos'] == 'VERB' and len(t['originalText']) > 2 and t['originalText'].lower() not in self.stopwords:
                
                lemma = t['lemma']
                if 'verbos' in self.config['lemma']:
                    lemma = self.lemmatizar(t['lemma'], 'v')
                    # if lemma in self.verbos_comunes:
                    #     continue

                k = lemma.lower().translate(str.maketrans('','', self.puntuacion))

                # filtro los numeros q no son años
                if k.isdigit() and len(k) is not 4:
                    continue

                if k in conteo['verbos']:
                    conteo['verbos'][k] += 1
                else:
                    conteo['verbos'][k] = 1

        if 'entidades' in self.config['leer']:
            for e in anotado['entitymentions']:
                    k = e['text'].translate(str.maketrans('','', self.puntuacion))

                    # filtro los numeros q no son años
                    if k.isdigit() and len(k) is not 4:
                        continue

                    if k in conteo['entidades']:
                        conteo['entidades'][k] += 1
                    else:
                        conteo['entidades'][k] = 1

        return conteo
        
            
    def lemmatizar(self, termino, pos):
        term = self.traductor_a_ingles.translate(termino).lower()

        if term[0] is '*':
            return termino

        if pos == 'v':
            if ' ' in term:
                lemma = 'to ' + self.lemmatizador.lemmatize(term.split(' ')[-1], pos)
            else:
                lemma = 'to ' + self.lemmatizador.lemmatize(term, pos)
        else:
            lemma = self.lemmatizador.lemmatize(term, pos)

        lemma_en_espaniol = self.traductor_a_espaniol.translate(lemma.lower()).lower()

        if lemma_en_espaniol[0] is '*':
            return termino

        if pos == 'n' and ' ' in lemma_en_espaniol:
            lemma_en_espaniol = lemma_en_espaniol.split(' ')[-1]

        if pos == 'v':
            lemma_en_espaniol = lemma_en_espaniol.split(' ')[-1]

        if SequenceMatcher(None, termino,lemma_en_espaniol).ratio() < 0.75 and pos != 'v':
            lemma_en_espaniol = termino

        return lemma_en_espaniol

    def __noticias2freqs__(self, noticias):

        freq_adjetivos_texto = {}
        freq_sustantivos_texto = {}
        freq_entidades_texto = {}
        freq_verbos_texto = {}

        freq_adjetivos_titulo = {}
        freq_sustantivos_titulo = {}
        freq_entidades_titulo = {}
        freq_verbos_titulo = {}

        for noticia in noticias:

            tokens_titulo, tokens_texto = self.tokens(noticia.titulo, noticia.texto)

            freq_adjetivos_titulo = Frecuencias.sumar_freqs(freq_adjetivos_titulo, tokens_titulo['adjetivos'], 30)
            freq_sustantivos_titulo = Frecuencias.sumar_freqs(freq_sustantivos_titulo, tokens_titulo['sustantivos'], 30)
            freq_verbos_titulo = Frecuencias.sumar_freqs(freq_verbos_titulo, tokens_titulo['verbos'], 30)
            freq_entidades_titulo = Frecuencias.sumar_freqs(freq_entidades_titulo, tokens_titulo['entidades'], 30)

            freq_adjetivos_texto = Frecuencias.sumar_freqs(freq_adjetivos_texto, tokens_texto['adjetivos'], 50)
            freq_sustantivos_texto = Frecuencias.sumar_freqs(freq_sustantivos_texto, tokens_texto['sustantivos'], 50)
            freq_verbos_texto = Frecuencias.sumar_freqs(freq_verbos_texto, tokens_texto['verbos'], 50)
            freq_entidades_texto = Frecuencias.sumar_freqs(freq_entidades_texto, tokens_texto['entidades'], 50)

        return freq_adjetivos_titulo, freq_sustantivos_titulo, freq_verbos_titulo, freq_entidades_titulo, freq_adjetivos_texto, freq_sustantivos_texto, freq_verbos_texto, freq_entidades_texto

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


