from parser_studentID import Parser
import matplotlib.pyplot as plt
from preprocessData_studentID import POST_TYPE_ID_ATTRIBUTE, BODY_ATTRIBUTE, ID_ATTRIBUTE, CREATION_DATE_ATTRIBUTE
import math

def incrementCounterByKey(counter, key):
	if key in counter:
		counter[key] += 1
	else:
		counter[key] = 1
	return counter

def visualizeWordDistribution(inputFile, outputImage):
	file = open(inputFile, 'r')
	fileWordCounter = dict()
	for line in file:
		if (POST_TYPE_ID_ATTRIBUTE not in line or BODY_ATTRIBUTE not in line or ID_ATTRIBUTE not in line or CREATION_DATE_ATTRIBUTE not in line):
			continue
		parser = Parser(line)
		vocabularySize = parser.getVocabularySize()
		if (vocabularySize >= 100):
			vocabularySizeSection = 10
		else:
			vocabularySizeSection = math.floor(vocabularySize / 10)
		incrementCounterByKey(fileWordCounter, vocabularySizeSection)

	sectionCounts = []
	for section in range(0, 11):
		sectionCounts.append(fileWordCounter[section])

	_, ax = plt.subplots()
	# should have a smarter way to represent
	sectionGroups = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', 'Others']
	barRect = ax.bar(sectionGroups, sectionCounts)

	ax.set_xlabel('Vocabulary Size of File')
	ax.set_ylabel('File Count')
	ax.bar_label(barRect, padding=3)

	plt.savefig(outputImage)


def visualizePostNumberTrend(inputFile, outputImage):
	file = open(inputFile, 'r')
	quarterAnswerCounter = dict()
	quarterQuestionCounter = dict()
	for line in file:
		if (POST_TYPE_ID_ATTRIBUTE not in line or BODY_ATTRIBUTE not in line or ID_ATTRIBUTE not in line or CREATION_DATE_ATTRIBUTE not in line):
			continue
		parser = Parser(line)
		quarter = parser.dateQuarter
		if (parser.type == 'question'):
			incrementCounterByKey(quarterAnswerCounter, quarter)
		if (parser.type == 'answer'):
			incrementCounterByKey(quarterQuestionCounter, quarter)

	quarterAnswerCounts = []
	quarterQuestionCounts = []
	quarters = []
	for quarterAnswerKey, quarterAnswerCount in sorted(quarterAnswerCounter.items()):
		quarterAnswerCounts.append(quarterAnswerCount)
		quarters.append(quarterAnswerKey)
	for _, quarterQuestionCount in sorted(quarterQuestionCounter.items()):
		quarterQuestionCounts.append(quarterQuestionCount)

	_, ax = plt.subplots()
	print(quarterAnswerCount)
	ax.plot(quarters, quarterAnswerCounts, label="Answers")
	ax.plot(quarters, quarterQuestionCounts, label="Questions")
	ax.legend()

	plt.savefig(outputImage)

if __name__ == "__main__":

	f_data = "data.xml"
	f_wordDistribution = "wordNumberDistribution.png"
	f_postTrend = "postNumberTrend.png"
	
	visualizeWordDistribution(f_data, f_wordDistribution)
	visualizePostNumberTrend(f_data, f_postTrend)
