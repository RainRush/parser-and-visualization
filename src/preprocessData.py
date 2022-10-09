import re

ID_ATTRIBUTE = "Id"
POST_TYPE_ID_ATTRIBUTE = "PostTypeId"
CREATION_DATE_ATTRIBUTE = "CreationDate"
BODY_ATTRIBUTE = "Body"

whitespaceRules = [
	{ "subFrom": "\s+", "subTo": " " }
]

removeHTMLTagRules = [
	{ "subFrom": "<.*?>", "subTo": "" }
]

removeUnneededCharRefRules = [
	{ "subFrom": "&#xA;", "subTo": " " },
	{ "subFrom": "&#xD;", "subTo": " " }
]

characterRefToOriginalFormRules = [
	{ "subFrom": "&amp;", "subTo": "&" },
	{ "subFrom": "&quot;", "subTo": "\"" },
	{ "subFrom": "&apos;", "subTo": "'" },
	{ "subFrom": "&gt;", "subTo": ">" },
	{ "subFrom": "&lt;", "subTo": "<" },
]

def applyRulesOnLine(rules, line):
	for rule in rules:
		line = re.sub(rule["subFrom"], rule["subTo"], line)
	return line

def preprocessLine(inputLine):
	preprocessedLine = getValueByAttribute(BODY_ATTRIBUTE, inputLine)
	preprocessedLine = applyRulesOnLine(characterRefToOriginalFormRules, preprocessedLine)
	preprocessedLine = applyRulesOnLine(removeUnneededCharRefRules, preprocessedLine)
	preprocessedLine = applyRulesOnLine(removeHTMLTagRules, preprocessedLine)
	preprocessedLine = applyRulesOnLine(whitespaceRules, preprocessedLine)
	return preprocessedLine

def getValueByAttribute(attribute, inputLine):
	result = re.search(f'{attribute}=\"(.*?)\"', inputLine)
	return result.group(1)

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

		postTypeId = getValueByAttribute(POST_TYPE_ID_ATTRIBUTE, line)
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
