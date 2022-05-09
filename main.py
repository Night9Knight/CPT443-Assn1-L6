import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from dfa import DFA

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title("CPT443 Assignment 1")
        self.resizable(True, True)
        self.iconbitmap('./assets/fsm.ico')
        self.dfa = DFA()
        self.textList = tk.StringVar(value=['Waiting for input...'])
        self.accepted_words = []
        self.init_ui()
    
    def init_ui(self):
        self.init_frames()
        self.init_inputFrames()
        self.init_outputFrames()
    
    def init_frames(self):
        # Create the main label
        label = tk.Label(master=self, text="Adverbs DFA Matching", font=("Helvetica", 16))
        label.pack()

        # Create the main frames
        self.inputFrame = tk.Frame(master=self)
        self.inputFrame.pack(fill='both', expand=True, padx=10, pady=5, side='left')
        self.notebookFrame = tk.Frame(master=self)
        self.notebookFrame.pack(fill='both', expand=True, padx=5, pady=5, side='left')
    
    def init_inputFrames(self):
        # Create the widgets for first main frame
        inputBoxLbl = tk.Label(master=self.inputFrame, text="Input text:", font=("Helvetica", 10, 'bold'))
        self.inputBox = ScrolledText(master=self.inputFrame)
        buttonFrame = tk.Frame(master=self.inputFrame)
        loadFileBtn = tk.Button(master=buttonFrame, text="Load text file", command=self.loadFile)
        submitBtn = tk.Button(master=buttonFrame, text="Submit", command=self.submitInput)
        clearBtn = tk.Button(master=buttonFrame, text="Clear", command=self.clearInput)
        inputBoxLbl.pack(side=tk.TOP, anchor=tk.W)
        self.inputBox.pack(expand=True, fill='both')
        buttonFrame.pack(side=tk.BOTTOM, anchor=tk.W, fill='both', expand=True)
        loadFileBtn.pack(side=tk.LEFT, anchor=tk.W)
        submitBtn.pack(side=tk.LEFT, anchor=tk.W, padx=5)
        clearBtn.pack(side=tk.LEFT, anchor=tk.W)
    
    def init_outputFrames(self):
        # Create the widgets for second main frame
        outputLbl = tk.Label(master=self.notebookFrame, text="Output:", font=("Helvetica", 10, 'bold'))
        outputLbl.pack(side=tk.TOP, anchor=tk.W)
        notebook = ttk.Notebook(master=self.notebookFrame)
        notebook.pack(expand=True, anchor=tk.W, fill='both')

        wordListFrame = tk.Label(master=notebook)
        positionFrame = tk.Frame(master=notebook)
        wordOccurenceFrame = tk.Frame(master=notebook)
        wordListFrame.pack(fill='both', expand=True)
        positionFrame.pack(fill='both', expand=True)
        wordOccurenceFrame.pack(fill='both', expand=True)

        self.wordListBox = tk.Listbox(master=wordListFrame, listvariable=self.textList, selectmode='extended')
        self.wordListBox.pack(fill='both', expand=True, padx=5, pady=5, side='left')
        scrollbar = tk.Scrollbar(
            wordListFrame,
            orient='vertical',
            command=self.wordListBox.yview
        )
        scrollbar.pack(side='left', fill='y')
        self.wordListBox['yscrollcommand'] = scrollbar.set
        self.wordListBox.bind('<<ListboxSelect>>', self.items_selected)

        self.positionTextBox = ScrolledText(master=positionFrame)
        self.positionTextBox.pack(fill='both', expand=True, padx=5, pady=5)
        self.positionTextBox.insert("1.0", "Waiting for input...")
        self.positionTextBox.config(state='disabled')

        self.occurenceTextBox = ScrolledText(master=wordOccurenceFrame)
        self.occurenceTextBox.pack(fill='both', expand=True, padx=5, pady=5)
        self.occurenceTextBox.insert("1.0", "Waiting for input...")
        self.occurenceTextBox.config(state='disabled')

        notebook.add(wordListFrame, text="Word List")
        notebook.add(positionFrame, text="Matched text positions")
        notebook.add(wordOccurenceFrame, text="Matched words and occurences")

    def submitInput(self):
        inputString = self.inputBox.get("1.0", "end")
        if inputString.strip()!="":
            self.setPositionTextBox("Running the code...")
            self.setOccurenceTextBox("Running the code...")
            self.textList.set(['Running the code...'])
            self.accepted_words, occurrences, _ = self.dfa.matchInputString(inputString)
            positionList = []
            occurenceList = []

            # Check if the output dictionaries are empty
            if not self.accepted_words and not occurrences:
                self.setPositionTextBox("No matches found.")
                self.setOccurenceTextBox("No matches found.")
                self.textList.set(['No matches found.'])
            else:
                for word, coords in self.accepted_words.items():
                    positionList.append(f'Word "{word}" is accepted at position {coords}')
                    for coord in coords:
                        self.inputBox.tag_add("bold", f"1.0+{coord[0]}c", f"1.0+{coord[1]+1}c")
                
                for word, count in occurrences.items():
                    occurenceList.append(f'Word "{word}" occurs {count} times')
                
                self.textList.set([word for word in occurrences.keys()])

                self.inputBox.tag_config("bold", foreground="green", font=("Courier", 10, "bold"))
                self.setPositionTextBox("\n".join(positionList))
                self.setOccurenceTextBox("\n".join(occurenceList))
        else:
            self.setPositionTextBox("No input text provided.")
            self.setOccurenceTextBox("No input text provided.")
            self.textList.set(['No input text provided.'])
    
    def clearInput(self):
        self.inputBox.delete("1.0", "end")
        self.setPositionTextBox("Waiting for input...")
        self.setOccurenceTextBox("Waiting for input...")
        self.textList.set(['Waiting for input...'])
    
    def loadFile(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            with open(filepath, 'r') as f:
                self.inputBox.delete("1.0", "end")
                self.inputBox.insert("1.0", f.read())        

    def setPositionTextBox(self, text):
        self.positionTextBox.config(state='normal')
        self.positionTextBox.delete("1.0", "end")
        self.positionTextBox.insert("1.0", text)
        self.positionTextBox.config(state='disabled')
    
    def setOccurenceTextBox(self, text):
        self.occurenceTextBox.config(state='normal')
        self.occurenceTextBox.delete("1.0", "end")
        self.occurenceTextBox.insert("1.0", text)
        self.occurenceTextBox.config(state='disabled')
    
    def items_selected(self, event):
        """ handle item selected event
        """
        # get selected indices
        selected_indices = self.wordListBox.curselection()
        # get selected items
        selected_words = [self.wordListBox.get(i) for i in selected_indices]
        
        self.inputBox.tag_delete("highlight")

        for word in selected_words:
            if word in self.accepted_words:
                coords = self.accepted_words[word]
                for coord in coords:
                    self.inputBox.tag_add("highlight", f"1.0+{coord[0]}c", f"1.0+{coord[1]+1}c")
        
        self.inputBox.tag_config("highlight", background="yellow")


if __name__ == "__main__":
    app = App()
    app.mainloop()
        

# accepted_words = []

# def submitInput():
#     inputString = inputBox.get("1.0", "end")
#     setPositionTextBox("Running the code...")
#     setOccurenceTextBox("Running the code...")
#     textList.set(['Running the code...'])
#     if inputString.strip()!="":
#         global accepted_words
#         accepted_words, occurrences, _ = dfa.matchInputString(inputString)
#         positionList = []
#         occurenceList = []
        
#         for word, coords in accepted_words.items():
#             positionList.append(f'Word "{word}" is accepted at position {coords}')
#             for coord in coords:
#                 inputBox.tag_add("bold", f"1.0+{coord[0]}c", f"1.0+{coord[1]+1}c")
        
#         for word, count in occurrences.items():
#             occurenceList.append(f'Word "{word}" occurs {count} times')
        
#         textList.set([word for word in occurrences.keys()])

#         inputBox.tag_config("bold", foreground="green", font=("Times New Roman", 10, "bold"))
#         setPositionTextBox("\n".join(positionList))
#         setOccurenceTextBox("\n".join(occurenceList))

# def clearInput():
#     inputBox.delete("1.0", "end")
#     textList.set(['Waiting for input...'])
#     setPositionTextBox("Waiting for input...")
#     setOccurenceTextBox("Waiting for input...")

# def setPositionTextBox(text):
#     positionTextBox['state'] = 'normal'
#     positionTextBox.delete("1.0", "end")
#     positionTextBox.insert("1.0", text)
#     positionTextBox['state'] = 'disabled'

# def setOccurenceTextBox(text):
#     occurenceTextBox['state'] = 'normal'
#     occurenceTextBox.delete("1.0", "end")
#     occurenceTextBox.insert("1.0", text)
#     occurenceTextBox['state'] = 'disabled'

# def items_selected(event):
#     """ handle item selected event
#     """
#     # get selected indices
#     selected_indices = wordListBox.curselection()
#     # get selected items
#     selected_words = [wordListBox.get(i) for i in selected_indices]
    
#     inputBox.tag_delete("highlight")

#     for word in selected_words:
#         if word in accepted_words:
#             coords = accepted_words[word]
#             for coord in coords:
#                 inputBox.tag_add("highlight", f"1.0+{coord[0]}c", f"1.0+{coord[1]+1}c")
    
#     inputBox.tag_config("highlight", background="yellow")

# # Create the main window
# window = tk.Tk()
# window.geometry("1280x720")
# window.title("CPT443 Assignment 1")
# window.resizable(True, True)
# window.iconbitmap('./assets/fsm.ico')

# dfa = DFA()
# textList = tk.StringVar(value=['Waiting for input...'])

# # Create the main label
# label = tk.Label(master=window, text="Adverbs DFA Matching", font=("Helvetica", 16))
# label.pack()

# # Create the main frames
# inputFrame = tk.Frame(master=window)
# inputFrame.pack(fill='both', expand=True, padx=10, pady=5, side='left')
# notebookFrame = tk.Frame(master=window)
# notebookFrame.pack(fill='both', expand=True, padx=5, pady=5, side='left')

# # Create the widgets for first main frame
# inputBoxLbl = tk.Label(master=inputFrame, text="Input text:", font=("Helvetica", 10, 'bold'))
# inputBox = ScrolledText(master=inputFrame)
# buttonFrame = tk.Frame(master=inputFrame)
# submitBtn = tk.Button(master=buttonFrame, text="Submit", command=submitInput)
# clearBtn = tk.Button(master=buttonFrame, text="Clear", command=clearInput)
# inputBoxLbl.pack(side=tk.TOP, anchor=tk.W)
# inputBox.pack(expand=True, fill='both')
# buttonFrame.pack(side=tk.BOTTOM, anchor=tk.W, fill='both', expand=True)
# submitBtn.pack(side=tk.LEFT, anchor=tk.W)
# clearBtn.pack(side=tk.LEFT, anchor=tk.W, padx=5)

# # Create the widgets for second main frame
# outputLbl = tk.Label(master=notebookFrame, text="Output:", font=("Helvetica", 10, 'bold'))
# outputLbl.pack(side=tk.TOP, anchor=tk.W)
# notebook = ttk.Notebook(master=notebookFrame)
# notebook.pack(expand=True, anchor=tk.W, fill='both')

# wordListFrame = tk.Label(master=notebook)
# positionFrame = tk.Frame(master=notebook)
# wordOccurenceFrame = tk.Frame(master=notebook)
# wordListFrame.pack(fill='both', expand=True)
# positionFrame.pack(fill='both', expand=True)
# wordOccurenceFrame.pack(fill='both', expand=True)

# wordListBox = tk.Listbox(master=wordListFrame, listvariable=textList, selectmode='extended')
# wordListBox.pack(fill='both', expand=True, padx=5, pady=5, side='left')
# scrollbar = tk.Scrollbar(
#     wordListFrame,
#     orient='vertical',
#     command=wordListBox.yview
# )
# scrollbar.pack(side='left', fill='y')
# wordListBox['yscrollcommand'] = scrollbar.set
# wordListBox.bind('<<ListboxSelect>>', items_selected)

# positionTextBox = ScrolledText(master=positionFrame)
# positionTextBox.pack(fill='both', expand=True, padx=5, pady=5)
# positionTextBox.insert("1.0", "Waiting for input...")
# positionTextBox.config(state='disabled')

# occurenceTextBox = ScrolledText(master=wordOccurenceFrame)
# occurenceTextBox.pack(fill='both', expand=True, padx=5, pady=5)
# occurenceTextBox.insert("1.0", "Waiting for input...")
# occurenceTextBox.config(state='disabled')

# notebook.add(wordListFrame, text="Word List")
# notebook.add(positionFrame, text="Matched text positions")
# notebook.add(wordOccurenceFrame, text="Matched words and occurences")

# window.mainloop()