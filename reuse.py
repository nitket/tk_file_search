import textwrap
import PyPDF2
import docx
import pathlib
import platform
import os

def set_root(s):
    if len(s) > 0:
        return s
    else:
        return '/'

def wrap(string, lenght=80):
    return "\n".join(textwrap.wrap(str(string), lenght))

def mergeTextFiles(files):
    if(type(files) == list and len(files) > 0):

        new_file = open('merger_text.txt','w')

        for filename in files:
            try:
                read_file = open(filename,'r')
                new_file.write(read_file.read())
                new_file.write("\n")
                read_file.close()
            except:
                print(f'file not found {filename}')
        new_file.close()
        return {'status':'success','msg':'TXT merged successful','filename':'merger_text.txt'}

    else:
        return {'status':'error','msg':'No files to merge'}

def mergePdfFiles(files):

    if(type(files) == list and len(files) > 0):

        new_file = open('merger_pdf.pdf','wb')
        pdf_merger = PyPDF2.PdfFileMerger(strict=False)

        for filename in files:
            try:
                read_file = open(filename,'rb')
                pdf_merger.append(read_file)
            except:
                print(f'file not found {filename}')
        pdf_merger.write(new_file)
        pdf_merger.close()
        new_file.close()
        return {'status':'success','msg':'Pdf merged successful','filename':'merger_pdf.pdf'}
    else:
        return {'status':'error','msg':'No files to merge'}

def mergeDocxFiles(files):
    if(type(files) == list and len(files) > 0):
        new_file = docx.Document()

        for filename in files:
            try:
                read_file = docx.Document(filename)
                for element in read_file.element.body:
                    new_file.element.body.append(element)
        
            except:
                print(f'file not found {filename}')
        new_file.save('merger_doc.docx')
        return {'status':'success','msg':'DOCX merged successful','filename':'merger_doc.docx'}

    else:
        return {'status':'error','msg':'No files to merge'}

#this function is working for function file_search()
def file_search2(filename,searchTerm=None,extension=None):
    check = True
    if searchTerm != None and searchTerm != "" and extension != None and extension != "":
        if searchTerm in filename and filename.endswith(extension):
            pass
        else:
            check = False
    elif searchTerm:
        if searchTerm in filename:
            pass
        else:
            check = False
    elif extension:
        if filename.endswith('.'+extension):
            pass
        else:
            check = False
    else:
        check = False
        
    return check

def searchFile(searchTerm,extension=None,path="/"):
    searchTerm = searchTerm.lower()
    extension = extension.lower() if extension != None and extension != "" else extension
    if searchTerm == "" and extension == "":
        return {"success":'error','msg':"Searchterm or extension is required"}
    
    file_list = open('file_list.txt','w')
    files_search_count = 0
    files_total_count = 0
    files_groupwise = dict()
    files_found_list = []

    os_info = platform.platform()
    for root, dirs, files in os.walk(path, topdown=False):
        files_search_count = files_search_count + 1
        for name in files:
            filename = name.lower()
            if file_search2(filename,searchTerm,extension):
                if('Windows' in os_info):
                    file_list.write(root+'\\'+name+'\n')
                    files_total_count = files_total_count + 1
                    files_found_list.append(root+'\\'+name)
                    file_extension = pathlib.Path(name).suffix.lower().replace('.','')

                    if file_extension in files_groupwise.keys():
                        files_groupwise[file_extension].append(root+'\\'+name)
                    else:
                        files_groupwise[file_extension] = [root+'\\'+name]
                else:
                    file_list.write(root+'/'+name+'\n')
                    files_total_count = files_total_count + 1
                    files_found_list.append(root+'/'+name)
                    file_extension = pathlib.Path(name).suffix.lower().replace('.','')

                    if file_extension in files_groupwise.keys():
                            files_groupwise[file_extension].append(root+'/'+name)
                    else:
                        files_groupwise[file_extension] = [root+'/'+name]

    file_list.close()
    return {'status':'success','msg':'Search Successfull','data':{'files_found_list':files_found_list,'files_groupwise':files_groupwise,'files_search_count':files_search_count,'files_total_count':files_total_count}}
    
