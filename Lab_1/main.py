from win32com.server.policy import call_func

from Lab_1.conf_parser import UniversalConfigParser

from Lab_1.function import Function

# декораторы и исключения

file_path = 'config_files/config.txt'
parser = UniversalConfigParser(file_path)

config_data = parser()

print(config_data)

print(Function.call_function(config_data.n0, config_data.h, config_data.nk, config_data.a, config_data.b, config_data.c))
