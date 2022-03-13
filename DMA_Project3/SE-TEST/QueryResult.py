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

from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.util import ngrams
from whoosh.lang.porter import stem

from nltk import word_tokenize

def extract_ngrams(data, num):
    n_grams = ngrams(word_tokenize(data), num)
    return [''.join(grams) for grams in n_grams]



def getSearchEngineResult(query_dict):
    result_dict = {}
    ix = index.open_dir("index")

    with ix.searcher(weighting=scoring.BM25F()) as searcher:
    # with ix.searcher(weighting=scoring.ScoringFunction()) as searcher:

        # TODO - Define your own query parser 
         
        # parser = QueryParser("contents", schema=ix.schema,plugins=RangePlugin(expr=None,excl_start="'",excl_end="'"), group=OrGroup)
        parser = QueryParser("contents", schema=ix.schema,group=OrGroup)
        

        stopWords = set(stopwords.words('english'))
        
        ngs=analysis.SpaceSeparatedTokenizer()
        ngt = analysis.NgramTokenizer(minsize=5,maxsize=8)
        st=PorterStemmer()
        
        for qid, q in query_dict.items():
            q=q.replace(")", "^1.2") # best value : 1.2
            q=q.replace("?", " ")
            q=q.replace(",", " ")
            q=q.replace(".", " ")
            #q=q.replace("(", "")         

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
           
            # rext=analysis.StemmingAnalyzer()
            # tokens0=rext(new_q)
            # new_q=""
            # for token in tokens0:
            #     new_q+=token.text+" "
            
            # temp_q=q.split(' ')
            # n=len(temp_q)
            # list=[]
            # for i in range(n):
            #     if temp_q[i].lower() in stopWords: list.append(i)

            # private_tokens=[]
            # m=len(list)
            # for i in range(m-1):
            #     if list[i]+1 !=list[i+1]:private_tokens.append(temp_q[list[i]+1:list[i+1]])
            # if list[m-1]!=n:private_tokens.append(temp_q[list[m-1]+1:])   
            # n2=len(private_tokens) 
            # private_tokens_result=[]    
            # for i in range(n2):
            #     temp=''
            #     for txt in private_tokens[i]:
            #         temp+=txt
            #     temp+='^1.2'
            #     private_tokens_result.append(temp)
            # for i in [0,-1]:
            #     temp=''
            #     for txt in private_tokens[i]:
            #         temp+=txt
            #     temp+='^1.2'
            #     private_tokens_result.append(temp)    

            

            # if qid<=2: 
            #     print(private_tokens,new_q , n2)
            #     print(private_tokens_result)

            # Change to lower words
            new_q=new_q.lower()
            # new_q=re.sub('[-=,#/?:$}]','',new_q)
            # ngram Tokenize (2~4) by using NLTK

            # tokens1=extract_ngrams(new_q,1) ## 살려야 될것  
            # tokens2=extract_ngrams(new_q,2) ## 살려야 될것
            # if qid==1:
            #     print(pos_tag(tokens1))

            # noun_list=[t[0] for t in pos_tag(tokens1) if t[1] =='NN' or t[1]=='NNS']
            # inoun_list=[t[0] for t in pos_tag(tokens1) if t[1] =='IN']
            # md_list=[t[0] for t in pos_tag(tokens1) if t[1] =='MD']
            # jj_list=[t[0] for t in pos_tag(tokens1) if t[1] =='JJ']
            # vb_list=[t[0] for t in pos_tag(tokens1) if t[1] =='VB']
            
            # n3=len(tokens1)
            # if qid==1:
            #     print(pos_tag(tokens1))
            #     print(inoun_list)

            # # query stemming vs
            # for i in range(n3):
            #     if tokens1[i] in noun_list: 
            #         if i <5:          
            #             tokens1[i]+='^1.04'
            #     elif tokens1[i] in inoun_list:                    
            #         tokens1[i]+='^0.8' #0.8
            #     elif tokens1[i] in md_list:
            #         tokens1[i]+='^0.89'   #
            #     elif tokens1[i] in jj_list:
            #         tokens1[i]+='^1'    
            #     elif tokens1[i] in vb_list:
            #         tokens1[i]+='^0.98'

            # for i in range(n3):
            #     if tokens1[i] in noun_list: 
            #         if i <5:          
            #             tokens1[i]+='^1.0'
            #     elif tokens1[i] in inoun_list:                    
            #         tokens1[i]+='^1.' #0.8
            #     elif tokens1[i] in md_list:
            #         tokens1[i]=''   #
            #     elif tokens1[i] in jj_list:
            #         tokens1[i]+='^1'    
            #     elif tokens1[i] in vb_list:
            #         tokens1[i]+='^1'
                # else:
                #     tokens1[i]+='^0.5'


            


            # tokens2[0]=tokens2[0]+'^2'
            # if qid==1:print(len(tokens2))
            # n=len(tokens2)
            # for i in range(1,n):
            #     if i%4==0:         
            #         tokens2[i]=tokens2[i]+'^1.1'
            # print(tokens)
              
            tokens =extract_ngrams(new_q,1)            
            tokens+=extract_ngrams(new_q,2)
            tokens+=extract_ngrams(new_q,3)
            tokens+=extract_ngrams(new_q,4)
            tokens+=extract_ngrams(new_q,5)
            tokens+=extract_ngrams(new_q,6)
            tokens+=extract_ngrams(new_q,7)
            tokens+=extract_ngrams(new_q,8)

            #tokens=tokens1+tokens2 #+private_tokens_result
            
            # # ngram Tokenize by using Whoosh 
            # # 2gram Tokenize 
            # tokens1=[]
            # temptokens=ngs(new_q)
            # pretoken=""
            # for token in temptokens:
            #     txt=st.stem(token.text)
            #     # text=pretoken+" "+txt
            #     text=pretoken+txt
            #     pretoken=txt
            #     tokens1.append(text)
            # # 3gram Tokenize 
            # tokens2=[]
            # prepretoken=""
            # pretoken=""
            # temptokens=ngs(new_q)
            # for token in temptokens:
            #     txt=st.stem(token.text)
            #     # text=prepretoken+" "+pretoken+" "+txt
            #     text=prepretoken+pretoken+txt
            #     prepretoken=pretoken
            #     pretoken=txt
                
            #     tokens2.append(text)
            # # mergeing
            # tokens=tokens1+tokens2
