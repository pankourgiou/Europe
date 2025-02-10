import operator

class SymbolicInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
        
    def evaluate_expression(self, expr):
        parts = expr.split()
        if parts[0] in self.variables:
            parts[0] = self.variables[parts[0]]
        if parts[2] in self.variables:
            parts[2] = self.variables[parts[2]]
        try:
            return str(self.operators[parts[1]](float(parts[0]), float(parts[2])))
        except (KeyError, ValueError, IndexError):
            return "Invalid expression"
        
    def execute(self, code):
        lines = code.split('\n')
        for line in lines:
            parts = line.split()
            if not parts:
                continue
            
            command = parts[0]
            
            if command == '€':  # Print command
                print(' '.join(parts[1:]))
                
            elif command == ':=':  # Variable assignment
                var_name = parts[1]
                var_value = ' '.join(parts[2:])
                if any(op in var_value for op in self.operators):
                    var_value = self.evaluate_expression(var_value)
                self.variables[var_name] = var_value
                
            elif command == '∞':  # Loop
                try:
                    count = int(parts[1])
                    loop_command = ' '.join(parts[2:])
                    for _ in range(count):
                        self.execute(loop_command)
                except ValueError:
                    print("Invalid loop count")
                
            elif command == '?':  # If condition
                var_name, condition, value = parts[1], parts[2], ' '.join(parts[3:])
                if var_name in self.variables and eval(f"{self.variables[var_name]} {condition} {value}"):
                    self.execute(' '.join(parts[4:]))
                
            elif command == 'def':  # Function definition
                func_name = parts[1]
                func_body = ' '.join(parts[2:])
                self.functions[func_name] = func_body
                
            elif command in self.functions:  # Function execution
                self.execute(self.functions[command])
                
    
# Example usage:
code = """
x := cold
? x = cold € x cold
∞ 10 € cold
def mimic € play
mimic
"""
interpreter = SymbolicInterpreter()
interpreter.execute(code)
