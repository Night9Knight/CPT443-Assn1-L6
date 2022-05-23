import json
import graphviz
import re

class DFA:
    def __init__(self):
        self.transition_dict = {}
        self.start_state = '<s>'
        self.accept_states = []
        with open('advs_transitions.json') as json_file:
            self.transition_dict = json.load(json_file)
        
        with open('adverbs.txt') as f:
            self.accept_states = f.readlines()
            self.accept_states = [state.strip() for state in self.accept_states]
    
    def __formatInputString(self, input):
        # Get list of adverbs with multiwords
        with open('adverbs_multiwords.txt') as f:
            multiwords = f.readlines()
            multiwords = [word.strip() for word in multiwords]
        
        # Replace multiwords adverbs in input string with proper format
        for word in multiwords:
            input = re.sub(word.replace('_',' '), word, input, flags=re.IGNORECASE)
        
        return input
    
    # Not used in the main text matching function
    def __formatWord(self, word):
        # Remove dot (.) symbols which is not part of a word
        word = re.sub(r"\.(?=\s)", '', word)

        # Remove other punctuations symbol
        word = re.sub(r"[!#\"$%&()*+,\/:;<=>?@\[\\\]^`{|}~]", "", word)

        return word
    
    # Formats the input string to wrap around the accepted words with html tag to indicate it is bolded
    def __boldAcceptedWords(self, inputString, acceptedWords):
        acceptedWordList = set([word for word in acceptedWords])
        print(acceptedWordList)
        for word in acceptedWordList:
            inputString = re.sub(rf'((?<!\w){word}(?![\w_]))', r'<strong>\1</strong>', inputString, flags=re.IGNORECASE)
        
        return inputString

    # Only usable for one word
    def accepts(self, wordString, returnTransitions=False):
        transitions = []
        previous_state = ""
        current_state = self.start_state
        current_word = ""
        # Replace spaces with underscores
        word = re.sub(' ', '_', wordString)
        for letter in word:
            current_word += letter
            if letter not in self.transition_dict[current_state]:
                transitions.append((current_state, letter, graphviz.escape('<REJECT>')))
                if returnTransitions:
                    return False, transitions, current_word
                return False
            previous_state = current_state
            current_state = self.transition_dict[current_state][letter]

            # print(previous_state, '+',letter, '->', current_state)
            transitions.append((previous_state, letter, current_state))
        
        if returnTransitions:
            return current_state in self.accept_states, transitions, current_word

        return current_state in self.accept_states
    
    # Only usable for one word
    def accepts_with_graph(self, wordString):
        accepts, transitions, word = self.accepts(wordString, returnTransitions=True)

        # Use Graphviz to create a graph
        dfa_dot = graphviz.Digraph(wordString, comment='DFA')
        dfa_dot.node('fake', style='invis')
        if accepts:
            dfa_dot.attr('node', color='green')
            dfa_dot.edge('fake', graphviz.escape('<s>'))
            dfa_dot.node(graphviz.escape('<s>'), root='true')
            dfa_dot.node(word, shape='doublecircle')
            for transition in transitions:
                dfa_dot.edge(graphviz.escape(transition[0]), graphviz.escape(transition[2]), label=transition[1])
        else:
            dfa_dot.attr('node', color='red')
            dfa_dot.edge('fake', graphviz.escape('<s>'))
            dfa_dot.node(graphviz.escape('<s>'), root='true', label='\<s\>')
            for transition in transitions:
                dfa_dot.edge(graphviz.escape(transition[0]), graphviz.escape(transition[2]), label=transition[1])
        
        dfa_dot.render(directory='dfaDot-Output', view=True)
    
    # Not used anymore because unable to track position properly
    def matchInputString2(self, inputString):
        formatInputString = self.__formatInputString(inputString.lower())
        wordList = formatInputString.split()
        lastWordLen = len(wordList[-1])
        acceptedWords = []
        wordOccurrence = {}
        i = 0
        while(i <= len(formatInputString)-lastWordLen):
            word = self.__formatWord(wordList[0])
            if self.accepts(word):
                acceptedWords.append((word,(i,i+len(word)-1)))
                if word in wordOccurrence:
                    wordOccurrence[word] += 1
                else:
                    wordOccurrence[word] = 1
        
            i += len(wordList[0])+1
            wordList.pop(0)

        # Format the accepted words (not involved in the GUI)
        boldedText = self.__boldAcceptedWords(inputString, acceptedWords)
        
        return acceptedWords, wordOccurrence, boldedText
    
    def matchInputString(self, inputString):
        formatInputString = self.__formatInputString(inputString)
        acceptedWords = {}
        wordOccurrence = {}
        skipLetter = False

        current_state = self.start_state

        for i, letter in enumerate(formatInputString.lower()):
            # lower_letter = letter.lower()
            if letter not in self.transition_dict[current_state]:
                # Reset the current state if the current letter is not a letter, else force it to skip the letter until the next whitespace or punctuation symbol
                if not letter.isalpha():
                    current_state = self.start_state
                    skipLetter = False
                else:
                    skipLetter = True
                continue

            if skipLetter:
                continue
            
            current_state = self.transition_dict[current_state][letter]

            # Check if current state is accepted (and make sure the current state is not part of a word)
            if current_state in self.accept_states and not formatInputString[i+1].isalnum() and formatInputString[i+1] not in ['-','_']:
                if current_state in acceptedWords:
                    acceptedWords[current_state].append((i-len(current_state)+1,i))
                else:
                    acceptedWords[current_state] = [(i-len(current_state)+1,i)]
                if current_state in wordOccurrence:
                    wordOccurrence[current_state] += 1
                else:
                    wordOccurrence[current_state] = 1
                current_state = self.start_state

        return acceptedWords, wordOccurrence


