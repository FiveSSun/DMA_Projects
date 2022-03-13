from whoosh.analysis.filters import LowercaseFilter
from whoosh.analysis.ngrams import NgramFilter, NgramTokenizer
from whoosh.analysis.tokenizers import Tokenizer
import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring, analysis, fields
from whoosh.qparser.plugins import RangePlugin, RegexPlugin, SingleQuotePlugin, WhitespacePlugin
import CustomScoring as scoring
import whoosh
import re
import nltk
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
from whoosh.lang.porter import stem
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer

lemma=WordNetLemmatizer()
from nltk.tag import pos_tag
from nltk import word_tokenize
a=['A', 'class', 'is', 'a', 'blueprint', 'for', 'the', 'object']

b=['A class', 'class is', 'is a', 'a blueprint', 'blueprint for', 'for the', 'the object']
c=a+b
print(c)
a.append('K')
print(a)
a.extend(b)
#print(a[1:1])


a='hello'
b=pos_tag([a])
c=b[0]
print(b)
print(c)
print(c[1])
print(lemma.lemmatize('was','v'))