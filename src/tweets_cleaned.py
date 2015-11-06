# program that calculates the number of tweets cleaned

import sys
import json
import string

#get file path from command line argument in python
input_file = open(sys.argv[1],"r+")
output_file = open(sys.argv[2],"w")


def removeNonAscii(s): 
    if s is not None:
        return "".join(filter(lambda x: ord(x)<128, s)) 

data= []
for line in input_file:
    data.append(json.loads(line))


result = []
unicode_count = 0

for line in data:
    dic = {}
    if  line.get("text") is not None:
        dic['time'] = line.get("created_at")

        # remove non-unicode, replace the escape,newline and tab characters by space
        dic['content'] = filter(None,removeNonAscii(line.get("text")))
        dic['content'] =  str(dic['content']).translate(string.maketrans("\n\t\r", "   "))
        
        if len(line.get("text")) > len(removeNonAscii(line.get("text"))):
            unicode_count +=1
        result.append(dic)

#print unicode_count ,"tweets contained unicode."


# extracting the information of text" field and  "created_at" field, 
# then output this tweet with the format of 
# <contents of "text" field> (timestamp: <contents of "created_at" field>)

[output_file.write('{0} (timestamp: {1})\n'.format(dic['content'], dic['time'])) for dic in result]
output_file.write('\n{0} tweets contained unicode.'.format(unicode_count)) 

output_file.close()
