import os
from email.parser import Parser

class Corpus:
    '''Class wrapping corpus (folder) of email files to train or evaluate'''

    def __init__(self, dir_path):
        '''Corpus class constructor'''
        self.directory = dir_path
        

    def emails(self):
        '''
        Generator function, returning content of email files one by one
        '''
        email_list = os.listdir(self.directory)

        for email_filename in email_list:
            #skip metadata files
            if email_filename.startswith('!'):
                continue            
            
            email_body = self.get_email_body(email_filename)
            if(email_body == None):
                continue
            
            yield email_filename, email_body

    
    def get_email_body(self, email_filename):
        '''
        Extracts text from file of email
        Params:
        email_filename - filename of email to proccess
        '''
        try:
            with open(os.path.join(self.directory, email_filename), mode='r', encoding='utf-8') as f:
                email_body = Parser().parse(f).as_string()
        except:
            self.add_to_unreadable(email_filename)
            email_body = None
        
        return email_body

    
    def add_to_unreadable(self, email_filename):
        '''
        Appends emails name to list of unreadable files in !unreadable.txt
        '''
        with open(os.path.join(self.directory, '!unreadable.txt'), mode='a', encoding='utf-8') as f:
            #Saves unreadable files' filenames to metadata file !unreadable.txt
            f.write(f'{email_filename}\n')
