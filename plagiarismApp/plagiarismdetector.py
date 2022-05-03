from io import StringIO
from pathlib import Path
from unicodedata import name
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import math

""" mydol = StringIO("This book is filled with practical advice, written in a\nplain, direct language. It's very relatable, and the tips\nin here are surely going to make a big difference to\nanyone who is open to changing their business and\nlife. It's an energy giving book - after reading this, I\nfelt that excitement to want to do things right now!\nAkin Alabi is without a doubt one of the foremost")

docw = mydol.readlines()

print(("docw","hhs")) """


BASE_DIR = Path(__file__).resolve().parent.parent


class Plagiarism:
    def __init__(self, documents):
        self.documents = [self.convertToText(doc) for doc in documents]
        self.docNames = tuple(obj["Name"] for obj in documents)

    def convertToText(self, file):
        output_string = StringIO()
        filePath = file["filepath"].replace("/", '\\')
        filePath = "{}{}{}".format(BASE_DIR, '\media\\', filePath)

        with open(filePath, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
            whitelist = set(
                'abcdefghijklmnopqrstuvwxyz., ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\n')
            newValue = ''.join(
                filter(whitelist.__contains__, output_string.getvalue()))
        return StringIO(newValue)

    def stemSentence(self, sentence):
        porter = PorterStemmer()
        porter.stem(sentence)
        token_words = word_tokenize(sentence)
        token_words
        stem_sentence = []
        for word in token_words:
            stem_sentence.append(porter.stem(word))
            stem_sentence.append(" ")
        return "".join(stem_sentence)

    def remove_common_word_stemming(self, main, generic):
        finaler = []
        for i in main:
            query = i
            stopwords = generic
            querywords = query.split()

            resultwords = [word for word in querywords if word.lower()
                           not in stopwords]
            result = " ".join(resultwords)
            finaler.append(self.stemSentence(result))

        return finaler

    def badCharHeuristic(self, string, size):
        NO_OF_CHARS = 256
        '''
        The preprocessing function for
        Boyer Moore's bad character heuristic
        '''

        # Initialize all occurrence as -1
        badChar = [-1]*NO_OF_CHARS

        # Fill the actual value of last occurrence
        for i in range(size):
            badChar[ord(string[i])] = i

        # return initialized list
        return badChar

    def search(self, txt, pat):
        '''
        A pattern searching function that uses Bad Character
        Heuristic of Boyer Moore Algorithm
        '''
        m = len(pat)
        n = len(txt)

        # create the bad character list by calling
        # the preprocessing function badCharHeuristic()
        # for given pattern
        badChar = self.badCharHeuristic(pat, m)

        # s is shift of the pattern with respect to text
        s = 0
        while(s <= n-m):
            j = m-1

            # Keep reducing index j of pattern while
            # characters of pattern and text are matching
            # at this shift s
            while j >= 0 and pat[j] == txt[s+j]:
                j -= 1

            # If the pattern is present at current shift,
            # then index j will become -1 after the above loop
            if j < 0:
                return 1
                '''
                    Shift the pattern so that the next character in text
                        aligns with the last occurrence of it in pattern.
                    The condition s+m < n is necessary for the case when
                    pattern occurs at the end of text
                '''
                s += (m-badChar[ord(txt[s+m])] if s+m < n else 1)
            else:
                '''
                Shift the pattern so that the bad character in text
                aligns with the last occurrence of it in pattern. The
                max function is used to make sure that we get a positive
                shift. We may get a negative shift if the last occurrence
                of bad character in pattern is on the right side of the
                current character.
                '''
                s += max(1, j-badChar[ord(txt[s+j])])
        return -1

    def CheckForPlagiarism(self):
        documents = self.documents
        docNames = self.docNames

        def chunkArr(listee):

            final = []
            for i in listee:
                t = i.split(".")
                for i in t:
                    final.append(i)
            for i in range(0, final.count("")):
                final.remove("")
            return final

        documents = [chunkArr(tuple(' '.join(line.split())
                                    for line in doc.readlines())) for doc in documents]

        common_word_list = ["do", "she", "they", "we",
                            "are", "is", "a", "an", "in", "as", "in", "of"]

        documents = [self.remove_common_word_stemming(
            doc, common_word_list) for doc in documents]

        docSize = len(documents)
        documentTobeChecked = documents[docSize-1]
        documents_joined = [
            ".".join(doc) for doc in documents[:(docSize-1 if docSize > 1 else 1)]]

        for index, current_document_joined in enumerate(documents_joined):
            count = 0
            for i in documentTobeChecked:
                checkvar = self.search(current_document_joined, i)
                if checkvar > -1:
                    count = count+1

            rate_plagiarism = (200*count) / \
                (len(documentTobeChecked)+len(documents[index]))
            # print("the matches are "+str(count))
            # print("\nThe rate of plagiarism "+str(rate_plagiarism), end="\n\n")
            yield {"rate": str(math.ceil(rate_plagiarism))+"%", "name": docNames[index]}
