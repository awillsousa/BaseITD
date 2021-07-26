# -*- coding: utf-8 -*-
import re
from sys import stdout
import argparse
import re
import nltk
from nltk.tokenize import word_tokenize


# Tokenizador para portugues 
sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')

# Punctuation list
#punctuations = re.escape('!"#%\'()*+,./:;<=>?@[\\]^_`{|}~')
punctuations = re.escape('ºª§!"#%\'()*+,./:;<=>?@[\\]^_`{|}~') 

# ##### #
# Regex #
# ##### #
re_remove_brackets = re.compile(r'\{.*\}')
re_remove_html = re.compile(r'<(\/|\\)?.+?>', re.UNICODE)
re_transform_numbers = re.compile(r'\d', re.UNICODE)
re_transform_emails = re.compile(r'[^\s]+@[^\s]+', re.UNICODE)
re_transform_url = re.compile(r'(http|https)://[^\s]+', re.UNICODE)
# Different quotes are used.
re_quotes_1 = re.compile(r"(?u)(^|\W)[‘’′`']", re.UNICODE)
re_quotes_2 = re.compile(r"(?u)[‘’`′'](\W|$)", re.UNICODE)
re_quotes_3 = re.compile(r'(?u)[‘’`′“”]', re.UNICODE)
re_dots = re.compile(r'(?<!\.)\.\.(?!\.)', re.UNICODE)
re_punctuation = re.compile(r'([,";:]){2},', re.UNICODE)
re_hiphen = re.compile(r' -(?=[^\W\d_])', re.UNICODE)
re_tree_dots = re.compile(u'…', re.UNICODE)
# Differents punctuation patterns are used.
re_punkts = re.compile(r'(\w+)([%s])([ %s])' %
                       (punctuations, punctuations), re.UNICODE)
re_punkts_b = re.compile(r'([ %s])([%s])(\w+)' %
                         (punctuations, punctuations), re.UNICODE)
re_punkts_c = re.compile(r'(\w+)([%s])$' % (punctuations), re.UNICODE)
re_double_punkt = re.compile(r'([%s])+(?=[%s])'%(punctuations, punctuations), re.UNICODE)
re_only_punkt = re.compile(r'(^[%s]$)'%(punctuations), re.UNICODE)
re_changehyphen = re.compile(u'–')
re_doublequotes_1 = re.compile(r'(\"\")')
re_doublequotes_2 = re.compile(r'(\'\')')
re_trim = re.compile(r' +', re.UNICODE)


def clean_setence(sent):
    tokens = []
    for w in word_tokenize(sent):
        if not re_only_punkt.match(w) and len(w) > 1:
            tokens.append(w)
        
    return " ".join(tokens)

def clean_text(text):
    """Apply all regex above to a given string."""
    text = text.lower()
    text = text.replace('\xa0', ' ')
    text = re_tree_dots.sub('...', text)
    text = re.sub('\.\.\.', '', text)
    text = re_remove_brackets.sub('', text)
    text = re_changehyphen.sub('-', text)
    text = re_remove_html.sub(' ', text)
    text = re_transform_numbers.sub('', text)
    text = re_transform_url.sub('URL', text)
    text = re_transform_emails.sub('EMAIL', text)
    text = re_quotes_1.sub(r'\1"', text)
    text = re_quotes_2.sub(r'"\1', text)
    text = re_quotes_3.sub('"', text)
    text = re.sub('"', '', text)
    text = re_dots.sub('.', text)
    text = re_punctuation.sub(r'\1', text)    
    text = re_hiphen.sub(' - ', text)
    text = re_punkts.sub(r'\1 \2 \3', text)
    text = re_punkts_b.sub(r'\1 \2 \3', text)
    text = re_punkts_c.sub(r'\1 \2', text)
    text = re_double_punkt.sub(r'', text)
    
    text = re_doublequotes_1.sub('\"', text)
    text = re_doublequotes_2.sub('\'', text)
    text = re_trim.sub(' ', text)
    
    return text.strip()


def normalize(s):    
    s = s.lower()    
    # Isolate punctuation
    s = re.sub(r'([\'\"\.\(\)\!\?\-\\\/\,])', r' \1 ', s)
    # Remove some special characters
    s = re.sub(r'([\;\:\|•«\n])', ' ', s)
    # Replace numbers and symbols with language
    s = s.replace('&', ' e ')
    s = s.replace('@', ' arroba ')
    s = s.replace('0', ' zero ')
    s = s.replace('1', ' um ')
    s = s.replace('2', ' dois ')
    s = s.replace('3', ' tres ')
    s = s.replace('4', ' quatro ')
    s = s.replace('5', ' cinco ')
    s = s.replace('6', ' seis ')
    s = s.replace('7', ' sete ')
    s = s.replace('8', ' oito ')
    s = s.replace('9', ' nove ')
    
    return s
