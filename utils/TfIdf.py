import re, math
from operator import itemgetter
from pprint import pprint as pp



class TfIdf:
    def get_stopwords(self):
        with open("../french_stopwords", 'r', encoding="utf-8") as file:
            stop_w = file.readlines()
            new_stop_word = []
            for prep in stop_w:
                new_stop_word.append(prep.replace("\n", ""))

        return new_stop_word
    
    def get_sentences(self, text):
        sentences = re.findall(r"[^.]+[^.]", sample)
        return sentences
    
    def remove_punctuation(self, phrase):
        new_phrase = ""
        for l in phrase:
            if l.isalpha() or l == " ":
                new_phrase += l
            else:
                new_phrase += " "
        new_phrase.replace("  ", " ")
    
        return new_phrase
    
    def get_words_docs(self, text):
        rslt = []
        text = self.remove_punctuation(text)
        stop_w = self.get_stopwords()
        for w in text.split(" "):
            if len(w) > 0:
                if w.lower() not in stop_w:
                    rslt.append(w.lower())

        return rslt

    def calculateTF(self, text):
        rslt = []
        tf_score = {}
        text = self.remove_punctuation(text)
        stop_w = self.get_stopwords()
        total_words = self.get_words_docs(text)
        total_word_len = len(total_words)
        for w in total_words:
            if w in tf_score:
                tf_score[w] += 1
            else:
                tf_score[w] = 1
        tf_score.update((x, y/int(total_word_len)) for x, y in tf_score.items())
        return tf_score
    
    def check_sentence(self, word, sentences):
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))
    
    def calcualateIdf(self, text):
        total_words = self.get_words_docs(text)
        total_sentences = self.get_sentences(text)
        idf_score = {}
        for word in total_words:
            if word in idf_score:
                idf_score[word] = self.check_sentence(word, total_sentences)
            else:
                idf_score[word] = 1

        
        # print(math.log(int(len(total_sentences))/10))
        idf_score.update((x, math.log(int(len(total_sentences))/y)) for x, y in idf_score.items())
        return idf_score
    
    def calcualateTfIdf(self, text, number_kw):
        tf_score = self.calculateTF(text)
        idf_score = self.calcualateIdf(text)
        tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}
        # print(tf_idf_score)
        return list(self.get_top_n(tf_idf_score, number_kw).keys())

    def get_top_n(self, dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result


if __name__ == "__main__":
    

    sample = "Les cas d’accaparement frauduleux en matière foncière gagnent effectivement du… terrain. Un réseau de faussaires vient d’être démantelé par le BIANCO qui a découvert un processus typique d’accaparement dans le cadre d’une investigation sur l’acquisition suspecte d’un terrain dans un District proche de la Capitale. Le réseau inclut la participation d’agents des Domaines et de la Topographie, de chefs d’arrondissement administratif, de magistrats, d’officiers publics et de promoteurs immobiliers."
    with open("sample2", 'r', encoding="utf-8") as file:
        sample = file.read()
    sentences = re.findall(r"[^.]+[^.]", sample)


    tf = TfIdf()
    # print(tf.get_stopwords())
    print(tf.calcualateTfIdf(sample, 5))
