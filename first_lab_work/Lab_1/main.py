from Lab_1.conf_parser import UniversalConfigParser
from Lab_1.function import Function

# декораторы и исключения

file_path = input("Enter the path to the configuration file (or press Enter to enter manually): ").strip()

parser = UniversalConfigParser(file_path)

config_data = parser()

print(config_data)

result_func = Function.call_function(*tuple(config_data.__dict__.values()))

print("Function: a * m.sin(x) + b * m.cos(x) + abs(a * m.sin(x) - b * m.cos(x)) + c")
for x, y in result_func.items():
    print(f"x: {x} >> y: {y}")