from parser_29211786 import Parser
import matplotlib.pyplot as plt
import math

def visualizeWordDistribution(inputFile, outputImage):
	ID_ATTRIBUTE = "Id"
	POST_TYPE_ID_ATTRIBUTE = "PostTypeId"
	CREATION_DATE_ATTRIBUTE = "CreationDate"
	BODY_ATTRIBUTE = "Body"

	try:
		file_word_counter = dict()
		file = open(inputFile, 'r')
		for line in file:
			if (POST_TYPE_ID_ATTRIBUTE not in line or BODY_ATTRIBUTE not in line or ID_ATTRIBUTE not in line or CREATION_DATE_ATTRIBUTE not in line):
				continue
			parser = Parser(line)
			vocabulary_size = parser.getVocabularySize()
			# 0-9 to be section 0, 10-19 to be section 1, etc
			vocabulary_size_section = math.floor((vocabulary_size) / 10)
			# vocabulary size > 10, set to 10 as others
			if vocabulary_size_section > 10:
				vocabulary_size_section = 10
			if vocabulary_size_section not in file_word_counter:
				file_word_counter[vocabulary_size_section] = 0
			file_word_counter[vocabulary_size_section] += 1
			
		section_counts = []
		for section in range(0, 11):
			section_counts.append(file_word_counter[section])

		_, ax = plt.subplots()
		section_groups = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', 'Others']
		barRect = ax.bar(section_groups, section_counts)

		ax.set_xlabel('Vocabulary Size of Posts')
		ax.set_ylabel('Post Count')
		ax.bar_label(barRect, padding=3)

		plt.savefig(outputImage)
	except Exception as e:
		print(e)


def visualizePostNumberTrend(inputFile, outputImage):
	ID_ATTRIBUTE = "Id"
	POST_TYPE_ID_ATTRIBUTE = "PostTypeId"
	CREATION_DATE_ATTRIBUTE = "CreationDate"
	BODY_ATTRIBUTE = "Body"
	ANSWER_POST_TYPE = "answer"
	QUESTION_POST_TYPE = "question"
	QUESTION_COLOR = "green"
	ANSWER_COLOR = "red"

	try:
		file = open(inputFile, 'r')
		# choice of data structure: dictionary -
		# for key-value pairs where keys to be Quarter of each Year
		# and value to be the number of posts
		# { QUARTER: { ANSWER: count, QUESTION: count } }
		# e.g. { "2020Q1": { "answer": 12, "question": 11 }, "2020Q2": { "answer": 0, "question": 1 } }
		quarter_counter = dict()

		for line in file:
			if (POST_TYPE_ID_ATTRIBUTE not in line or BODY_ATTRIBUTE not in line or ID_ATTRIBUTE not in line or CREATION_DATE_ATTRIBUTE not in line):
				continue
			parser = Parser(line)
			quarter = parser.dateQuarter
			# non-supported post type, will pass this line
			if (parser.type != QUESTION_POST_TYPE and parser.type != ANSWER_POST_TYPE):
				continue

			if quarter not in quarter_counter:
				# initiate the question-answer dictionary for the first seen quarter
				quarter_counter[quarter] = { QUESTION_POST_TYPE: 0, ANSWER_POST_TYPE: 0 }

			quarter_counter[quarter][parser.type] += 1

		_, ax = plt.subplots(figsize=(15, 10))
		ax.set_xlabel("Quarter")
		ax.set_ylabel("Number of Posts")

		quarter_question_counts = []
		quarter_answer_counts = []
		quarters = []

		for quarter_key, quarter_count in sorted(quarter_counter.items()):
			quarter_question_count = quarter_count[QUESTION_POST_TYPE]
			quarter_answer_count = quarter_count[ANSWER_POST_TYPE]

			# add annotations to the graph
			ax.text(quarter_key, quarter_question_count, quarter_question_count,\
				size=12, color=QUESTION_COLOR, va="top", ha="right")
			ax.text(quarter_key, quarter_answer_count, quarter_answer_count,\
				size=12, color=ANSWER_COLOR, va="bottom", ha="left")

			quarters.append(quarter_key)
			quarter_question_counts.append(quarter_question_count)
			quarter_answer_counts.append(quarter_answer_count)

		ax.plot(quarters, quarter_question_counts, label="Questions", color=QUESTION_COLOR, marker="o")
		ax.plot(quarters, quarter_answer_counts, label="Answers", color=ANSWER_COLOR, marker="o")
		ax.legend()

		plt.savefig(outputImage)
	except Exception as e:
		print(e)



if __name__ == "__main__":
	f_data = "data.xml"
	f_wordDistribution = "wordNumberDistribution.png"
	f_postTrend = "postNumberTrend.png"
	
	visualizeWordDistribution(f_data, f_wordDistribution)
	# visualizePostNumberTrend(f_data, f_postTrend)
