import sys

logics = {}
T_STRING = 0
T_AND = 1
T_NOT = 2
T_OUTPUT = 3
T_PRTOUT = 4
T_PRTOUTS = 5
T_BINDIGIT = 6
T_PRTRTN = 7
T_OUTNOT = 8
T_IMPORT = 9
T_START = 10
T_CUSTOM = 11
T_SAVEOUT = 12
T_LOADOUT = 13

class Logical:
    def __init__(self):
        self.outputs = []
        self.result = True
        self.saved_outs = []

    def output(self):
        self.outputs.append(self.result)

    def start(self):
        self.result = True

    def AND(self):
        A = self.outputs.pop()
        B = self.result
        if A and B:
            self.result = True
        else:
            self.result = False

    def NOT(self):
        INPUT = self.result
        self.result = not INPUT

    def BINDIGIT(self):
        B = self.outputs.pop()
        C = self.outputs.pop()
        D = self.outputs.pop()
        A = self.result

        decimal_value = A * 8 + B * 4 + C * 2 + D * 1

        print(decimal_value, end='')

    def prtout(self):
        print(self.outputs.pop())

    def prtouts(self):
        print(self.outputs)

    def prtrtn(self):
        print(self.result)

    def OUTNOT(self):
        INPUT = self.outputs.pop()
        self.result = not INPUT

    def saveout(self):
        self.saved_outs.append(self.outputs.pop())

    def loadout(self):
        self.result = self.saved_outs.pop()

def Lex(code):
    splitted = code.split()
    tokenpos = 1
    in_str = [False]
    tokens = []
    finalstr = []

    while tokenpos <= len(splitted):
        token = splitted[tokenpos - 1]
        tokenpos += 1

        if not in_str[0]:
            if token.startswith("\""):
                if token.endswith("\""):
                    tokens.append((T_STRING, token.replace("\"", "").replace("\\n", "\n")))
                else:
                    finalstr.clear()
                    in_str[0] = True
                    finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
            elif token == "and":
                tokens.append((T_AND,))
            elif token == "not":
                tokens.append((T_NOT,))
            elif token == "out":
                tokens.append((T_OUTPUT,))
            elif token == "prtout":
                tokens.append((T_PRTOUT,))
            elif token == "prtouts":
                tokens.append((T_PRTOUTS,))
            elif token == "bdigit":
                tokens.append((T_BINDIGIT,))
            elif token == "onot":
                tokens.append((T_OUTNOT,))
            elif token == "prtrtn":
                tokens.append((T_PRTRTN,))
            elif token == "import":
                tokens.append((T_IMPORT,))
            elif token == "start":
                tokens.append((T_START,))
            elif token == "saveout":
                tokens.append((T_SAVEOUT,))
            elif token == "loadout":
                tokens.append((T_LOADOUT,))
            else:
                tokens.append((T_CUSTOM, token))
        elif in_str[0]:
            if token.endswith("\""):
                finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
                tokens.append((T_STRING, " ".join(finalstr).replace("\"", "").replace("\\n", "\n")))
                finalstr.clear()
                in_str[0] = False
            else:
                finalstr.append(token.replace("\"", "").replace("\\n", "\n"))
        else:
            print("Error in lexer: where we are?")
            sys.exit(1)
    return tokens

logic = [Logical()]

def interpret(code):
    tokens = Lex(code)
    tokenpos = 1

    while tokenpos <= len(tokens):
        if tokens:
            token = tokens[tokenpos - 1]
            tokenpos += 1

            if token[0] == T_NOT:
                logic[0].NOT()
            elif token[0] == T_IMPORT:
                token = tokens[tokenpos - 1]
                tokenpos += 1
                if token[0] == T_STRING:
                    if token[1].endswith(".logc"):
                        with open(token[1], "r") as fi:
                            logics[token[1].replace(".logc", "")] = fi.read()
                    else:
                        print("Error: use .logc file extension")
                        sys.exit(1)
                else:
                    print("Error: use strings to specify files directorys to import")
                    sys.exit(1)
            elif token[0] == T_AND:
                logic[0].AND()
            elif token[0] == T_OUTPUT:
                logic[0].output()
            elif token[0] == T_BINDIGIT:
                logic[0].BINDIGIT()
            elif token[0] == T_PRTOUT:
                logic[0].prtout()
            elif token[0] == T_PRTOUTS:
                logic[0].prtouts()
            elif token[0] == T_PRTRTN:
                logic[0].prtrtn()
            elif token[0] == T_START:
                logic[0].start()
            elif token[0] == T_OUTNOT:
                logic[0].OUTNOT()
            elif token[0] == T_SAVEOUT:
                logic[0].saveout()
            elif token[0] == T_LOADOUT:
                logic[0].loadout()
            elif token[0] == T_CUSTOM:
                if token[1] in logics.keys():
                    interpret(logics.get(token[1]))
                else:
                    print(f"Error: unknown keyword: {token[1]}")
            else:
                print("TODO: not implemented yet or doesn't exists")
                sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Computer logic simulator esolang")
        print(f"usage: {sys.argv[0]} <file>")
    else:
        if sys.argv[1].endswith(".logc"):
            with open(sys.argv[1], "r") as f:
                interpret(f.read())
        else:
            print("Error: use .logc file extension")
            sys.exit(1)
