# Parser And Data Visualization

### To Run

- Confirm that `matplotlib` had been installed in the environment
- `$ python3 ./src/preprocessData.py` to generate a full list of preprocessed questions and answers within `question.txt` and `answer.txt`
- `$ python3 ./src/dataVisualization.py` to process data and create visualization images in `postNumberTrend.png` and `wordNumberDistribution.png`

### To Do

- Add `requirements.txt` and script for setup
- Improve `parser.py` `getVocabularySize()` to be more accurate on picking out unique words
- Confirm if `math` module is allowed to import. If not, use `numpy` to get floor
- Refactor `dataVisualization.py`
  - Smarter way on getting `sectionGroups`
  - Can answer and question counters merge into one and use tuple / object?
  - Can the x-axis of post number trend be clearer?
  - Refactor the part where the counters were looped through and data appended into the list
