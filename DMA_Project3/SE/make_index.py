import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC,NGRAMWORDS, NGRAM
from whoosh.analysis import *

from nltk.corpus import stopwords, wordnet
from nltk.util import ngrams
from nltk import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer

# Stemmizer & Lemmatizer
Pstem=PorterStemmer()
Lstem=LancasterStemmer()
lemma=WordNetLemmatizer()

# Ngram ftn
def extract_ngrams(data, num):
    n_grams = ngrams(word_tokenize(data), num)
    return [''.join(grams) for grams in n_grams]

# Classify the type of words
def get_wordnet_pos(treebank_tag):  
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


# Set up Schema [ docID - Numeric/ doctext- TEXT { option : stem (stoplist), Ngram (size) } ]
stopWords = set(stopwords.words('english'))

# schema = Schema(docID=NUMERIC(stored=True), contents=TEXT)
#schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=NgramTokenizer(4)))
#schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=StemmingAnalyzer(stoplist=STOP_WORDS), spelling=True))
schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=StemmingAnalyzer(stoplist=STOP_WORDS)))
# schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=StemmingAnalyzer(stoplist=STOP_WORDS)|NgramFilter(minsize=1,maxsize=18)))
# schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=StemmingAnalyzer(stoplist=STOP_WORDS)|NgramFilter(minsize=1,maxsize=18,at='start')))
# schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=StemmingAnalyzer(stoplist=STOP_WORDS)|NgramFilter(minsize=1,maxsize=18,at='end')))

index_dir = "index"

if not os.path.exists(index_dir):
    os.makedirs(index_dir)

ix = create_in(index_dir, schema)

writer = ix.writer()
 
with open('doc/document.txt', 'r') as f:
    text = f.read()
    docs = text.split('   /\n')[:-1]

    stopWords = set(stopwords.words('english')) ## insertion part (can remove)
    for doc in docs:
        br = doc.find('\n')
        docID = int(doc[:br])
        doc_text = doc[br+1:]
        ##########################################################
        # # Change special character  to whitespace
        # doc_text=doc_text.replace("\n"," ") # useless
        doc_text=doc_text.replace(".", " ") # useless
        #doc_text=doc_text.replace("?", "") # useless
        # doc_text=doc_text.replace(",", "") # useless
        # doc_text=doc_text.replace(".", "") # decrease
        # doc_text=doc_text.replace("-", " - ") # decrease

        # Document Processing 
        # new_q = ''
        # for word in doc_text.split(' '):
        #     # Remove stopWords
        #     if word.lower() not in stopWords and word.lower() !=' ':
        #         # Stemmize or Lemmatize  
        #         try:
        #             A=pos_tag([word])
        #             B=A[0]
        #             # if B[1]=="MD":continue
        #             #print(word)

        #             if get_wordnet_pos(B[1])==None:
        #                 word=Lstem.stem(B[0])
        #             else:
        #                 word=lemma.lemmatize(B[0],get_wordnet_pos(B[1]))
        #         # Fail to classify the type of words                           
        #         except IndexError:
        #             continue
        #         new_q += word + ' '

        
        
        # doc_text=new_q
        ##########################################################
        writer.add_document(docID=docID, contents=doc_text)

        # Check list
        # if docID ==1:
        #     print(doc_text)
        # if docID ==1:
        #     break

writer.commit()