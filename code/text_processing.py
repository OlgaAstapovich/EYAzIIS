import nltk
from nltk.corpus import stopwords
import pandas as pd
from tkinter.filedialog import *

stop_words = set(stopwords.words("english"))


def download_text_from_file():
    file = askopenfile(mode='r', filetypes=[('Text Files', '*.txt')])
    if file:
        text = []
        for line in file:
            text.append(line)
        return text


def process_input_text(file):
    with open(file) as file:
        text = []
        for line in file:
            text.append(line)
        return text


def download_input_text(textfield):
    try:
        text = []
        text.append(textfield)
        return text
    finally:
        pass


def save_text_into_file(text):
    file = open("file.txt", "w")
    file.write(text)
    file.close()


def process_text(text):
    try:
        words = []
        for item in text:
            s = re.sub(r'[^\w\s]+|[\d]+', r'', item).strip()
            words.extend(nltk.word_tokenize(s.lower()))
        df = pd.DataFrame({
            'word': [word for word in words if (word not in stop_words)],
            'number': [1 for word in [word for word in words if (word not in stop_words)]],
            'additional information': ["" for word in [word for word in words if (word not in stop_words)]]})
        new_df = pd.DataFrame(data=df.groupby(['word', 'additional information'], as_index=False)['number'].count(),
                          columns=["word", "additional information", "number"])
        return new_df
    finally:
        pass


def fill_dictionary(data, visual_dictionary):
    try:
        for i in range(data['word'].size):
            visual_dictionary.insert('', 'end', values=(
            data.loc[i, 'word'], "{:.2}".format(data.loc[i, 'number'] / data['word'].size),
            data.loc[i, 'additional information']))

    finally:
        pass
