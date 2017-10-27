import re
import nltk
import sys, getopt
from nltk.tag import pos_tag

#global variable
Q_list = ["does","did","have","has","had","Is","Are"]


#will show the past tense of the word, this is used in process_answer on the verb when printing the output
def past_tense(word):
	if word == 'drop':
		return "dropped"
	elif word == 'rise':
		return 'rose'
	elif word == 'up':
		return 'went up'
	elif word == 'down':
		return 'went down'
	elif word == 'climb':
		return 'climbed'
	elif word == 'fall':
		return "fell"
	elif word == 'open':
		return "opened"

#retrieves a list of synonyms for the words in the function otherwise returns false
def syn(word):
	rise = ["up","risen","rise","rose","climb","climbed","soar","soared"]
	drop = ["drop","fall","down","plummet","decline","plunged","fell"]
	close = ["closed","close"]
	open_word = ["open","opened"]
	if word in rise:
		return rise
	if word in drop:
		return drop
	if word in close:
		return close
	if word in open_word:
		return open_word
	else:
		return False

#returns the answer list
def process_answer(ques,Entity,Verb_list,answerlist):
	count = 0

	print "\nQ:",ques
	#answers for questions starting with "Did"
	#iterates through a list under the dictionary key value of rise/fall/close/open, whichever is mentioned in the question
	if re.match(r"^Did.*\?$",ques) :

		for key,answer in answerlist.items():
			if len(answer)>0:
				for source in answer:
					count += 1
					print("\nA%d: It %s" %(count,past_tense(key)))
					print "\nSource\n",source


	#answers for questions starting with "What" and "How much"
	#iterates through a a list of tuples to get the values and the sentences
	if re.match(r"^How\smuch.*\?$",ques) or re.match(r"^What.*\?$",ques) :
		for answer,sourcline in answerlist["value"]:
			count += 1
			print("\nA%d: %s" %(count,answer))
			print "\nSource\n",sourcline
	#If no answer is found then print below
	if count == 0:
		print "\nNo information available\n"




def find_answer(PN,VBlist,passage,question_type):
	Interest_word = str(PN[0])
	#used for paraphrase

	Interest_words = list()
	wordflag = 0
	sentence_flag = 0


	#extract paraphrases of entity
	for line in passage.split("\n"):
		if re.search("\s"+Interest_word+"\s",line,re.IGNORECASE) and sentence_flag == 0:

			captured_sentence=nltk.word_tokenize(line)

			for word, pos in pos_tag(captured_sentence):
				if wordflag == 1 and "NNP" in pos:
					Interest_words.append(word)
				elif wordflag == 0 and Interest_word.lower() in word.lower():
					Interest_words.append(word)
					wordflag = 1
				elif wordflag == 1 and "NNP" not in pos:
					break;
			sentence_flag = 1

		if sentence_flag == 1:
			break
	captured_sentence_list=list()

	answerlist=dict()
	answerlist["value"]=list()
	for verb in VBlist:
		answerlist[str(verb)]=list()

	for Entity_word in Interest_words:

		linecount = 0
		for line in passage.split("\n"):

			linecount=linecount+1
			if line not in captured_sentence_list:

				if re.search("\s"+Entity_word.lower()+"\s",line,re.IGNORECASE):
					#if the the question is a confirmation type like "did it rise or fall"
					if question_type == 1:
						for verb_word in VBlist:
							# rise fall or close whatever verb is in the verblist from the question
							#verbcase(verb_word)=list()
							for syn_word in syn(verb_word):
								#all the synonyms
								if re.search("\s"+Entity_word.lower()+"\s.*"+syn_word,line,re.IGNORECASE):
									line_and_number=line+"\n"+"(line "+str(linecount)+")"
									answerlist[str(verb_word)].append(line_and_number)
									captured_sentence_list.append(line)
									#the verb dictionary of answerlist is a list where The answers are appeneded hence 'drop' and 'rise' will have seperate lists

					#if the question asks for a quantity:
					elif question_type == 2:
						for syn_word in syn(VBlist[0]):
							found=re.search(r'\s'+Entity_word.lower()+".*"+syn_word+'\s[\D]*([\d]+(\s[\d]+\/[\d]+|\.?\d+)\%?)',line,re.IGNORECASE)
							if found:
								answerlist[str(VBlist[0])].append(line)
								line_and_number=line+"\n"+"(line "+str(linecount)+")"
								answerlist["value"].append((found.group(1),line_and_number))

								captured_sentence_list.append(line)
								#captured sentences list is appened so that the those lines of the passage are not visited again


	return answerlist
	#returns the answerlist found from the passage to the q_type

def q_type(ques,passage):
	Entity = list()
	# entity list contatining proper nouns in the question
	Verb_list = list()
	# verb list contatining proper verb in the question
	Conjunctionlist = list()
	ques=ques.strip()
	sentence_word=re.findall(r'[^ \?]+',ques)

	listp=pos_tag(sentence_word)

	for word,tag in listp:
		if "NNP" in tag:
			if word.lower() not in Q_list:
				#eliminating 'Did' since it came as a proper noun
				Entity.append(word)
				continue
		if syn(word):
			# if it matches the synonym list of rise fall and close
			Verb_list.append(word)
		if "CC" in tag:
			Conjunctionlist.append(word)


	question_type_tag = 0

	if re.match(r"^Did.*\?$",ques):
		question_type_tag = 1
	elif re.match(r"^How\smuch.*\?$",ques):
		question_type_tag = 2
	elif re.match(r"^What.*\?$",ques):
		question_type_tag = 2

	if question_type_tag != 0:
		process_answer(ques,Entity,Verb_list,find_answer(Entity,Verb_list,passage,question_type_tag))
		#calls the find_answer function to retrieve the answer list
	else:
		print "type not explored or wrong question structure"

def main(argv):
	Entity = list()
	Verb_list = list()
	#opens the passage
	passagefile = open(argv[0])
	passage = passagefile.read()
	passage = passage.strip()
	#opens the question document if it exists
	if len(argv)>1:
		questionfile = open(argv[1])
		questionList = questionfile.read()
		questionList = questionList.strip()
		for question in re.split("\n",questionList):
			q_type(question,passage)
	else:
		while True:
			user_question = raw_input("Enter a question or Enter q: ")
			if re.match(r"^[qQ]$", user_question.strip()):
				sys.exit(0)
			elif re.match(r"^.*\?$",user_question):
				q_type(user_question,passage)
			else:
				print "Try again"


if __name__ == '__main__':
	main(sys.argv[1:])
