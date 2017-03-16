class MarkovChainError(LookupError):
    '''raise this when there's a lookup error for my app'''


import random
import re
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

class SpecialChar:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name


open_token = SpecialChar("Open Token")
close_token = SpecialChar("Close Token")

class MarkovChain:
    def __init__(self):
        self.chain = {}
        self.ngram = 1

    def train(self, corpora_address, author_id):
        import xml.etree.ElementTree
        authors = xml.etree.ElementTree.parse(corpora_address).getroot()
        for author_elem in authors:
            if author_elem.attrib['id'] == author_id:
                author = author_elem
        self.name = author.attrib['name']
        self.ngram = int(author.attrib['ngram'])
        # We tokenize the corpus.
        for text in author.findall('text'):
            text = text.text
            # We replace new lines with <br> tags
            text = text.replace('\n', '<br>')
            # We add a spaces between this characters so they are treated as words
            text = re.sub(r'([,.¡!¿?;:])', r' \1 ', text)
            # We remove tildes.
            text = strip_accents(text)
            # We remove all special characters.
            text = re.sub(r"[^a-zA-Z0-9,.¡!¿?;:’'<>]", ' ', text)
            vectorized_text = [open_token] + [word.lower().strip() for word in text.split(' ') if word.strip() != ''] + [close_token]

            for ngram in zip(*[vectorized_text[i:] for i in range(self.ngram+1)]):
                self.chain.setdefault(ngram[:-1], []).append(ngram[-1])


    def generate_quote(self, max_num_words = 50, ending_char = None):
        if not self.chain:
            raise MarkovChainError('The Markov Chain has not been trained.')


        current_words = random.choice([ngram for ngram in self.chain.keys() if ngram[0] == open_token])
        print(current_words)
        sentence = [] + list(current_words[1:])

        # We generate the text.
        for _ in range(0, max_num_words):
            if current_words in self.chain:
                next_word = random.choice(self.chain[current_words])
                if next_word == close_token:
                    break
                sentence.append(next_word)
                if next_word == ending_char:
                    break
                current_words =  tuple(sentence[-(self.ngram):])
            else:
                break

        print(self.ngram)
        generated_text = ' '.join(sentence)
        for char in ['.', ',', '!', '?']:
            generated_text = generated_text.replace(' '+char, char)
        for char in ['¡', '¿']:
            generated_text = generated_text.replace(char+' ', char)
        return generated_text
