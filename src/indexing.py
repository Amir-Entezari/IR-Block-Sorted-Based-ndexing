import json
import os

import nltk
import string
from typing import List

from src.utils import gamma_code_to_list, list_to_gamma_code


class Token:
    def __init__(self, word: str):
        self.word = word
        self.docs = []

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word


class InvertedIndex:
    """
    In this class, I implement an information retrieval system which can search a query among documents.
    ...
    Attributes:
    -----------
    documents: List
        list of documents in format of string.
    posting_list: List[Token]
        list of Token objects. Tokens store a string and document's indexes
    stop_word: set
        set of stop words to check when tokenizing
    case_sensitive: bool
        a boolean to determine whether we want to distinguish between lowercase and uppercase form.

    Methods
    -------
    Methods defined here:
        __init__(self, documents: List, case_sensitive=False):
            Constructor will set initial attributes like documents and case_sensitive. NOTE that documents should be
            list of strings at first.
            :parameter
            ---------
            documents:List
                list of strings at first. but then chagnes to list of lists of strings
            :return
                None
        tokenize_document(self, document, use_nltk=False):
            in this function, we tokenize a documents. if use_nltk=True, we tokenize using nltk library. if
            case_sensitive has been set to True, we lower all tokens.
            :parameter
            ---------
                document: str
                use_nltk: bool, Optional
            :return
            -------
                None
        create_posting_list(self):
            calling this function, will create posting list of all occurred words cross all documents. in this function,
            we use BSBI algorithm, we read batch of documents from disk and create multiple posting_list with that
            batch size and save them on disk. In the end, we merge all these batch posting lists. Clearly, in this
            implementation we use less RAM because we don't read all documents at once.
            :parameter
                None
            :return
                None
        get_token_index(self, x):
            this function finds index of a word in posting list using binary search algorithm.
            :parameter
                x:str
                    the word you want to find its index
            :return
                int: index of the word in posting_list
        get_token(self, token):
                This function will return the token object that contains docs information. if the given token is not in the
                posting_list, it returns the spell corrected token.
                :param token:
                    token you want to fetch it from posting list
                :return:
                    return the instance of token from posting list
        get_word_docs(self, word: str):
            this simple function gets a token and will return all indexes of documents that this token is appeared in.
            :param word:
                a word that you want to search.
            :return:
                list of indexes of documents.
        intersect(self, first_word, second_word):
            this function gets two words, and finds documents that both of these words has been occurred.
            :parameter
            first_word: str
                first word you want to search
            second_word: str
                second word you want to search
            :return
                list of indexes of documents.
        union(self, first_word, second_word):
            this function get two words, and find documents that either each of these words has been occurred.
            :parameter
            first_word: str
                first word you want to search
            second_word: str
                second word you want to search
            :return
                list of indexes of documents.
        not_in(self, word):
            this function get one word, and find documents that this word has been not occurred.
            :parameter
            word: str
                the word you want to search
            :return
                list of indexes of documents.
        search(self, query):
            this function get a query and recognize what kind of query is; then search the query.
            :parameter
                query: str
                    the query that user wants to search
            :return
                print list of indexes of documents in a pretty way.

    """

    def __init__(self, case_sensitive=False):
        """
        Constructor will set initial attributes like documents and case_sensitive. NOTE that documents should be
            list of strings at first.
            :parameter
            ---------
            documents:List
                list of strings at first. but then changes to list of lists of strings
            :return
                None
        """
        self.document_paths: List = []
        self.posting_list: List[Token] = []
        self.stop_words: set = set(nltk.corpus.stopwords.words('english') + list(string.punctuation))
        self.case_sensitive = case_sensitive

    def get_document_paths(self, path=os.getcwd()):
        for filename in sorted(os.listdir(path)):
            filepath = os.path.join(path, filename)
            if filepath.endswith('.txt'):
                # Use encoding cp1252 for test cases if an error raised
                self.document_paths.append(filepath)
        return self.document_paths

    def tokenize_document(self, document, use_nltk=False):
        """
        in this function, we tokenize each documents. if use_nltk=True, we tokenize using nltk library. if
            case_sensitive has been set to True, we lower all tokens.
            :parameter
            ---------
                use_nltk: bool, Optional
            :return
            -------
                None
        """
        if use_nltk:
            tokenized_doc = []
            for token in nltk.tokenize.word_tokenize(document):
                if token not in self.stop_words:
                    tokenized_doc.append(token if self.case_sensitive == True else token.lower())
            document = tokenized_doc
            return document
        else:
            document = document.split()
            return document

    def create_posting_list(self, batch_size=1, use_nltk=True):
        """
        calling this function, will create posting list of all occurred words cross all documents. in this function, we
        loop over all documents_path and read numbers of them(with batch size), then inside this loop, we loop over all
        the tokens that are in the current document. then we check if the length of posting_list is zero, then we add
        this token as first word. else if the length of posting_list is more than 0, we find the correct index of the
        token in posting_list alphabetically. then we check if this token, has been already in posting_list, we just add
        the current document index in tokens.docs, else, we add this token in the posting_list, then add the current
        document index. And when all documents have been indexed and the batch posting lists are saved, we read them from
        disk and merge them into main posting list.
            :parameter
                None
            :return
                None
        :return:
        """
        temp_posting_list = []
        for doc_idx in range(len(self.document_paths)):
            if doc_idx % batch_size == 0:
                temp_posting_list = []
            doc_path = self.document_paths[doc_idx]
            doc = open(doc_path, encoding='cp1252').read()
            doc = self.tokenize_document(doc, use_nltk=use_nltk)
            batch_idx = doc_idx // batch_size
            for token in doc:
                if temp_posting_list == 0:
                    temp_posting_list.append(Token(token))
                    temp_posting_list[0].docs.append(doc_idx)
                    continue
                i = 0
                while i < len(temp_posting_list) and token > temp_posting_list[i].word:
                    i += 1
                if i == len(temp_posting_list):
                    temp_posting_list.append(Token(token))
                    # self.posting_list[i].post_idx.append(post_idx)
                elif token != temp_posting_list[i].word:
                    temp_posting_list.insert(i, Token(token))

                if doc_idx not in temp_posting_list[i].docs:
                    temp_posting_list[i].docs.append(doc_idx)

            if (doc_idx + 1) % batch_size == 0:
                self.posting_list_to_json(temp_posting_list, path=f"posting_lists/{batch_idx}.json")
        self.posting_list_to_json(temp_posting_list, path=f"posting_lists/{batch_idx}.json")

        path = os.path.join(os.getcwd(), 'posting_lists')
        batch_posting_lists = []
        for filename in sorted(os.listdir(path)):
            filepath = os.path.join(path, filename)
            if filepath.endswith('.json'):
                # Use encoding cp1252 for test cases if an error raised
                batch_posting_lists.append(filepath)
        curr_merge_posting_list = self.json_to_posting_list(batch_posting_lists[0])
        for i in range(len(batch_posting_lists) - 1):
            temp_posting_list = self.json_to_posting_list(batch_posting_lists[i + 1])
            curr_merge_posting_list = self.merge_two_posting_list(curr_merge_posting_list,
                                                                  temp_posting_list)
        self.posting_list = curr_merge_posting_list
        # for token in self.posting_list:
        #     token.docs = list_to_gamma_code(token.docs)

    def posting_list_to_json(self, posting_list, path):
        json_posting_list = {}
        for token in posting_list:
            json_posting_list[token.word] = token.docs
        with open(path, "w") as outfile:
            json.dump(json_posting_list, outfile)
        return json_posting_list

    def json_to_posting_list(self, path):
        with open(path, 'r') as openfile:
            json_object = json.load(openfile)
            posting_list = []
            for word, docs in json_object.items():
                token = Token(word)
                token.docs = docs
                posting_list.append(token)
            return posting_list

    def merge_two_posting_list(self, posting_list_1: List[Token], posting_list_2: List[Token]):
        """
        In this function we merge two posting list. If posting lists contain tokens that their docs attribute is a str,
        we should first convert their docs to list of numbers, then merge them and at last, we convert their docs to
        gamma code.
        :param posting_list_1: First posting list we want to merge
        :param posting_list_2: Second posting list we want to merge
        :return:
            returns a merged posting list of first and second posting list.
        """
        merged_posting_list = posting_list_1
        if type(posting_list_1[0].docs) != list:
            for token in posting_list_1:
                token.docs = gamma_code_to_list(token.docs)
        if type(posting_list_2[0].docs) != list:
            for token in posting_list_2:
                token.docs = gamma_code_to_list(token.docs)
        for token in posting_list_2:

            low = 0
            high = len(merged_posting_list) - 1
            idx = 0
            while low <= high:
                idx = (high + low) // 2
                if merged_posting_list[idx].word < token.word:
                    low = idx + 1
                elif merged_posting_list[idx].word > token.word:
                    high = idx - 1
                else:
                    break
            if token.word == merged_posting_list[idx].word:
                for doc in token.docs:
                    if doc not in merged_posting_list[idx].docs:
                        merged_posting_list[idx].docs.append(doc)
            else:
                merged_posting_list.insert(idx, token)
        if type(posting_list_2[0].docs) == list:
            for token in posting_list_1:
                token.docs = list_to_gamma_code(token.docs)
        return merged_posting_list

    def get_token_index(self, x, posting_list=None):
        """
        this function find index of a word in posting list using binary search algorithm.
            :parameter
                x:str
                    the word you want to find its index
            :return
                int: index of the word in posting_list
        """
        if not posting_list:
            posting_list = self.posting_list
        low = 0
        high = len(posting_list) - 1
        mid = 0
        while low <= high:
            mid = (high + low) // 2
            if posting_list[mid].word < x:
                low = mid + 1
            elif posting_list[mid].word > x:
                high = mid - 1
            else:
                return mid
        return -1

    def get_token(self, token):
        """
        This function will return the token object that contains docs informations. if the given token is not in the
        posting_list, it return the spell corrected token.
        :param token:
            token you want to fetch it from posting list
        :return:
            return the instance of token from posting list
        """
        p = self.get_token_index(token)
        if p == -1:
            null_token = Token('token')
            null_token.docs = []
            return null_token
        return self.posting_list[p]


nltk.download('punkt')
nltk.download('stopwords')
