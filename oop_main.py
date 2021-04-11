import os
import tkinter as tk
from tkinter import ttk
import pathlib
import reuse
import logger

class App(tk.Tk):

    __logging = logger.Logger()
    def __init__(self):
        super().__init__()

        self.__main_width = 800
        self.__main_height = 600
        self.files_found_list = []
        self.files_groupwise = dict()
        self.files_search_count = 0
        self.files_total_count = 0

        #calculate coordination of screen and window form
        positionRight = int(self.winfo_screenwidth()/2 - self.__main_width/2)
        positionDown = int(self.winfo_screenheight()/2 - self.__main_height/2)

        # configure the root window
        self.title('File Finder')
        self.geometry("{}x{}+{}+{}".format(self.__main_width,
                                           self.__main_height, positionRight, positionDown))

        self.createStatusBar()
        self.createSearchFrame()
        self.createListingFrame()
        self.createMergerFrame()

    def createStatusBar(self):
        #statusbar
        self.statusvar = tk.StringVar()
        self.statusvar.set("File Finder")
        self.statusbar = tk.Label(
            self, textvariable=self.statusvar, relief=tk.SUNKEN, anchor=tk.W, fg="green")
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def createSearchFrame(self):

        #search frame
        self.search_frame = tk.Frame(self, bg='white')
        self.search_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        tk.Label(master=self.search_frame, text="Search Term", bg="white").grid(
            row=0, column=0, pady=5, sticky='ew')
        self.search_term = tk.Entry(master=self.search_frame)
        self.search_term.grid(row=1, column=0, pady=5,
                         ipady=5, ipadx=15, sticky='ew')

        tk.Label(master=self.search_frame, text="Search Directory", bg="white").grid(
            row=0, column=1, pady=5, padx=5, sticky='ew')
        self.search_dir = tk.Entry(master=self.search_frame)
        self.search_dir.grid(row=1, column=1, pady=5, ipady=5,
                        ipadx=15, padx=5, sticky='ew')

        tk.Label(master=self.search_frame, text="Extension", bg="white").grid(
            row=0, column=2, pady=5, padx=5, sticky='ew')
        self.extension = tk.Entry(master=self.search_frame)
        self.extension.grid(row=1, column=2, pady=5, ipady=5,
                       ipadx=15, padx=5, sticky='ew')

        self.search_btn = tk.Button(master=self.search_frame,
                               text="Search", command=self.searchBtnClick)
        self.search_btn.grid(row=1, column=3, pady=5, ipady=3, padx=5, sticky='ew')

        self.search_frame.pack(side='top', fill=tk.X, padx=5, pady=5)

    def createListingFrame(self):
        #listing frame
        self.listing_frame = tk.Frame(self,bg="white")
        tk.Label(master=self.listing_frame, text="File Listing").pack()

        self.treev = ttk.Treeview(master=self.listing_frame, selectmode='none')

        # Constructing vertical scrollbar
        # with treeview
        self.verscrlbar = ttk.Scrollbar(
            self.listing_frame, orient="vertical", command=self.treev.yview)
        self.verscrlbar.pack(side='right', fill='y')
        self.horscrlbar = ttk.Scrollbar(
            self.listing_frame, orient="horizontal", command=self.treev.xview)
        self.horscrlbar.pack(side='bottom', fill='x')

        # Configuring treeview
        self.treev.configure(xscrollcommand=self.horscrlbar.set,
                        yscrollcommand=self.verscrlbar.set)

        style = ttk.Style(self.treev)
        style.configure('Treeview', rowheight=35)  # word wrap

        # Defining number of columns
        self.treev["columns"] = (1, 2)
        # Assigning the width and anchor to  the
        # respective columns
        self.treev.column("#0", width=0, stretch=tk.NO, minwidth=100)
        self.treev.column("#1", width=150, anchor="center",
                     minwidth=200, stretch=tk.NO)
        self.treev.column("#2",anchor="w")

        # Assigning the heading names to the
        # respective columns
        self.treev.heading("#1", text="No.")
        self.treev.heading("#2", text="File")

        self.treev.pack(side='top', fill=tk.X)
        self.listing_frame.pack(side='top', fill=tk.X, padx=5, pady=5)

    def createMergerFrame(self):
        #merger frame
        self.merger_frame = tk.Frame(self,bg="white")

        self.merger_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.txt_merger_btn = tk.Button(master=self.merger_frame, text="Merge Text Files",
                                   state=tk.DISABLED, command=lambda: self.mergeFiles('txt'))
        self.txt_merger_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.pdf_merger_btn = tk.Button(master=self.merger_frame, text="Merge PDF Files",
                                   state=tk.DISABLED, command=lambda: self.mergeFiles('pdf'))
        self.pdf_merger_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.docx_merger_btn = tk.Button(master=self.merger_frame, text="Merge DOCX Files",
                                    state=tk.DISABLED, command=lambda: self.mergeFiles('docx'))
        self.docx_merger_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.merger_frame.pack(side='top', fill=tk.BOTH,
                          padx=5, pady=5, expand=tk.YES)

    def searchBtnClick(self):
        self.__logging.log('info','search button clicked')
        try:
            self.search_btn['state'] = tk.DISABLED
            self.clearAllInputs()
            self.changeMergeButtonState()
            searchTerm = self.search_term.get()
            path = reuse.set_root(self.search_dir.get())
            ext = self.extension.get()

            if(searchTerm or ext):
                self.statusvar.set('Searching.')
                self.__logging.log('info',
                    f'searchFile function called searchTerm={searchTerm},extension={ext},path={path}')
                result = reuse.searchFile(searchTerm, ext, path)
                self.__logging.log('info','searchFile function return result')

                if result['status'] == 'success':
                    self.files_found_list = result['data']['files_found_list']
                    self.files_groupwise = result['data']['files_groupwise']
                    self.files_search_count = result['data']['files_search_count']
                    self.files_total_count = result['data']['files_total_count']

                    if type(self.files_found_list) == list and len(self.files_found_list) > 0:
                        for i, file in enumerate(self.files_found_list):
                            self.treev.insert("", 'end', iid=int(i)+1,
                                        values=(int(i)+1, reuse.wrap(file)))
                        self.statusvar.set('Search Completed.')
                        self.changeMergeButtonState(self.files_groupwise)
                    else:
                        self.statusvar.set('No Files Found')
                        self.__logging.log('info','no files found')
            else:
                self.__logging.log('info',
                    'search term or extension is required to search files')
                self.statusvar.set(
                    'Please enter serach term or extension to search for files.')

        except Exception as e:
            self.__logging.log('error',str(e))

        self.search_btn['state'] = tk.NORMAL


    def removeAllTreeviewItems(self):
        self.__logging.log('info','remove all tree view item called')
        for item in self.treev.get_children():
            self.treev.delete(item)
        self.__logging.log('info','all items from treeview removed.')


    def changeMergeButtonState(self,files_groupwise={}):
        self.__logging.log('info','change merge button state called')
        if(len(files_groupwise)):
            for key in files_groupwise.keys():
                if key == 'txt':
                    self.txt_merger_btn['state'] = tk.NORMAL
                elif key == 'pdf':
                    self.pdf_merger_btn['state'] = tk.NORMAL
                elif key == 'docx':
                    self.docx_merger_btn['state'] = tk.NORMAL
        else:
            self.txt_merger_btn['state'] = tk.DISABLED
            self.pdf_merger_btn['state'] = tk.DISABLED
            self.docx_merger_btn['state'] = tk.DISABLED


    def clearAllInputs(self):
        self.__logging.log('info','clear all input function called')

        self.files_groupwise = dict()
        self.files_found_list = []
        self.files_search_count = 0
        self.files_total_count = 0

        self.txt_merger_btn['state'] = tk.DISABLED
        self.pdf_merger_btn['state'] = tk.DISABLED
        self.docx_merger_btn['state'] = tk.DISABLED
        self.removeAllTreeviewItems()


    def mergeFiles(self,file_type):
        self.__logging.log('info',f'mergingFiles function called-{file_type}')
        try:
            self.setMergerBtnState(file_type, tk.DISABLED)
            self.txt_merger_btn['state'] = tk.DISABLED
            if file_type == 'txt' and 'txt' in self.files_groupwise.keys() and len(self.files_groupwise['txt']) > 0:
                reuse.mergeTextFiles(self.files_groupwise['txt'])
            elif file_type == 'pdf' and 'pdf' in self.files_groupwise.keys() and len(self.files_groupwise['pdf']) > 0:
                reuse.mergePdfFiles(self.files_groupwise['pdf'])
            elif file_type == 'docx' and 'docx' in self.files_groupwise.keys() and len(self.files_groupwise['docx']) > 0:
                reuse.mergeDocxFiles(self.files_groupwise['docx'])
            else:
                self.__logging.log('info',f'Merging not supported for {file_type}')
        except Exception as e:
            self.__logging.log('error',str(e))
        self.__logging.log('info',f'Merger finished-{file_type}')
        self.setMergerBtnState(file_type, tk.NORMAL)


    def setMergerBtnState(self,btn_type, state):
        if btn_type == 'txt':
            self.txt_merger_btn['state'] = state
        elif btn_type == 'pdf':
            self.pdf_merger_btn['state'] = state
        elif btn_type == 'docx':
            self.docx_merger_btn['state'] = state
    


if __name__ == "__main__":
    app = App()
    app.mainloop()
