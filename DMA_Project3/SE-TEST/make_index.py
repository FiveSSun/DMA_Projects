import os.path
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC,NGRAMWORDS
from whoosh import analysis
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
from nltk import word_tokenize
from whoosh.lang.porter import stem
from nltk.stem import PorterStemmer
from nltk.tag import pos_tag
import re
from whoosh.analysis import *

#schema = Schema(docID=NUMERIC(stored=True), contents=TEXT)
schema = Schema(docID=NUMERIC(stored=True), contents=TEXT(analyzer=StemmingAnalyzer(stoplist=STOP_WORDS)))
index_dir = "index"

# Make index folder at directory
if not os.path.exists(index_dir):
    os.makedirs(index_dir)

ix = create_in(index_dir, schema)

# Edit schema
writer = ix.writer()
ngs=analysis.SpaceSeparatedTokenizer()

st=PorterStemmer() 
retokenize=RegexpTokenizer("[\s]+",gaps=True)

def extract_ngrams(data, num):
    n_grams = ngrams(word_tokenize(data), num)
    return [ ''.join(grams) for grams in n_grams]

st = PorterStemmer()

with open('doc/document.txt', 'r') as f:
    text = f.read()
    docs = text.split('   /\n')[:-1]
    for doc in docs:
        br = doc.find('\n')
        docID = int(doc[:br])
        doc_text = doc[br+1:]
        ## stemming ##

        # wordList = re.sub("[^\w]", " ",  doc_text).split()
        # new_docs=''

        # for word in wordList:
        #     new_docs+=word+' '
        #     #new_docs+=st.stem(word)+' '
        # # new_docs=re.sub('[-=,#/?:$}]','',new_docs)
        # # temp=ngs(doc_text)
        # # new_docs=""
        # # for token in temp:
        # #     print(type(token.text))
        # #     new_docs+=stem(token.text)+" "
        # doc_text=new_docs
        # if docID==1: print(doc_text)

        ##############

        # If you want, you can process doc_text here
        # tokens=extract_ngrams(doc_text,1)
        # tokens+=extract_ngrams(doc_text,2)
        # tokens+=extract_ngrams(doc_text,3)
        # tokens+=extract_ngrams(doc_text,4)
        # new_doc=""
        # for token in tokens: 
        #     new_doc+=token+" "
        # doc_text=new_doc
        # if docID==1: print(new_doc)
        

        # ngt=analysis.NgramTokenizer(minsize=2,maxsize=10)       
                   
        # tokens=ngt(doc_text)
        # new_q=""
        # for token in tokens: 
        #     new_q+=token.text+" "
        
        # doc_text=new_q
        writer.add_document(docID=docID, contents=doc_text)

# Store updated schema
writer.commit()