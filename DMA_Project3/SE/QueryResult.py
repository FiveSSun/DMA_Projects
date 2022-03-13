from whoosh.analysis.filters import STOP_WORDS
import whoosh.index as index
from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring, query
import CustomScoring as scoring
from nltk.corpus import stopwords, wordnet
from whoosh.query import Variations

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

def getSearchEngineResult(query_dict):
    result_dict = {}
    ix = index.open_dir("index")

    # Choose scoring Function
    with ix.searcher(weighting=scoring.BM25F(B=0.75, K1=2.0)) as searcher:
    #with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:

        # TODO - Define your own query parser
        parser = QueryParser("contents", schema=ix.schema, group=OrGroup)
        # parser = QueryParser("contents", schema=ix.schema, group=OrGroup, termclass=Variations)
        stopWords = set(stopwords.words('english'))

        for qid, q in query_dict.items():
            
            q=q.replace(")", "^1.2") # best value : 1.2
            q=q.replace("?", " ")
            q=q.replace(",", " ")
            q=q.replace(".", " ")

            # q=q.replace("(", "")
            # q=q.replace("^", "") # useless
            # q=q.replace("/", "") # useless
            # q=q.replace("-", "^1.15-") # decrease score

            new_q = ''
            #####################################################################
            for word in q.split(' '):
                # Remove stopWords
                if word.lower() not in stopWords:
                    if word!="":
                        A=pos_tag([word])
                        B=A[0]    

                        # # Stemmize or Lemmatize                                         
                        # if get_wordnet_pos(B[1])==None:
                        #     word=Lstem.stem(B[0])
                        # else:
                        #     word=lemma.lemmatize(B[0],get_wordnet_pos(B[1]))

                        # # Give Weight To Word 
                        # # No Effect : CD DT NNP NNPS
                        if B[1]=="MD":
                            word="" # best value : 0.0
                            # continue   
                        elif B[1]=="NN" or B[1]=="NNS":
                            word=word+"^1.08" # best value : 1.08
                        elif B[1]=="JJ" or B[1]=="JJR" or B[1]=="JJS":
                            word=word # best value : 1
                        elif B[1]=="RB" or B[1]=="RBR" or B[1]=="RBS":
                            word=word+"^0.78" # best value : 0.78                           
                        elif B[1]=="VB" or B[1]=="VBD" or B[1]=="VBG"or B[1]=="VBP" or B[1]=="VBZ":
                            word=word # best value : 1
                        else:
                            word=word+"^0.76" # best value : 0.76

                    # Paste word
                    new_q += word + ' '
            
            # Erase Last Weight (Error)
            new_q=new_q[:-6]
            new_q=new_q.lower()
            #####################################################################            
            query = parser.parse(new_q)
            #TODO
            correct = searcher.correct_query(query,new_q)

            results = searcher.search(correct.query, limit=None)
            result_dict[qid] = [result.fields()['docID'] for result in results]        
            #if qid==225-7: print(correct.query)
    return result_dict