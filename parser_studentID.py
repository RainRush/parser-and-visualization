import re, math
from venv import create
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
		wordsCounter = dict()

		for word in words:
			if word in wordsCounter:
				wordsCounter[word] += 1
			else:
				wordsCounter[word] = 1
		return wordsCounter

if __name__ == "__main__":
	testLine = '<row Id="1" PostTypeId="1" CreationDate="2015-09-09T16:39:07.963" Body="&lt;p&gt;My second to last laptop was a Core2Duo 2.4 GHz processor. I have recently purchased a new laptop, which has 2.5 GHz i7 processors (the new model Macbook Pro).&lt;/p&gt;&#xA;&#xA;&lt;p&gt;It it fairly obvious that a 5-year newer processor is faster. &lt;/p&gt;&#xA;&#xA;&lt;p&gt;My assumption is the processor speed has something to do with actual calculations per second, but obviously the &quot;GHz&quot; comparison is meaningless as a comparison when not comparing the same model of processor.&lt;/p&gt;&#xA;&#xA;&lt;ul&gt;&#xA;&lt;li&gt;How can I reliably or meaningfully determine the differences in performance from two processors of different models? &lt;/li&gt;&#xA;&lt;/ul&gt;&#xA;" />'
	parser = Parser(testLine)
	print(parser)
	print(parser.inputString)
	print(parser.getVocabularySize())
