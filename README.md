## DOCUMENTATION FOR THE QA System:
  NAME: ANUPAM BASU
  EMAIL: anupamb@udel.edu

  FILENAME:qa1.py
      PACKAGES USED: nltk
      libraries used in nltk: nltk.tag


# Terminaology used:
    type 1: Confirmation based question
    type 2: Quantity based question

# METHODS USED:
        q_type
            Arguments: ques, passage
            Purpose: Takes in the question from the function call and categorizes what type of question it falls under. Currently it follows sentences begining with What, How , Did.

            ****'What' and 'How' falls under the quantitative answers(type 1)****

            ****'Did' falls under the confirmation answers (type 2)****

            It also collects the Nouns(Proper Noun list or entity list) and verbs (Verb list) from the question using the pos_tag which we utilise in sending to the "find_answer" function as an argument to "process_answer" function
            return: void

        find_answer
            Arguments: PN,VBlist,passage,question_type
            Purpose: looks for answers in the passage and returns a list of ocurances of a word. It takes in the ProperNoun(PN) VBlist(verb list), the passage, and the question_type (either 1 or 2 ;see q_type function)
            Initially it will look through the passage with the first element of ProperNoun to look for a match along with the list of Proper Nouns which we will utilise for paraphrasing(used as Interest_word).
            e.g.:
                  PN[0]="Dow"
                  Interest_Words=["Dow","Jones","Industrial"]
            A dictionary in the name of "answerlist" is created to store lists under verbs in the case of type 1, and list of tuples (<value>, <sentence_where_value was found>)


            Under both types I look for sentences matching an entity under Interest_word(which is used for paraphrasing) and searching through list of synonyms under the VBlist(captured in q_type) in the arguments. Different regular expressions are used in each case.

            type 1 collects lines into a dictionary with the verb word(e.g.: fall,rise) as the key and the value as a list (a collection of answers).

            type 2 collects lines into a dictionary with the "value" as the key and the value as a list of tuples (value, <sentence_containing_value>).

            captured_sentence_list is used to not repeat the same sentences captured when searching the passage again through paraphrasing (e.g. Dow, Average).

            return: answerlist

        process_answer
            Arguments: ques,Entity,Verb_list,answerlist
            Purpose: is to process the answer looking through the answerlist for two types of questions. One will retrieve the answerlist with the verb as the key (type 1), and output the collection.
            The type 2

        syn
            Arguments: word
            Purpose: To return either a set of synonyms if the argument matches any in the list of strings for (rise,fall close,open) on request or return false.
            return: return synonyms or false

        past_tense
            Arguments: word
            Purpose: Used in tht process_answer for type 1 questions. Returns a past tense of the word for the use of output.

        Main
            Purpose: Accepts two arguments from the command line. If one argument then the user is prompted to ask a question till the user presses "q". Invalid questions will result in "Try again" .Calls the q_type function


LIMITATIONS:
  - Does not detect Pronouns
  - Answer collection might mistake a verb meant for a different Proper noun:
      e.g.
          Q: Did Dow fall?
          A: It fell
          Source:
          It was a lukewarm performance in Dow, while S&P had a steep fall.


REASON WHY I COULD NOT RUN MY FILE IN THE VM IN HOEK:


Below is the error message which occurs on downloading nltk library essential for my program in the vm provided

***************************************************************************************************************
                                          ERROR MESSAGE
***************************************************************************************************************

>>> import nltk
>>> nltk.download()
NLTK Downloader
---------------------------------------------------------------------------
    d) Download      l) List      c) Config      h) Help      q) Quit
---------------------------------------------------------------------------
Downloader> c

Data Server:
  - URL: <http://nltk.googlecode.com/svn/trunk/nltk_data/index.xml>
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python2.7/dist-packages/nltk/downloader.py", line 644, in download
    self._interactive_download()
  File "/usr/lib/python2.7/dist-packages/nltk/downloader.py", line 962, in _interactive_download
    DownloaderShell(self).run()
  File "/usr/lib/python2.7/dist-packages/nltk/downloader.py", line 996, in run
    self._simple_interactive_config()
  File "/usr/lib/python2.7/dist-packages/nltk/downloader.py", line 1049, in _simple_interactive_config
    self._show_config()
  File "/usr/lib/python2.7/dist-packages/nltk/downloader.py", line 1041, in _show_config
    len(self._ds.collections()))
  File "/usr/lib/python2.7/dist-packages/nltk/downloader.py", line 489, in collections
    self._update_index()
  File "/usr/lib/python2.7/dist-packages/nltk/downloader.py", line 814, in _update_index
    ElementTree.parse(urllib2.urlopen(self._url)).getroot())
  File "/usr/lib/python2.7/dist-packages/nltk/etree/ElementTree.py", line 862, in parse
    tree.parse(source, parser)
  File "/usr/lib/python2.7/dist-packages/nltk/etree/ElementTree.py", line 586, in parse
    parser.feed(data)
  File "/usr/lib/python2.7/dist-packages/nltk/etree/ElementTree.py", line 1245, in feed
    self._parser.Parse(data, 0)
xml.parsers.expat.ExpatError: mismatched tag: line 5, column 4
```
