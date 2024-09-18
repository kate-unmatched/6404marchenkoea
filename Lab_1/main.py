from Lab_1.conf_parser import UniversalConfigParser
from Lab_1.function import Function

# декораторы и исключения

file_path = input("Enter the path to the configuration file (or press Enter to enter manually): ").strip()

parser = UniversalConfigParser(file_path)

config_data = parser()

print(config_data)

result_func = Function.call_function(config_data.n0, config_data.h, config_data.nk, config_data.a, config_data.b, config_data.c)

for x, y in result_func.items():
    print(f"x:{x} >> y: {y}")