class MarkovChainError(LookupError):
    '''raise this when there's a lookup error for my app'''


import random
import re
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

class SpecialChar:
    pass


open_token = SpecialChar()
close_token = SpecialChar()

class MarkovChain:
    def __init__(self):
        self.chain = {}

    def train(self, corpora_address, author_id):
        import xml.etree.ElementTree
        authors = xml.etree.ElementTree.parse(corpora_address).getroot()
        for author_elem in authors:
            if author_elem.attrib['id'] == author_id:
                author = author_elem
        self.name = author.attrib['name']

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
            text = re.sub(r"[^a-zA-Z0-9,.!?;:’'<>]", ' ', text)
            vectorized_text = [open_token] + [word.lower().strip() for word in text.split(' ') if word.strip() != ''] + [close_token]
            for current_word, next_word in zip(vectorized_text, vectorized_text[1:]):
                self.chain.setdefault(current_word, []).append(next_word)



    def generate_quote(self, max_num_words = 25, ending_char = None):
        if not self.chain:
            raise MarkovChainError('The Markov Chain has not been trained.')
        else:
            current_word = random.choice(self.chain[open_token])
            sentence = []

            # We generate the text.
            for _ in range(0, max_num_words):
                if current_word is close_token:
                    break
                if current_word == ending_char:
                    break
                sentence.append(current_word)

                if current_word in self.chain:
                    current_word = random.choice(self.chain[current_word])
                else:
                    break

            generated_text = ' '.join(sentence)
            for char in ['.', ',', '!', '?']:
                generated_text = generated_text.replace(' '+char, char)
            return generated_text