#####################################################
            # ngram Tokenizing by using alphabet
            # tokens_ngt=ngt(new_q)
    
            # new_q1=""
            # for token in tokens_ngt: 
            #     new_q1+=token.text+" "
#####################################################            
            new_q=' '
            
            for token in tokens: 
                new_q+=token+" "
#####################################################

            
            # query = parser.parse(new_q.lower())
            # print(new_q)
            #parser.remove_plugin(WhitespacePlugin)
            query =parser.parse(new_q)
            #query = QueryParser("tag",ix.schema).parse(tokens)
            # parser.add_plugin(RangePlugin(expr=None,excl_start="/",excl_end="/"))
            # parser.add_plugin(RegexPlugin())
            # for token in tokens:
            #     query = parser.parse(token)
            
            results = searcher.search(query, limit=None)
            result_dict[qid] = [result.fields()['docID'] for result in results]
        
        # stopWords = set(stopwords.words('english'))

        # for qid, q in query_dict.items():
        #     new_q = ''
            
        #     for word in q.split(' '):
        #         if word.lower() not in stopWords:
        #             new_q += word + ' '

        #     query = parser.parse(new_q.lower())
        #     results = searcher.search(query, limit=None)
        #     result_dict[qid] = [result.fields()['docID'] for result in results]
        
        ngt=analysis.NgramTokenizer(minsize=2,maxsize=6)
        
        # for qid, q in query_dict.items():
            
        #     tokens=ngt(q)
        #     new_q=""
        #     for token in tokens: 
        #         new_q+=token.text+" "

        #     query = parser.parse(new_q.lower())
        #     results = searcher.search(query, limit=None)
        #     result_dict[qid] = [result.fields()['docID'] for result in results]
        

    return result_dict