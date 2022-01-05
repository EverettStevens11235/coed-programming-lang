import argparse
from tkinter import *

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help="name of coed file to run")
parser.add_argument('-d', type=bool, help="Debug mode")
args = parser.parse_args()

text = open(args.filename, 'r').read()

variables = {}

def lexer(text):
	tokens = []
	tok = ""
	string = ""
	inString = False
	ignore = False
	listeningForVarName = False
	listeningForVarValue = False
	varName = ""
	varValue = None
	postingVar = False
	lforfname = False
	fname=""
	inFunc = False
	digits = "0123456789"
	num = ""
	line = 1
	dbg = args.d
	if dbg:
		print("Entered line 1.")
	for char in text:
		tok += char
		if ignore:
			if tok == "/":
				ignore = False
				tok = ""
			elif tok == " ":
				tok = ""
			else:
				tok = ""
		else:
			if inString:
				if tok == "'":
					tokens.append(f"STRING '{string}'")
					if listeningForVarValue:
						listeningForVarValue = False
					string = ""
					inString = False
					tok = ""
				else:
					string+=tok
					tok=""
			if tok == " ":
				if inString:
					string += tok
				tok = ""
			elif tok == "open":
				tokens.append("OPEN FUNCTION")
				tok = ""
			elif tok == "as":
				tok = ""
			elif tok == "showtext":
				tokens.append("SHOWTEXT")
				tok = ""
			elif tok == "'":
				inString = True
				tok = ""
			elif tok == "function":
				tokens.append(f"FUNCTION: {fname}")
				fname = ""
				tok = ""
			elif tok == "create~":
				tokens.append("CREATE")
				lforfname = True
				tok = ""
			elif tok == "\n":
				line+=1
				inFunc = False
				if dbg:
					print(f"Entered line {line}.")
				tok = ""
			elif tok == "get":
				tokens.append("GET VAR")
				tok = ""
			elif tok == "post":
				tokens.append("POST VAR")
				tok = ""
			elif tok == "/":
				ignore = True
				tok = ""
			elif tok == "(":
				listeningForVarName = True
				tok = ""
			elif tok == ")":
				listeningForVarName = False
				tokens.append(f"NAME: '{varName}'")
				varName = ""
				postingVar = True
				tok = ""
			elif tok == "=":
				if postingVar:
					listeningForVarValue = True
				tok=""
			elif tok in digits:
				if inString:
					string += tok
					tok = ""
				else:
					num += tok
					tok = ""
			elif tok == "mknum":
				newNum = int(num)
				if listeningForVarValue:
					varValue = newNum
				tok = ""
			elif tok == "rmnum":
				num = ""
				tok = ""
			elif tok == ":":
				if postingVar:
					postingVar = False
				elif lforfname:
					lforfname = False
				tok = ""
			elif tok == "-":
				if listeningForVarValue == True:
					listeningForVarValue = False
					tokens.append(f"VALUE: {str(varValue)}")
					varValue = 0
				tok = ""
			elif tok == "\t":
				inFunc = True
				tok=""
			elif tok == "end":
				tokens.append("END")
				tok = ""
			elif tok == "msgbox":
				tokens.append("MSGBOX")
				tok=""
			else:
				# if its a character/group of characters out of syntax
				if inString:
					string += tok
					tok = ""
				elif listeningForVarName == True:
					varName += tok
					tok = ""
				elif lforfname:
					fname += tok
					tok = ""
				else:
					pass
				
	
	if tokens == []:
		raise IndexError("No tokens found in tokens list.")
	else:
		return tokens

def parser(tokens):
	#print("space")
	try:
		global variables
		if tokens[0] == "CREATE":
			#print("space")
			if tokens[1][0:8] == "FUNCTION" and tokens[len(tokens) - 1] == "END":
				#print(tokens[len(tokens) - 1])
				i = 2
				while i < len(tokens) - 1:
					#print("space")
					if tokens[i] + " " + tokens[i+1][0:4] == "POST VAR NAME":
						#print("space")
						if tokens[i+2][0:5] == "VALUE":	
							newValue = tokens[i+2][7:8]
							name = tokens[i+1][7:][:-1]
							variables[name] = newValue
						elif tokens[i+2][0:6] == "STRING":
							newValue = tokens[i+2][8:][:-1]
							name = tokens[i+1][7:][:-1]
							variables[name] = newValue
					elif tokens[i] + " " + tokens[i+1][0:4] == "GET VAR NAME":
						name = tokens[i+1][7:][:-1]
						if name in variables:
							print(variables[name])
						else:
							raise Exception(f"Never assigned variable with name {name}.")
					elif tokens[i] == "MSGBOX":
						root = Tk()
						text = Label(root, text=tokens[i+1][8:][:-1])
						text.pack()
						root.mainloop()
					elif tokens[i] + " " + tokens[i+1] == "OPEN FUNCTION SHOWTEXT":
						#print("space")
						print(tokens[i+2][8:][:-1])
					#print(tokens[i])
					i+=1
			else:
				raise SyntaxError()
		else:
			raise SyntaxError("Script must be a function class.")
	except Exception as e:
		print(e)

parser(lexer(text))
if args.d: 
	print(variables)
