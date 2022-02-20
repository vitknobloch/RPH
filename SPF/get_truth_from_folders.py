import os
import random
from email.message import Message
from email.parser import Parser

def get_filenames(directory):
    file_list = os.listdir(directory)
    return file_list

def get_file_dict(directories_class_list):
    file_dict = dict()
    for dc in directories_class_list:
        file_list = get_filenames(dc[0])
        for f in file_list:
            file_dict[f] = dc[1]

    return file_dict

def write_file(filename, directories_class_list):
    file_dict = get_file_dict(directories_class_list)

    key_list = list(file_dict.keys())
    random.shuffle(key_list)

    counter = 0
    for t in key_list:
        print(t, file_dict[t])
        counter += 1

    with open(filename, mode='w', encoding='utf-8') as f:
        for t in key_list:
            f.write(f'{t} {file_dict[t]}\n')

    return counter

def replace_with_text(directory):
    filenames = get_filenames(directory)
    
    
    for fn in filenames:
        emailstr = ''
        print(fn)
        with open(f'{directory}/{fn}', mode='r', encoding='utf-8') as f:
            email = Parser().parse(f)
            emailstr = email.as_string()
        
        with open(f'{directory}/{fn}', mode='w', encoding='utf-8') as f:
            f.write(emailstr)




if __name__ == '__main__':

    #replace_with_text('data/4')

    folders = [
        ('data/archive/ham', 'OK'),
        ('data/archive/spam', 'SPAM')
        ]
    target = 'data/!truth.txt'

    print(write_file(target, folders))
    print('Done')


