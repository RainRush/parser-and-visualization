import re

def preprocessLine(inputLine):
	# setup rules based on phases
	# defined substitute from and substitute to, 
	# to be executed with re.sub
	whitespace_rules = [
		{ "subFrom": "\s+", "subTo": " " }
	]

	remove_HTML_tag_rules = [
		{ "subFrom": "<.*?>", "subTo": "" }
	]

	remove_unneeded_char_ref_rules = [
		{ "subFrom": "&#xA;", "subTo": " " },
		{ "subFrom": "&#xD;", "subTo": " " }
	]

	character_ref_to_original_form_rules = [
		{ "subFrom": "&amp;", "subTo": "&" },
		{ "subFrom": "&quot;", "subTo": "\"" },
		{ "subFrom": "&apos;", "subTo": "'" },
		{ "subFrom": "&gt;", "subTo": ">" },
		{ "subFrom": "&lt;", "subTo": "<" },
	]
	
	# merge the rules based on phases
	transformation_rules = character_ref_to_original_form_rules\
		+ remove_unneeded_char_ref_rules\
		+ remove_HTML_tag_rules\
		+ whitespace_rules

	preprocessed_line = inputLine
	# loop through all data transformation rules
	for rule in transformation_rules:
		preprocessed_line = re.sub(rule["subFrom"], rule["subTo"], preprocessed_line)
	
	return preprocessed_line



def splitFile(inputFile, outputFile_question, outputFile_answer):
	output_files = [outputFile_question, outputFile_answer]
	# reset / clean up output files
	for output_file in output_files:
		with open(output_file, 'w') as _:
			pass

	POST_TYPE_ID_ATTRIBUTE = "PostTypeId"
	BODY_ATTRIBUTE = "Body"

	for line in open(inputFile, 'r'):
		# skip lines without PostTypeId or without Body
		if (POST_TYPE_ID_ATTRIBUTE not in line or BODY_ATTRIBUTE not in line):
			continue

		# find body
		body_search_result = re.search(f'{BODY_ATTRIBUTE}=\"(.*?)\"', line)
		body = body_search_result.group(1)

		preprocessed_line = preprocessLine(body)
		# safeguarding the output file by dropping empty data
		if (preprocessed_line == ""):
			continue

		# find post type id
		post_type_id_search_result = re.search(f'{POST_TYPE_ID_ATTRIBUTE}=\"(.*?)\"', line)
		post_type_id = post_type_id_search_result.group(1)

		# get the file to output into by post_type_id
		output_file = ''
		if (post_type_id == "1"):
			output_file = outputFile_question
		elif (post_type_id == "2"):
			output_file = outputFile_answer
		# if the post type id is not supported above, drop this line
		else:
			continue

		# write processed line to file
		with open(output_file, 'a', encoding='utf-8') as file_to_write:
			file_to_write.write(f"{preprocessed_line}\n")
	


if __name__ == "__main__":

	f_data = "data.xml"
	f_question = "question.txt"
	f_answer = "answer.txt"

	splitFile(f_data, f_question, f_answer)
