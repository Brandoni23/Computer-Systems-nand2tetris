import re

class CompilationEngine():
	def __init__(self, outputf, inputf):
		self.input = inputf
		self.output = outputf
		self.indent = 0
		#self.input.readline()

	def compileClass(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'class'))
		self.indent += 1
		for i in range(3):
			self.output.write(' ' * self.indent + self.input.readline())
		while ('static' in self.input | 'field' in self.input):
			self.compileClassVarDec()
		while ('constructor' in self.input | 'function' in self.input | 'method' in self.input):
			self.compileSubroutine()
		self.output.write(' ' * self.indent + self.input)
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/class'))
		self.indent -= 1

	def compileClassVarDec(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'classVarDec'))
		self.indent += 1
		for i in range(3):
			self.output.write(' ' * self.indent + self.input.readline())
		while (',' in self.input | 'identifier' in self.input):
				self.output.write(' ' * self.indent + self.input.readline())
		self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/classVarDec'))
		self.indent -= 1

	def compileSubroutine(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'subroutineDec'))
		self.indent += 1
		for i in range(4):
			self.output.write(' ' * self.indent + self.input.readline())
		self.compileParameterList()
		self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'subroutineBody'))
		self.indent += 1
		self.output.write(' ' * self.indent + self.input.readline())
		while 'var' in self.input:
			self.compileVarDec()
		self.compileStatements()
		self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/subroutineBody'))
		self.indent -= 1
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/subroutineDec'))
		self.indent -= 1

	def compileParameterList(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'parameterList'))
		self.indent += 1
		if ' ) ' not in self.input:
			for i in range(2):
				self.output.write(' ' * self.indent + self.input.readline())
		while ' ) ' not in self.input:
			for i in range(3):
				self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/parameterList'))
		self.indent -= 1

	def compileVarDec(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'varDec'))
		self.indent += 1
		for i in range(3):
	  		self.output.write(' ' * self.indent + self.input.readline())
		while (',' in self.input | 'identifier' in self.input):
			self.output.write(' ' * self.indent + self.input.readline())
		self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/varDec'))
		self.indent -= 1

	def compileStatements(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'statements'))
		self.indent += 1
		morestat = True
		#st = ['let','if','do','while','return']
		while morestat:
			stat = self.input.readline()
			if stat == 'do':
				self.compileDo()
			elif stat == 'let':
				self.compileLet()
			elif stat == 'while':
				self.compileWhile()
			elif stat == 'return':
				self.compileReturn()
			elif stat == 'if':
				self.compileIf()	
			else:
				morestat = False
			self.nexttoken = stat
			self.output.write('{}<{}>\n'.format(' ' * self.indent, '/statements'))
			self.indent -= 1

	def compileDo(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'doStatement'))
		self.indent += 1
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		if self.input == '.':
			for i in range(2):
				self.output.write(' ' * self.indent + self.input.readline())
		self.output.write(' ' * self.indent + self.input.readline())
		self.compileExpressionList()
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/doStatement'))
		self.indent -= 1

	def compileLet(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'letStatement'))
		self.indent += 1
		self.output.write(' ' * self.indent + stat)
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		if self.input == '[':
			self.output.write(' ' * self.indent + self.input.readline())
			self.compileExpression()
			self.output.write(' ' * self.indent + self.input.readline())
		self.output.write(' ' * self.indent + self.input.readline())
		self.compileExpression()
		self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/letStatement'))
		self.indent -= 1

	def compileWhile(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'whileStatement'))
		self.indent += 1
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		self.compileExpression()
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		self.compileStatements()
		self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/whileStatement'))
		self.indent -= 1

	def compileReturn(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'returnStatement'))
		self.indent += 1
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		if self.input != ';':
			self.compileExpression()
		self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/returnStatement'))
		self.indent -= 1

	def compileIf(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'ifStatement'))
		self.indent += 1
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		self.compileExpression()
		for i in range(2):
			self.output.write(' ' * self.indent + self.input.readline())
		self.compileStatements()
		self.output.write(' ' * self.indent + self.input.readline())
		maybe_el = self.input.readline()
		if maybe_el == 'else':
			self.output.write(' ' * self.indent + maybe_el)
			self.output.write(' ' * self.indent + self.input.readline())
			self.compileStatements()
			self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/ifStatement'))
		self.indent -= 1

	def compileExpression(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'expression'))
		self.indent += 1
		self.compileTerm()
		op = self.input.readline()
		while re.search(r'> (\+|-|\*|/|&amp;|\||&lt;|&gt;|=) <', op):
			self.output.write(' ' * self.indent + op)
			self.compileTerm()

		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/expression'))
		self.indent -= 1

	def compileTerm(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'term'))
		self.indent += 1
		ft = self.input.readline()
		if re.search(r'> (-|~) <', ft):
			self.output.write(' ' * self.indent + ft)
			self.compileTerm()
		elif '(' in ft:
			self.output.write(' ' * self.indent + ft)
			self.compileExpression()
			self.output.write(' ' * self.indent + self.input.readline())
		else:
			self.output.write(' ' * self.indent + ft)
			br = self.input.readline()
			if br == '[':
				self.output.write(' ' * self.indent + br)
				self.compileExpression()
				self.output.write(' ' * self.indent + self.input.readline())
			elif br == '(':
				self.output.write(' ' * self.indent + br)
				self.compileExpressionList()
				self.output.write(' ' * self.indent + self.input.readline())
			elif br == '.':
				self.output.write(' ' * self.indent + br)
				for i in range(2):
					self.output.write(' ' * self.indent + self.input.readline())
				self.compileExpressionList
				self.output.write(' ' * self.indent + self.input.readline())
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/term'))
		self.indent -= 1

	def compileExpressionList(self):
		self.output.write('{}<{}>\n'.format(' ' * self.indent, 'expressionList'))
		self.indent += 1
		li = self.input.readline()
		if li != '(':
			self.compileExpression()
		while li != '(':
			self.output.write(' ' * self.indent + self.input.readline())
			self.compileExpression()
			li = self.input.readline()
		self.nexttoken2 = li
		self.output.write('{}<{}>\n'.format(' ' * self.indent, '/expressionList'))
		self.indent -= 1