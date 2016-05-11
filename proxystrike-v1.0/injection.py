#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)
# This is a port of sqlibf to python, # sqlibf is a SQL injection 
# tool that was coded by Ramon Pinuaga (www.open-labs.org)


class InjectionType:
	def __init__(self,title):
		self.title=title

	def __str__(self):
		return self.title

TUnescaped=InjectionType( "Unescaped Injection")

TNumeric=InjectionType( "Numeric Injection")

TSingleQuote=InjectionType( "Single Quoted Injection")

TDoubleQuote=InjectionType( "Double Quoted Injection")

TConcatPipe=InjectionType( "Pipe concatenation Injection")

TConcatPlus=InjectionType( "Plus concatenation Injection")
