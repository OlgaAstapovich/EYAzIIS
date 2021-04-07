from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from DB_connector import *


from text_processing import *

class Window:
    def __init__(self, width=900, height=600, x=200, y=50, title="MyWindow", resizable=(False, False)):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))
        self.root.resizable(resizable[0], resizable[1])
        self.main_frame = Frame(self.root)


    def draw_widgets(self):
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar)
        self.filemenu.add_command(label="New", command=self.draw_input_widgets)
        self.filemenu.add_command(label="Open dictionary", command=lambda :(self.show_dictionary(), load_table('my_dictionary', self.dictionary)))
        self.filemenu.add_command(label="Load text from file",
                                  command=self.create_dictionary_from_text_file)
        self.filemenu.add_command(label="Save", command=lambda: save_table("my_dictionary", self.dictionary))
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.main_frame.pack(anchor=N)

    def draw_input_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.input_frame = Frame(self.main_frame)
        self.input_frame.pack(anchor=N)
        self.textfield = ScrolledText(self.input_frame, height=20, width=110)
        self.textfield.pack(padx=2, pady=2)
        self.processing_button = Button(self.input_frame, text="Process text",
                                        command=lambda: (
                                            save_text_into_file(self.textfield.get("1.0", END)), self.show_dictionary(),
                                            self.fill_dictionary_from_file("file.txt")))
        self.processing_button.pack(anchor=E, padx=10, pady=5)

    def show_dictionary(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.dictionary_frame = Frame(self.main_frame, width=250)
        self.button_frame = Frame(self.main_frame)
        self.dictionary = ttk.Treeview(self.dictionary_frame, height=15, columns=(1, 2, 3), show="headings")
        self.dictionary.heading(1, text="Word", anchor=W)
        self.dictionary.heading(2, text="Frequency of appearance", anchor=W)
        self.dictionary.heading(3, text="Additional information", anchor=W)
        self.vertical_dictionary_scroll = ttk.Scrollbar(self.dictionary_frame, orient="vertical",
                                                        command=self.dictionary.yview)
        self.dictionary.configure(yscrollcommand=self.vertical_dictionary_scroll.set)
        self.vertical_dictionary_scroll.pack(side=RIGHT, fill=Y, expand=False)
        self.edit_button = Button(self.button_frame, text="Edit", command=self.edit)

        self.dictionary_frame.pack(anchor=N, fill=BOTH)
        self.dictionary.pack(fill=BOTH)
        self.button_frame.pack()
        self.edit_button.pack(anchor=W)


    def fill_dictionary_from_file(self):
        fill_dictionary(process_text(download_text_from_file()), self.dictionary)


    def run(self):
        self.draw_widgets()
        self.root.mainloop()

    def edit(self):
        word = []
        for selection in self.dictionary.selection():
            item = self.dictionary.item(selection)
            word = item["values"][0:1]
        if word:
            edit_window = EditWindow(self.root, self.dictionary, text=word[0], title="Edit")
            edit_window.draw_widgets()
            edit_window.grab_focus()
        else:
            messagebox.showinfo(title="Hint", message="You should choose item from dictionary then click this button")

    def update(self):
        word_id = self.dictionary.focus()
        self.dictionary.set(word_id, '#3', value='text')

    def create_dictionary_from_text_file(self):
        text = download_text_from_file()
        if text:
            self.show_dictionary()
            fill_dictionary(process_text(text), self.dictionary)


class EditWindow:
    def __init__(self, parent, dictionary, text="word", width=300, height=200, x=200, y=50, title="Edit",
                 resizable=(False, False)):
        self.root = Toplevel(parent)
        self.dictionary = dictionary
        self.root.title(title)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))
        self.root.resizable(resizable[0], resizable[1])
        self.word = Label(self.root, text=text)
        self.entry = Entry(self.root, width=25)
        self.label = Label(self.root, text="Here you can write additional information to word you've chosen",
                           width=45, wraplength=200, relief=RAISED)
        self.ok_button = Button(self.root, text="Ok", width=15,
                                command=lambda: (self.update(self.entry.get()), self.root.destroy()))

    def draw_widgets(self):
        self.label.place(x=-3, y=0)
        self.word.place(x=25, y=90)
        self.entry.place(x=100, y=90)
        self.ok_button.place(x=100, y=150)

    def grab_focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()

    def get_text(self):
        return self.entry.get()

    def update(self, text):
        word_id = self.dictionary.focus()
        self.dictionary.set(word_id, '#3', value=text)

    def get_info(self):
        for selection in self.dictionary.selection():
            item = self.dictionary.item(selection)
            word = item["values"][2:3]
            print(word)
        return word


if __name__ == "__main__":
    window = Window()
    window.run()
