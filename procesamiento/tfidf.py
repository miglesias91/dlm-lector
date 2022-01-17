from nltk import word_tokenize, bigrams
from math import log

class tfidf:
    def __init__(self, docs):
        self.docs = docs
        self.dfs = {}
        self.tfidfs = {}

        self.stopwords = []
        with open('stopwords.txt') as s:
           self.stopwords = s.read().split('\n')

        self.sustantivos_comunes = []
        with open('sustantivos.txt') as s:
           self.sustantivos_comunes = s.read().split('\n')

        self.verbos_comunes = []
        with open('verbos.txt') as s:
           self.verbos_comunes = s.read().split('\n')

        import string

        self.puntuacion = string.punctuation + "¡¿\n"

    def calcular(self):

        i_doc = 0
        for doc in self.docs:
            bow = self.prepro(doc)

            self.tf_doc(bow, i_doc)
            self.df_doc(bow)

            i_doc += 1

        self.calcular_tfidfs()
        BORRAR = 0

    def tf_doc(self, bow, i_doc):

        conteo = self.conteo(bow)

        n = len(bow)
        for w in bow:
            if w not in self.tfidfs:
                self.tfidfs[w] = [0] * len(self.docs)

            self.tfidfs[w][i_doc] = conteo[w] / n
            
    def df_doc(self, bow):

        ubow = list(set(bow))

        for w in ubow:
            if w not in self.dfs:
                self.dfs[w] = 0

            self.dfs[w] += 1

    def calcular_tfidfs(self):

        n = len(self.docs)
        for w, df in self.dfs.items():
            # CHEQUEAR ESTE FOR Y VER Q ONDA EL USO DE LA MEMORIA
            for i in range(len(self.tfidfs[w])):
                self.tfidfs[w][i] *= log(n / df)
        BORRAR = 0

    def prepro(self, doc):

        bow = []
        doc = doc.lower().translate(str.maketrans('', '', self.puntuacion))
        terminos = word_tokenize(doc)
        
        terminos = [t.strip() for t in terminos if t.translate(str.maketrans('áéíóúý', 'aeiouy')) not in self.sustantivos_comunes and t.translate(str.maketrans('áéíóúý', 'aeiouy')) not in self.stopwords]
        bigramas = ["_".join(list(bigrama)) for bigrama in list(bigrams(terminos))]

        tokens = terminos + bigramas
        for token in tokens:

            if len(token) < 5 or len(token) > 20:
                continue

            if token.isdigit() and len(token) != 4:
                continue

            token_sin_tildes = token.translate(str.maketrans('áéíóúý', 'aeiouy'))
            if token_sin_tildes in self.sustantivos_comunes or token_sin_tildes in self.stopwords:
                continue

            bow.append(token)
        
        return bow

    def conteo(self, bow):
        mapa = {}

        for w in bow:
            if w not in mapa:
                mapa[w] = 0

            mapa[w] += 1

        return mapa
