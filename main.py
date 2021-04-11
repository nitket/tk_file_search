"""
    Python project to serach files with extension ,merge files txt pdf docx
"""
import os
import tkinter as tk
from tkinter import ttk
import pathlib
import reuse
import logging
logging.basicConfig(filename='app.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')

files_groupwise = dict()
files_found_list = []
files_search_count = 0
files_total_count = 0
    
#GUI FUNCTIONS
def searchBtnClick():
    logging.info('search button clicked')
    try:
        search_btn['state'] = tk.DISABLED
        global statusvar,files_total_count,files_search_count,files_groupwise,files_found_list
        clearAllInputs()
        changeMergeButtonState()
        searchTerm = search_term.get()
        path = reuse.set_root(search_dir.get())
        ext= extension.get()

        if(searchTerm or ext):
            statusvar.set('Searching.')
            logging.info(f'searchFile function called searchTerm={searchTerm},extension={ext},path={path}')
            result = reuse.searchFile(searchTerm,ext,path)
            logging.info('searchFile function return result')

            if result['status'] == 'success':
                files_found_list = result['data']['files_found_list']
                files_groupwise = result['data']['files_groupwise']
                files_search_count = result['data']['files_search_count']
                files_total_count = result['data']['files_total_count']

                if type(files_found_list) == list and len(files_found_list) > 0:
                    for i,file in enumerate(files_found_list):
                        treev.insert("",'end',iid=int(i)+1,values=(int(i)+1,reuse.wrap(file)))
                    statusvar.set('Search Completed.')
                    changeMergeButtonState(files_groupwise)
                else:
                    statusvar.set('No Files Found')
                    logging.info('no files found')
        else:
            logging.info('search term or extension is required to search files')
            statusvar.set('Please enter serach term or extension to search for files.')
        search_btn['state'] = tk.NORMAL

    except Exception as e:
        logging.error(str(e))
        search_btn['state'] = tk.NORMAL

def removeAllTreeviewItems():
    logging.info('remove all tree view item called')
    for item in treev.get_children():
       treev.delete(item)
    logging.info('all items from treeview removed.')

def changeMergeButtonState(files_groupwise={}):
    logging.info('change merge button state called')
    if(len(files_groupwise)):
        for key in files_groupwise.keys():
            if key == 'txt':
                txt_merger_btn['state'] = tk.NORMAL
            elif key == 'pdf':
                pdf_merger_btn['state'] = tk.NORMAL
            elif key == 'docx':
                docx_merger_btn['state'] = tk.NORMAL
    else:
        txt_merger_btn['state'] = tk.DISABLED
        pdf_merger_btn['state'] = tk.DISABLED
        docx_merger_btn['state'] = tk.DISABLED 


def clearAllInputs():
    logging.info('clear all input function called')
    global files_total_count,files_search_count,files_groupwise,files_found_list

    files_groupwise = dict()
    files_found_list = []
    files_search_count = 0
    files_total_count = 0

    txt_merger_btn['state'] = tk.DISABLED
    pdf_merger_btn['state'] = tk.DISABLED
    docx_merger_btn['state'] = tk.DISABLED
    removeAllTreeviewItems()

def mergeFiles(file_type):
    logging.info(f'mergingFiles function called-{file_type}')
    try:
        setMergerBtnState(file_type,tk.DISABLED)
        global files_groupwise
        txt_merger_btn['state'] = tk.DISABLED
        if file_type == 'txt' and  'txt' in files_groupwise.keys() and len(files_groupwise['txt']) > 0:
            reuse.mergeTextFiles(files_groupwise['txt'])
        elif file_type == 'pdf' and 'pdf' in files_groupwise.keys() and len(files_groupwise['pdf']) > 0:
            reuse.mergePdfFiles(files_groupwise['pdf'])
        elif file_type == 'docx' and 'docx' in files_groupwise.keys() and len(files_groupwise['docx']) > 0:
            reuse.mergeDocxFiles(files_groupwise['docx'])
        else:
            logging.info(f'Merging not supported for {file_type}')
    except Exception as e:
        logging.error(str(e))
    logging.info(f'Merger finished-{file_type}')
    setMergerBtnState(file_type,tk.NORMAL)

def setMergerBtnState(btn_type,state):
    global txt_merger_btn,pdf_merger_btn,pdf_merger_btn
    if btn_type == 'txt':
        txt_merger_btn['state'] = state
    elif btn_type == 'pdf':
        pdf_merger_btn['state'] = state
    elif btn_type == 'docx':
        docx_merger_btn['state'] = state
