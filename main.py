import nltk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd

from pyquery import PyQuery

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

root = Tk()
root["bg"] = "blue"
root.title("Parser tree")
root.resizable(width=False, height=False)
root.geometry("900x400+200+150")
label = Label(root, text='INPUT YOUR TEXT:', height=2, width=30, bg='light cyan')
label.grid(row=0, column=1)
calculated_text = Text(root, height=15, width=115)
calculated_text.grid(row=1, column=0, sticky='nsew', columnspan=3, rowspan=3)


def html_parser(html):
    pq = PyQuery(html)
    tag = pq('textarea')
    return tag.text()


def open_file_and_input_text():
    file_name = fd.askopenfilename(filetypes=(("Html files", "*.html"),))
    if file_name != '':
        with open(file_name, 'r') as file:
            text = file.read()
            text = html_parser(text)
            calculated_text.delete(1.0, END)
            calculated_text.insert(1.0, text)


def information():
    messagebox.askquestion("Help", "1. Input text or open file.\n"
                                   "2. Send button 'CREATE'.\n"
                                   "3. Look at the painted syntax tree.", type='ok')


grammar = r"""
        P: {<PRT|ADP>}
        V: {<VERB>}
        N: {<NOUN|PRON>}
        NP: {<N|NP|P>+<ADJ|NUM|DET>+}
        NP: {<ADJ|NUM|DET>+<N|NP|P>+}
        PP: {<P><NP>|<NP><P>}
        VP: {<NP|N><V>}
        VP: {<VP><NP|N||ADV>}
        VP: {<NP|N|ADV><VP>}
        VP: {<VP><PP|P>}
        """


def draw_syntax_tree():
    text = calculated_text.get(1.0, END)
    text = text.replace('\n', '')
    if text != '':
        doc = nltk.word_tokenize(text)
        doc = nltk.pos_tag(doc, tagset='universal')
        text_without_punct = []
        for item in doc:
            if item[1] != ',' and item[1] != '.':
                text_without_punct.append(item)
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(text_without_punct)
        result.draw()


button1 = Button(text="CREATE", height=3, width=20, command=draw_syntax_tree, bg='light cyan')
button1.grid(row=4, column=0)
button2 = Button(text="OPEN FILE", height=3, width=20, command=open_file_and_input_text, bg='light cyan')
button2.grid(row=4, column=1)
button3 = Button(text="HELP", height=3, width=20, command=information, bg='light cyan')
button3.grid(row=4, column=2)
root.mainloop()
