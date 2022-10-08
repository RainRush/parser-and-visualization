import re

POST_TYPE_ID_ATTRIBUTE = "PostTypeId"
BODY_ATTRIBUTE = "Body"

def preprocessLine(inputLine):
	postTypeIdSearchResult = re.search(f'{BODY_ATTRIBUTE}=\"(.*?)\"', inputLine)
	preprocessedLine = postTypeIdSearchResult.group(1)
	return preprocessedLine

def getPostTypeId(inputLine):
	postTypeIdSearchResult = re.search(f'{POST_TYPE_ID_ATTRIBUTE}=\"(.*?)\"', inputLine)
	return postTypeIdSearchResult.group(1)

def writeLineToFile(outputFile, line):
	with open(outputFile, 'a', encoding='utf-8') as fileToWrite:
		fileToWrite.write(f"{line}\n")

def splitFile(inputFile, outputFile_question, outputFile_answer):
	file = open(inputFile, 'r')
	# to delete
	lineCursor = 0
	for line in file:
		if (POST_TYPE_ID_ATTRIBUTE not in line or BODY_ATTRIBUTE not in line):
			continue
		# hold this line for test purpose, lineCursor to be removed
		if (lineCursor < 5):
			preprocessedLine = preprocessLine(line)
			postTypeId = getPostTypeId(line)

			if (postTypeId == "1"):
				writeLineToFile(outputFile_question, preprocessedLine)
			if (postTypeId == "2"):
				writeLineToFile(outputFile_answer, preprocessedLine)
		lineCursor += 1
	file.close()

if __name__ == "__main__":

	f_data = "data.xml"
	f_question = "question.txt"
	f_answer = "answer.txt"

	splitFile(f_data, f_question, f_answer)
