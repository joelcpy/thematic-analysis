# General Modules
import os

# NLP requirements
import nltk 
nltk.download("stopwords")
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re

# Gemsim
import gensim
from gensim.utils import simple_preprocess
import gensim.corpora as corpora
from gensim.models.phrases import  Phraser
stop_words = stopwords.words('english')

# spacy for lemmatization
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Navigate to the parent directory
parent_dir = os.path.dirname(os.getcwd())
model_path = os.path.join(parent_dir, 'models')

bigram= Phraser.load(model_path + "/bigram_mod.pkl")

def remove_stopwords(token_list: list[str]) -> list[str]:
    """Function removes stopwords"""

    return [word for word in simple_preprocess(' '.join(token_list)) if word not in stop_words]

def make_bigrams(token_list:list[str]) -> list[str]:
    """Function creates bigrams"""

    return bigram[token_list] 

def lemmatization(token_list: list[str], allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']) -> list[str]:
    """Function groups together the inflected forms of a word so they can be analysed as a single item"""

    doc = nlp(" ".join(token_list)) 
    return [token.lemma_ for token in doc if token.pos_ in allowed_postags]

def preprocessing_text(text:str) -> list[str]:
    """ 
    Function preprocess text for model prediction
    Args:
    - text: text extracted from URL
        
    Returns:
    - token list of cleaned text
    """
    # Parse html text and convert special characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Remove new line characters
    text = re.sub('\s+', ' ', text)
    # A fast was to remove numbers , punctuations etc that doesnt add any value to the model
    token_list = gensim.utils.simple_preprocess(text, deacc=True)
    # remove stopwords
    token_list = remove_stopwords(token_list)
    # Create bigrams
    token_list = make_bigrams(token_list)
    # Lemmatize text
    token_list = lemmatization(token_list)

    return token_list
