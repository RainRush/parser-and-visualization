import re, math
from preprocessData_studentID import preprocessLine, getValueByAttribute, ID_ATTRIBUTE, CREATION_DATE_ATTRIBUTE, POST_TYPE_ID_ATTRIBUTE

QUESTION_POST_TYPE = "question"
ANSWER_POST_TYPE = "answer"
OTHER_POST_TYPE = "other"

class Parser:
	"""docstring for ClassName"""
	def __init__(self, inputString):
		self.inputString = inputString
		self.ID = self.getID()
		self.type = self.getPostType()
		self.dateQuarter = self.getDateQuarter()
		self.cleanBody = self.getCleanedBody()

	def __str__(self):
		return f"{self.ID}, {self.type}, {self.dateQuarter}, {self.cleanBody}"

	def getID(self):
		return getValueByAttribute(ID_ATTRIBUTE, self.inputString)
		
	def getPostType(self):
		postTypeId = getValueByAttribute(POST_TYPE_ID_ATTRIBUTE, self.inputString)
		if (postTypeId == "1"):
			return QUESTION_POST_TYPE
		if (postTypeId == "2"):
			return ANSWER_POST_TYPE
		return OTHER_POST_TYPE

	def getDateQuarter(self):
		creationDate = getValueByAttribute(CREATION_DATE_ATTRIBUTE, self.inputString)
		creationDateResult = re.search("([0-9]{4})-([0-9]{2})-([0-9]{2})T*", creationDate)
		year = creationDateResult.group(1)
		month = creationDateResult.group(2)
		quarter = f"Q{math.floor(int(month) / 4) + 1}"
		return f"{year}{quarter}"

	def getCleanedBody(self):
		return preprocessLine(self.inputString)
		
	def getVocabularySize(self):
		# [^\d.\d] 2.4 will become 24
		words = re.sub(r'[^\w\s]', '', self.cleanBody).lower().split(' ')
		wordsSet = set()
		for word in words:
			wordsSet.add(word)
		vocabularySize = len(wordsSet)
		return vocabularySize
