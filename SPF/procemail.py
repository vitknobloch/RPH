from email.message import Message
from email.parser import Parser, HeaderParser
import re
from collections import Counter

class ProcessedEmail:
    '''Class wrapping a single email messege and it's content'''
    def __init__(self, filename, token_counter, url_counter, headers, truth=None):
        '''
        ProcessedEmail class constructor
        Params:
        filename: filename of the email's file
        token_counter: Counter with number of occurences of individual tokens
        url_counter: Counter with number of occutences of different URLs
        headers: dictionary od email headers
        truth (optional): this emails correct label (default None)
        '''
        self.filename = filename
        self.token_counter = token_counter
        self.url_counter = url_counter
        self.headers = headers
        self.truth = truth

        #Note: Only token_counter is used for evaluation in this version


    def __init__(self, filename, body, truth=None):
        '''
        ProcessedEmail class constructor
        Params:
        filename: filename of the email's file
        body: content of the email file
        truth (optional): this emails correct label (default None)
        '''
        self.filename = filename
        self.truth = truth

        email = Parser().parsestr(body)
        self.headers = HeaderParser().parsestr(body)

        urls, payload_tokens = self.tokenize_payload(email.get_payload())

        #if subject exists, add subject tokens to body tokens
        if(self.headers['subject']):
            header_urls, header_tokens = self.tokenize_payload(self.headers['subject'])
            payload_tokens += header_tokens
            urls += header_urls

        self.token_counter = Counter(payload_tokens)
        self.url_counter = Counter(urls)

        #Note: Only token_counter is used for evaluation in this version

    
    def get_normalized_counter(self):
        '''
        Returns counter where each word from the email is counted only once
        '''
        ret = Counter(self.token_counter)
        for t in ret:
            if ret[t] > 1:
                ret[t] = 1

        ret[''] = 0

        return ret


    def tokenize_payload(self, payload):
        '''
        Extracts individual words and URLs from message and returns lists of them
        Params:
        payload: email message payload as defined in Python email package
        '''
        #extract text form of the payload from messages with 
        # multipart or binary payload
        payload = self.extract_payload_text(payload)

        #Definitions of used regular expressions        
        #found the URL one online
        # https://stackoverflow.com/questions/499345/regular-expression-to-extract-url-from-an-html-link
        url_regex = r'href=[\'"]?([^\'" >]+)'        
        del_html_regex = r'<[^>]*>'
        del_non_english_regex = r'[^a-zA-Z]'
        split_regex = r'[\s.,;:]+'
        
        urls = re.findall(url_regex, payload) #extract urls from message
        payload = re.subn(del_html_regex, "", payload)[0]
        payload = re.subn(del_non_english_regex, ' ', payload)[0]
        #replace multiple whitespace chars with single space
        payload = re.subn(r'[\s]+', ' ', payload)[0]

        tokens = re.split(split_regex, payload.lower())

        return urls, tokens

    
    def extract_payload_text(self, payload):
        '''
        Recursive function to extract single text representation of multipart payloads
        Params:
        payload: email message payload as defined in Python email package
        '''        
        if isinstance(payload, str):
            return payload
        elif isinstance(payload, bytes):
            return ''
        
        payload_text = ""
        #if payload has multiple parts extract each one
        for p in payload:
            payload_text += self.extract_payload_text(p)
            payload_text += '\n'

        return payload_text

