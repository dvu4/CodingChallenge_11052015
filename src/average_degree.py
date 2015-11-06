# example of program that calculates the average degree of hashtags

import sys
import json
from datetime import datetime

from collections import Counter
import operator

#get file path from command line argument in python
input_file=open(sys.argv[1],"r+")
output_file=open(sys.argv[2],"w")


def removeNonAscii(s): 
    if s is not None:
        return "".join(filter(lambda x: ord(x)>31 & ord(x)<128 , s)) 

def extract_hashtags(s):
    return [word for word in s.split() if word[0] == "#" ]   


def time_diff(time1,time2):
    d1 = datetime.strptime(time1, "%a %b %d %H:%M:%S +0000 %Y")
    d2 = datetime.strptime(time2, "%a %b %d %H:%M:%S +0000 %Y")
    return (d2-d1).total_seconds()


data = [json.loads(line) for line in input_file]

result = []
unicode_count = 0
for line in data:
    dic = {}
    if  line.get("text") is not None:
        dic['time'] = line.get("created_at")
        
        list_hashtags = extract_hashtags(filter(None,removeNonAscii(line.get("text"))))
        
        dic1 = {}
        for hashtag in list_hashtags:
            dic1[hashtag] = len(list_hashtags) -1
        dic['content'] = dic1
    result.append(dic)
#print result
 

for i in range(len(result)):
    hashtag_node = [result[i:][idx]['content'] for idx,_ in enumerate(result[i:]) 
          if  time_diff(result[i:][0]['time'], result[i:][idx]['time']) <= 60]
       
    hashtag_graph= dict(reduce(operator.add, map(Counter, hashtag_node))) 

    
    # Calculating the rolling average degree of tweet within the 60 Second Window, 
    # The average degree = summing the degrees of all nodes in all graphs and 
    # dividing by the total number of nodes in all graphs.
    if bool(hashtag_graph):
        avg_degree = 1.0*sum(hashtag_graph.values())/len(hashtag_graph)
    else:
        avg_degree = 0
    print 'average degree is: %.2f \n' %avg_degree
    output_file.write('%.2f \n' %avg_degree)

                      
output_file.close()
