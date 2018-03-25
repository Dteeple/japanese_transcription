# japanese_transcription
Provides phonetic transcriptions for Japanese text (not intended for public consumption, just a skill test)

Sources employed:
1.  http://memory.loc.gov/diglib/codetables/9.2.html (for creating kana transcription table)
2.  Consulted https://en.wikipedia.org/wiki/Japanese_numerals in creating numeral_grammar.py
3.  https://github.com/Doublevil/JmdictFurigana/tree/master/JmdictFurigana/Resources/JMdict.xml (large kanji dictionary)

Dictionary (source 3) will be fetched and converted to JSON format at runtime

To run:

> python3 transcribe.py

Takes the file /input/tokens.tsv as input.

Will output a TSV file with token type (word/numeral), token to be transcribed, transcription in a semi-standard (partially Hepburn/Nihon-shiki) romanization system, and source of the transcription (dictionary or numeral grammar, for example).

I've added a tiny Romaji dictionary to cover a few illustrative words, like "Sony", but this is definitely a corner I cut.  The real Romaji dictionary would need to be much larger.

There is some inconsistency in transcription:  syllable-final nasals are represented by <N'> in dictionary transcriptions, but by <N> in numeral grammar transcriptions.  It could be remedied, but I'm cutting a corner for now.
  
Numerals are treated differently, depending on whether they're Sino-Japanese characters meant to be read as native Japanese ('kun'), borrowed Chinese ('on'), or Arabic numerals.  I'm certain some of this is wrong, since the numeral system is very complex.
  
 
