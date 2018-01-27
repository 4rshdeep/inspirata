import markovify
import nltk
import re
import json
import os

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

with open('encouraging.txt') as f:
    text = f.read()
    text_model = POSifiedText(text, state_size=3)

model_json = text_model.to_json()

with open('model.json', 'w') as f:
    json.dump(model_json, f, ensure_ascii=False)