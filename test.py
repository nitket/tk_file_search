files_groupwiese = {'txt':['files']}

print('txt' in files_groupwiese.keys())

if 'txt' in files_groupwiese.keys():
    files_groupwiese['txt'].append('new file')

print(files_groupwiese)