import tkinter
from pathlib import Path

from index import Index
from search import Search

DEFAULT_FONT = ('Helvetica', 20)

# reads the position record from a file into a dictionary
def readPositionRecord(input_file : str) -> dict:
    position_record = dict() # {term(str) : pos(int)}
    with open(input_file, 'r') as file:
        line = file.readline()
        position_record = eval(line.rstrip())

    return position_record


# GUI for search engine built using Tkinter
class SearchApp:
    def __init__(self):
        # main window
        self._root_window = tkinter.Tk()
        self._root_window.title("ICS Search Engine")
        self._root_window.configure(bg = "white")
        self._root_window.geometry("500x500")

        self._results_text = "" # displayed on screen when something is searched
        self._query = "" # user entered query

        self._path = Path("/Users/meggie/Downloads/DEV") 
        self.index = Index(self._path)
        self.pos_record = readPositionRecord("position_record.txt")
        self.pos_record2 = readPositionRecord("position_record2.txt")
        self.pos_record3 = readPositionRecord("position_record3.txt")

        # text label
        self._label = tkinter.Label(
            master = self._root_window,
            text = "Enter here to search",
            bg = "white",
            fg = "black",
            font = ("Helvetica", 15, "bold"),
            anchor = tkinter.CENTER)
        
        # text label formatting
        self._label.grid(
            row = 0, column = 0, columnspan = 3, pady = 2,
            sticky = tkinter.W + tkinter.E + tkinter.N
        )

        # text entry box (for user to enter query into)
        self._text_entry = tkinter.Entry(
            master = self._root_window,
            font = ("Helvetica", 10),
            width = 30,
            bd = 2,
            bg = "white",
            fg = "black",
            highlightbackground = "white",
            justify = tkinter.LEFT)
        # text entry box formatting
        self._text_entry.grid(
            row = 1, column = 0, columnspan = 2, pady = 2, padx = 2,
            sticky = tkinter.W + tkinter.E + tkinter.N
        )

        # "Search" button
        self._enter_button = tkinter.Button(
            master = self._root_window,
            text = "Search",
            font = ("Helvetica", 10, "bold"),
            width = 10, 
            bg = "light blue",
            bd = 2,
            highlightbackground = "white",
            command = self._search_button_pressed)
        # "Search" button formatting
        self._enter_button.grid(
            row = 1, column = 2, pady=2, padx = 2,
            sticky = tkinter.W + tkinter.E + tkinter.N
        )

        # results text label
        self._results = tkinter.Label(
            master = self._root_window,
            text = self._results_text, # result1\nresult2
            bg = "white",
            fg = "black",
            font = ("Helvetica", 12),
            justify = tkinter.LEFT,
            anchor = tkinter.W)
        # results text formatting
        self._results.grid(
            row = 2, column = 0, columnspan = 3, pady = 4, padx = 10,
            sticky = tkinter.W + tkinter.E + tkinter.N
        )

        # configuring grid rows/columns
        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 0)
        self._root_window.rowconfigure(2, weight = 1)

        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)
        self._root_window.columnconfigure(2, weight = 0)

    def _search_button_pressed(self):
        self._button_pressed = True
        self._query = self._text_entry.get()
        self._text_entry.delete(0, tkinter.END)
        # show search results. If not successful, diplay error message
        try:
            self.search = Search("tfIDF", self.pos_record, self.pos_record2, self.pos_record3, self._query)    
            self.setResults([self.index.geturlID(id) for _, id in self.search.getPages()])
        except:
            self._results_text = "Bad input. Try again."
        self._results.config(text = self._results_text)
        
    # starts Tkinter event loop
    def run(self) -> None:
        self._root_window.mainloop()
            
    # sets text of results label
    def setResults(self, results : list):
        self._results_text = '\n'.join(results)


if __name__ == "__main__":
    search_app = SearchApp()
    search_app.run()