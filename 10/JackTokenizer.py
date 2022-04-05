import sys
import textwrap
import re
import itertools

class JackTokenizer():
	keyword = ('(class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)')
	symbol = '([{}()[\].,;+\-*/&|<>=~])'
	integerConstant = '(\d+)'
	StringConstant = '\"([^\n]*)\"'
	identifier = '([A-Za-z_]\w*)'
	lexicalElements = '{}|{}|{}|{}|{}'.format(keyword, symbol, integerConstant, StringConstant, identifier)
	lexicalElementsREGEX = re.compile(lexicalElements)
	oneLinedComment = re.compile('//.*\n')
	multipleLinedComment = re.compile('/\*.*?\*/', flags=re.S)

	TokenType = ['KEYWORD', 'SYMBOL', 'INT_CONST', 'STRING_CONST', 'IDENTIFIER']

	def __init__(self, data):
		self.input = data.read()
		self.input = re.sub(self.oneLinedComment,'\n', self.input)
		self.input = re.sub(self.multipleLinedComment, ' ', self.input)
		self.matches = self.lexicalElementsREGEX.finall(self.input)
		self.matchtokentype = map(lambda x: self.TokenType[next(i for i, element in enumerate(x) if element)], self.matches)
		self.flatmatch = list(itertools.chain(*self.matches))
		self.tokens = [match for match in self.flatmatch if match] #?
		self.input2 = zip(self.tokens, self.matchtokentype)
		self.next_token = ''
		self.advance()
		self.f.close()

	def hasMoreTokens(self):
		if self.f is None:
			self.hasMoreTokens = False
		else:
			self.hasMoreTokens = True
		return self.hasMoreTokens

	def advance(self):
		self.current_token = self.next_token

		if self.hasMoreTokens == True:
			self.next_token = self.tokens.pop(0)
    	
		else:
			self.next_token = 'EOF'
        

	def tokenType(self):
		return self.current_token[1]

	def keyWord(self):
		return self.current_token[0].upper()

	def symbol(self):
		return self.current_token[0]

	def identifier(self):
		return self.current_token[0]

	def intVal(self):
   		return self.current_token[0]

	def stringVal(self):
		return self.current_token[0]
