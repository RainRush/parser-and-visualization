import re

POST_TYPE_ID_ATTRIBUTE = "PostTypeId"
BODY_ATTRIBUTE = "Body"

def trancateWhitespace(line):
	line = re.sub("\s+", " ", line)
	return line

def removeHTMLTags(line):
	line = re.sub("<.*?>", "", line)
	return line

def removeUnneededCharRef(line):
	line = re.sub("&#xA;", " ", line)
	line = re.sub("&#xD;", " ", line)
	return line

def convertCharRefToOriginalForm(line):
	line = re.sub("&amp;", "&", line)
	line = re.sub("&quot;", "\"", line)
	line = re.sub("&apos;", "'", line)
	line = re.sub("&gt;", ">", line)
	line = re.sub("&lt;", "<", line)
	return line

def preprocessLine(inputLine):
	bodyValueSearchResult = re.search(f'{BODY_ATTRIBUTE}=\"(.*?)\"', inputLine)
	preprocessedLine = bodyValueSearchResult.group(1)
	preprocessedLine = convertCharRefToOriginalForm(preprocessedLine)
	preprocessedLine = removeUnneededCharRef(preprocessedLine)
	preprocessedLine = removeHTMLTags(preprocessedLine)
	preprocessedLine = trancateWhitespace(preprocessedLine)
	return preprocessedLine

def getPostTypeId(inputLine):
	postTypeIdSearchResult = re.search(f'{POST_TYPE_ID_ATTRIBUTE}=\"(.*?)\"', inputLine)
	return postTypeIdSearchResult.group(1)

def writeLineToFile(outputFile, line):
	with open(outputFile, 'a', encoding='utf-8') as fileToWrite:
		fileToWrite.write(f"{line}\n")

def resetOutputFiles(outputFiles):
	for outputFile in outputFiles:
		with open(outputFile, 'w') as _:
			pass

def splitFile(inputFile, outputFile_question, outputFile_answer):
	resetOutputFiles([outputFile_question, outputFile_answer])
	file = open(inputFile, 'r')

	for line in file:
		if (POST_TYPE_ID_ATTRIBUTE not in line or BODY_ATTRIBUTE not in line):
			continue
		
		preprocessedLine = preprocessLine(line)
		if (preprocessedLine == ""):
			continue

		postTypeId = getPostTypeId(line)
		if (postTypeId == "1"):
			writeLineToFile(outputFile_question, preprocessedLine)
		if (postTypeId == "2"):
			writeLineToFile(outputFile_answer, preprocessedLine)
		
	file.close()

if __name__ == "__main__":

	f_data = "data.xml"
	f_question = "question.txt"
	f_answer = "answer.txt"

	splitFile(f_data, f_question, f_answer)
