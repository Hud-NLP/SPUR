import nltk, string, regex
from   datetime import datetime
from   sklearn.feature_extraction.text import TfidfVectorizer

def msg(*text_items, seperator = "\t"):
    text_to_show = ""
    for each_item in text_items:
        text_to_show += str(each_item) + seperator
    time_now = str(datetime.now().strftime("%H:%M:%S"))
    print("=== %s %s\t" %(time_now, text_to_show))

def cleanse_special_characters(text):
    cleansing_rules = [("\n+"           , " "           ),  # Remove line feeds (regex "+" is "one or more")
                       (" {2,}"         , " "           ),  # Multiple spaces to single space
                       ("\""            , "\'"          ),  # Convert double quotes to single quotes
                       ("\\\\"            , "/"           )   # Convert escape to forward slash
                       ]
    return_text = text
    for each_rule in cleansing_rules:  # Apply the cleansing rules in turn to the output text
        return_text = regex.sub(each_rule[0], each_rule[1], return_text)  # regex.sub does the search and replace

    return return_text

def return_alphanum(text):
    return_text = regex.sub("[^ -~]+", "", text)
    return_text = regex.sub("\"", "\'", return_text)
    return return_text

def file_to_clean_text(file):
    cleansing_rules =   [   ("\n+"   ,   " "     ),       # Remove line feeds (regex "+" is "one or more")
                            (" {2,}" ,   " "     ),       # Multiple spaces to single space
                            ("\""    ,   "\'"    )        # Convert double quotes to single quotes
                        ]
    return_text = ""
    for row in file:                                      # Add each row of the input file to the output text
        return_text += row

    for each_rule in cleansing_rules:                     # Apply the cleansing rules in turn to the output text
        return_text = regex.sub(each_rule[0], each_rule[1], return_text)    # regex.sub does the search and replace

    return return_text

def clean_text(sentence):
    sentence  = sentence.lower()
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    new_words = tokenizer.tokenize(sentence)
    result    = ""
    for each_word in new_words:
        result += (each_word  + " ")
    result = result[:-1]
    return result

# TFIDF-weighted cosine similarity code here:
#https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):    #remove punctuation, lowercase, stem
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return (tfidf * tfidf.T).A[0, 1]