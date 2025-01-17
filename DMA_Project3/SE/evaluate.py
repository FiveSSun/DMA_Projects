import numpy as np
from QueryResult import getSearchEngineResult


def readQueryFile(filename):
    query_dict = {}

    with open(filename, 'r') as f:
        text = f.read()
        queries = text.split('   /\n')

        for query in queries:
            br = query.find('\n')
            qID = int(query[:br])
            q = query[br+1:]
            query_dict[qID] = q

    return query_dict


def getGroundtruthRelevance(query_ids):
    relevant_dict = {}

    with open('doc/relevance.txt', 'r') as f:
        lines = f.readlines()

        for line in lines:
            items = line.split(' ')
            queryID = int(items[0])
            docID = int(items[1])
            if queryID in query_ids:
                # add into relevant_dict
                if queryID in relevant_dict:
                    relevant_dict[queryID].append(docID)
                else:
                    relevant_dict[queryID] = [docID]

    return relevant_dict


def evaluate(query_dict, relevent_dict, results_dict):
    BPREF = []

    for queryID in query_dict.keys():
        relevantCount = 0
        nonRelevantCount = 0
        score = 0
        results = results_dict[queryID]
        relevantDocuments = relevent_dict[queryID]
        relDocCount = len(relevantDocuments)

        for document in results:
            if document in relevantDocuments:
                relevantCount += 1
                if nonRelevantCount >= relDocCount:
                    score += 0
                else:
                    score += (1 - nonRelevantCount / relDocCount)
            else:
                nonRelevantCount += 1
            if relevantCount == relDocCount:
                break
        score = score / relDocCount
        BPREF.append(score)

    print(np.mean(BPREF))

    #print(BPREF)

if __name__ == '__main__':
    query_dict = readQueryFile('doc/query.txt')
    relevant_dict = getGroundtruthRelevance(query_dict.keys())
    results_dict = getSearchEngineResult(query_dict)
    evaluate(query_dict, relevant_dict, results_dict)