import xml.etree.ElementTree
from os.path import basename, splitext
from flask import Flask
from flask import render_template
from flask import jsonify

from markov_chain import MarkovChain

app = Flask(__name__)

def get_authors(corpora_address):
    authors = []
    for author_elem in xml.etree.ElementTree.parse(corpora_address).getroot():
       authors.append( {'id': author_elem.attrib['id'], 'name': author_elem.attrib['name'], 'image': author_elem.attrib['image']} )
    return authors

def get_filename(file_address):
    return splitext(basename(file_address))[0]

@app.route('/')
def index():
    corpora_address = app.root_path + "/corpora.xml"
    authors = get_authors(corpora_address)
    return render_template('index.html', authors=authors)

@app.route('/generate/<author_id>')
def generate_text(author_id):
    corpora_address = app.root_path + "/corpora.xml"
    markov_chain = MarkovChain()
    markov_chain.train(corpora_address, author_id)
    return jsonify( {'author': markov_chain.name, 'generated_text': markov_chain.generate_quote()} )

if __name__ == '__main__':
    app.run()
