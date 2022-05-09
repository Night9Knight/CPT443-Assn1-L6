# CPT443-Assn1-L6
A simple DFA application written in Python which could match a list of adverbs (up to what is covered in WordNet)

## Requirements
Write a well-structured, well-documented recognizer Deterministic Finite Automata (DFA) for the
assigned language. The program must be based on a complete DFA for the language, but you can
terminate the program on entering a trap state. You MUST process one character at a time from left
to right simulating a finite state machine. No other strategy for your program is allowed.
Each student will be given a different language to search for. For program development, a text file will
be given as example for implementation and testing. During the demonstration day, you may use the
given sample text or new text file to demo your machine.
For demonstration purpose, the output from the run must show the following:
 The pattern (input string).
The text used for demo.
The status (whether accept/reject).
Additional information (the position of the pattern found, occurrences of patterns, visualization using
boldface of the pattern occurred in the text etc.). 

Σ = { a,..z, A,..Z, 0,…9, and other symbols found the sample text}
Example languages
L = {w ∈ Σ * | w contain substring “Malaysia”, “Kuala Lumpur”, “Penang” ...}
L = {w ∈ Σ * | w contain substring “2 litres”, “1kg”, “100%” ...} 

L6. English Conjunctions/Adverb/Adjectives Finder
Example: and, most, good, bad, pretty, dirty, blue etc. 

## How to run
```
<FolderPath>/Scripts/python.exe main.py
```
