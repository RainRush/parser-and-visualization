# Parser And Data Visualization

### To Run

- Confirm that `matplotlib` had been installed in the environment
- `$ python3 ./src/preprocessData.py` to generate a full list of preprocessed questions and answers within `question.txt` and `answer.txt`
- `$ python3 ./src/dataVisualization.py` to process data and create visualization images in `postNumberTrend.png` and `wordNumberDistribution.png`

### To Do

- Add `requirements.txt` and script for setup
- Improve `parser.py` `getVocabularySize()` to be more accurate on picking out unique word
- Refactor `dataVisualization.py`
  - Smarter way on getting `sectionGroups`
