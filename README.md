# japanese_transcription
Provides phonetic transcriptions for Japanese text (not intended for public consumption, just a skill test)

Sources employed:
1.  http://memory.loc.gov/diglib/codetables/9.2.html (for creating kana transcription table)
2.  Consulted https://en.wikipedia.org/wiki/Japanese_numerals in creating numeral_grammar.py
3.  https://github.com/Doublevil/JmdictFurigana/tree/master/JmdictFurigana/Resources/JMdict.xml (large kanji dictionary)
4.  http://ftp.monash.edu/pub/nihongo/edict2u.gz (smaller dictionary)

Dictionaries (sources 3 and 4) will be fetched and converted to JSON format at runtime.  You'll need to have git-repo installed and configured first.

To run:

> python3 transcribe.py

Takes the file /input/tokens.tsv as input.  The required format is two columns, where the first column gives the type of data (word vs. num) and the second column is a space-separated string of tokens to be transcribed.

Will output a TSV file with token type (word/numeral), token to be transcribed, transcription in a semi-standard (partially Hepburn/Nihon-shiki) romanization system, and source of the transcription (dictionary or numeral grammar, for example).

