# -*- coding: utf-8 -*-
import jieba
import jieba.analyse

questions = open('./corpus/questions.txt').read().split('\n')

# for i, q in enumerate(questions):
#     print('{:2}. {}'.format(i, q))

tag_dic = {}
hash_maps = {}

for i in range(len(questions)):
    tags = jieba.analyse.extract_tags(questions[i], topK=50, withWeight=True)
    
    tag_dic = {}
    for (x, w) in tags:
        tag_dic[x] = w
    
    hash_maps[i] = tag_dic

def run_query(query):
    # query = u"想請問錄取後要如何辦赴美簽證？"

    tags = jieba.analyse.extract_tags(query, topK=50, withWeight=True)
    query_list = []
    for x, w in tags:
        # print(u'{} {}'.format(x, w))
        query_list = query_list + [(x, w)]

    minimum_index = ""
    minimum_error = float('inf')
    error_dic = {}
    for i in hash_maps:
        error = 0.0
        tags = hash_maps[i]
        for j in range(len(query_list)):
            k = query_list[j]
            if k[0] in tags:
                error += (k[1] - tags[k[0]])**2
            else:
                error += k[1]**2
        
        error_dic[i] = error
        
        if error < minimum_error:
            minimum_error = error
            minimum_index = i

    return minimum_index, error_dic
        

# print('Input : ' + query)
# print('Output: ' + questions[minimum_index])

if __name__ == '__main__':
    while True:
        usr_input = raw_input('Please enter your question:\nYou: ')
        if 'exit' in usr_input:
            break
        else:
            index, error_dic = run_query(usr_input)
            print 'Com: {}\n'.format(questions[index])
            for i in sorted(error_dic, key=error_dic.get):
                print("Error: {:.2f} -> {}".format(error_dic[i], questions[i]))
            print('\n')

