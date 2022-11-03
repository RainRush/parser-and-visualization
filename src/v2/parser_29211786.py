from preprocessData_29211786 import preprocessLine
import re, math

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
		# get and return value of Id
		ID_ATTRIBUTE = "Id"
		return re.search(f'{ID_ATTRIBUTE}=\"(.*?)\"', self.inputString).group(1)

	def getPostType(self):
		# get value of PostTypeId
		POST_TYPE_ID_ATTRIBUTE = "PostTypeId"
		post_type_id = re.search(f'{POST_TYPE_ID_ATTRIBUTE}=\"(.*?)\"', self.inputString).group(1)
		if (post_type_id == "1"):
			return "question"
		if (post_type_id == "2"):
			return "answer"
		return "other"

	def getDateQuarter(self):
		# get value of creation date
		CREATION_DATE_ATTRIBUTE = "CreationDate"
		creation_date = re.search(f'{CREATION_DATE_ATTRIBUTE}=\"(.*?)\"', self.inputString).group(1)

		# search and set year / month / day in group 1 / 2 / 3
		creation_date_result = re.search("([0-9]{4})-([0-9]{2})-([0-9]{2})T*", creation_date)
		year = creation_date_result.group(1)
		month = creation_date_result.group(2)

		# convert month into quarter
		quarter = f"Q{math.floor((int(month) - 1) / 3) + 1}"

		return f"{year}{quarter}"

	def getCleanedBody(self):
		# find body
		BODY_ATTRIBUTE = "Body"
		body = re.search(f'{BODY_ATTRIBUTE}=\"(.*?)\"', self.inputString).group(1)
		return preprocessLine(body)

	def getVocabularySize(self):
		words = re.sub(r'[^\w\s]', '', self.cleanBody).lower().split(' ')
		# choice of data structure: set - for distinct value
		words_set = set()
		for word in words:
			words_set.add(word)
		return len(words_set)
