import os
import json
import re
from pathlib import Path

class Lemmatizer:
    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = Path(current_dir).parent
        KataDasarFile = parent_dir + '/data/kata-dasar.txt'
        DictionaryFile = parent_dir + '/data/lemma_dict.json'
        with open(KataDasarFile) as f:
            self.kata_dasar = set(f.read().splitlines())
        with open(DictionaryFile) as file:
            self.lemma_dict = json.load(file)
    
    def stem1(self, word):
        if word.endswith(('lah','kah','pun')):
            return word[:-3]
        else:
            return word
    
    def stem2(self, word):
        if word.startswith('ku'):
            return word[2:]
        elif word.startswith('kau'):
            return word[3:]
        else:
            return word
        
    def stem3(self, word):
        if word.endswith(('ku','mu')):
            return word[:-2]
        elif word.endswith('nya'):
            return word[:-3]
        else:
            return word
        
    def stem4(self, word):
        if word.endswith('kan'):
            return [word[:-3],word[:-2]]
        elif word.endswith('an'):
            return word[:-2]
        elif word.endswith('isasi'):
            return word[:-5]
        elif word.endswith('i'):
            return word[:-1]
        elif word.endswith('isme'):
            return word[:-4]
        else:
            return word
    
    def stem5(self, word):
        if word.startswith(('di','ke','se')):
            return word[2:]
        else:
            return word
    
    def lemmatize(self, text):
        final_result = ''
        suffix = set(['lah', 'kah', 'pun', 'ku', 'mu', 'nya'])
        text = text.lower()
        text = re.sub('[^a-zA-Z0-9-]+',' ',text)
        for word in text.split():
            result = word.lower()
            if word.isdigit() or len(word)<=3 or word in self.kata_dasar:
                result = word.lower()
            elif word in self.lemma_dict:
                result = self.lemma_dict[word]
            else:        
                word1 = self.stem1(word)
                word2 = self.stem2(word)
                word13 = self.stem3(word1)
                word134 = self.stem4(word13) 
                word25 = self.stem5(word2)
                if word1 in self.kata_dasar:
                    result = word1
                elif word1 in self.lemma_dict:
                    result = self.lemma_dict[word1]
                elif word2 in self.kata_dasar:
                    result = word2
                elif word2 in self.lemma_dict:
                    result = self.lemma_dict[word2]
                elif word13 in self.kata_dasar:
                    result = word13
                elif word13 in self.lemma_dict:
                    result = self.lemma_dict[word13]
                elif len(word134)>0:
                    if len(word134[0]) > 1:
                        for w in word134:
                            if w in self.kata_dasar:
                                result = w
                            elif w in self.lemma_dict:
                                result = self.lemma_dict[w]
                    elif word134 in self.kata_dasar:
                        result = word134
                    elif word134 in self.lemma_dict:
                        result = self.lemma_dict[word134]
                if result == word.lower():
                    if word25 in self.kata_dasar:
                        result = word25
                    elif word25 in self.lemma_dict:
                        result = self.lemma_dict[word25]
                    else:
                        word12 = self.stem2(word1)
                        word125 = self.stem1(word25)
                        if word12 in self.kata_dasar:
                            result = word12
                        elif word12 in self.lemma_dict:
                            result = self.lemma_dict[word12]
                        elif word125 in self.kata_dasar:
                            result = word125
                        elif word125 in self.lemma_dict:
                            result = self.lemma_dict[word125]
                        else:
                            word123 = self.stem3(word12)
                            word1234 = self.stem4(word123)
                            word1235 = self.stem5(word123)
                            if word123 in self.kata_dasar:
                                result = word123
                            elif word123 in self.lemma_dict:
                                result = self.lemma_dict[word123]
                            elif len(word1234)>0:
                                if len(word1234[0]) > 1:
                                    for w in word1234:
                                        if w in self.kata_dasar:
                                            result = w
                                        elif w in self.lemma_dict:
                                            result = self.lemma_dict[w]
                                elif word1234 in self.kata_dasar:
                                    result = word1234
                                elif word1234 in self.lemma_dict:
                                    result = self.lemma_dict[word1234]
                            if result == word.lower():
                                if word1235 in self.kata_dasar:
                                    result = word1235
                                elif word1235 in self.lemma_dict:
                                    result = self.lemma_dict[word1235]
                                else:
                                    word12345 = self.stem4(word1235)
                                    if len(word12345)>0:
                                        if len(word12345[0]) > 1:
                                            for w in word12345:
                                                if w in self.kata_dasar:
                                                    result = w
                                                elif w in self.lemma_dict:
                                                    result = self.lemma_dict[w]
                                        elif word12345 in self.kata_dasar:
                                            result = word12345
                                        elif word12345 in self.lemma_dict:
                                            result = self.lemma_dict[word12345]
                                    # kepada-Nya --> kepada
                                    # anggota-anggota --> anggota
                                    if result == word.lower() and '-' in word:
                                        lemma_list=[self.lemma_dict.get(i,i) for i in word.split('-')]
                                        if (len(set(lemma_list)) == 2 and word.split('-')[1] in suffix) or len(set(lemma_list)) == 1:
                                            if lemma_list[0] in self.kata_dasar:
                                                result = lemma_list[0]
            final_result+=' {}'.format(result)
        return final_result.strip()