#GUI
window = tk.Tk()
width = 800
height=600
#calculate coordination of screen and window form
positionRight = int( window.winfo_screenwidth()/2 - width/2 )
positionDown = int( window.winfo_screenheight()/2 - height/2 )

# Set window in center screen with following way.
window.geometry("{}x{}+{}+{}".format(width,height,positionRight, positionDown))
#title
window.title('File Finder')

#statusbar
statusvar = tk.StringVar()
statusvar.set("File Finder")
statusbar = tk.Label(window, textvariable=statusvar,relief=tk.SUNKEN, anchor=tk.W,fg="green")
statusbar.pack(side=tk.BOTTOM, fill=tk.X)

#search frame
search_frame = tk.Frame(bg='white')
search_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

tk.Label(master=search_frame,text="Search Term",bg="white").grid(row=0,column=0,pady=5,sticky='ew')
search_term = tk.Entry(master=search_frame)
search_term.grid(row=1,column=0,pady=5,ipady=5,ipadx=15,sticky='ew')

tk.Label(master=search_frame,text="Search Directory",bg="white").grid(row=0,column=1,pady=5,padx=5,sticky='ew')
search_dir = tk.Entry(master=search_frame)
search_dir.grid(row=1,column=1,pady=5,ipady=5,ipadx=15,padx=5,sticky='ew')

tk.Label(master=search_frame,text="Extension",bg="white").grid(row=0,column=2,pady=5,padx=5,sticky='ew')
extension = tk.Entry(master=search_frame)
extension.grid(row=1,column=2,pady=5,ipady=5,ipadx=15,padx=5,sticky='ew')

search_btn = tk.Button(master=search_frame,text="Search",command=searchBtnClick)
search_btn.grid(row=1,column=3,pady=5,ipady=3,padx=5,sticky='ew')

search_frame.pack(side='top',fill=tk.X,padx=5,pady=5)


#listing frame
listing_frame = tk.Frame(bg="white")
tk.Label(master=listing_frame,text="File Listing").pack()
    
treev = ttk.Treeview(master=listing_frame, selectmode ='none')

# Constructing vertical scrollbar
# with treeview
verscrlbar = ttk.Scrollbar(listing_frame, orient ="vertical", command = treev.yview)
verscrlbar.pack(side ='right', fill ='y')
horscrlbar = ttk.Scrollbar(listing_frame, orient ="horizontal", command = treev.xview)
horscrlbar.pack(side ='bottom', fill ='x')

# Configuring treeview
treev.configure(xscrollcommand = horscrlbar.set,yscrollcommand=verscrlbar.set)

style = ttk.Style(treev)
style.configure('Treeview', rowheight=40)  #word wrap

# Defining number of columns
treev["columns"] = (1,2)
# Assigning the width and anchor to  the
# respective columns
treev.column("#0", width=0,stretch=tk.NO,minwidth=100)
treev.column("#1", width = 150,anchor="center" ,minwidth=200,stretch=tk.NO)
treev.column("#2", width = 400,anchor="w",minwidth=400)
    
# Assigning the heading names to the 
# respective columns
treev.heading("#1", text ="No.")
treev.heading("#2", text ="File")

treev.pack(side='top',fill=tk.X)
listing_frame.pack(side='top',fill=tk.X,padx=5,pady=5)

#merger frame
merger_frame = tk.Frame(bg="white")

merger_frame.grid_columnconfigure((0, 1, 2), weight=1)

txt_merger_btn = tk.Button(master=merger_frame,text="Merge Text Files",state=tk.DISABLED,command=lambda:mergeFiles('txt'))
txt_merger_btn.grid(row=0,column=0,padx=5,pady=5,sticky="ew")

pdf_merger_btn = tk.Button(master=merger_frame,text="Merge PDF Files",state=tk.DISABLED,command=lambda:mergeFiles('pdf'))
pdf_merger_btn.grid(row=0,column=1,padx=5,pady=5,sticky="ew")

docx_merger_btn = tk.Button(master=merger_frame,text="Merge DOCX Files",state=tk.DISABLED,command=lambda:mergeFiles('docx'))
docx_merger_btn.grid(row=0,column=2,padx=5,pady=5,sticky="ew")

merger_frame.pack(side='top',fill=tk.BOTH,padx=5,pady=5,expand=tk.YES)

window.mainloop()






