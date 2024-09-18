from dataclasses import dataclass
import json
import csv
import xml.etree.ElementTree as ET
import yaml
import os

from Lab_1.exceptions import handle_exceptions, UnsupportedFileTypeError, ConfigParsingError
REQUIRED_KEYS = ('n0', 'h', 'nk', 'a', 'b', 'c')


@dataclass(frozen=True)
class ConfigData:
    n0: int
    h: int
    nk: int
    a: float
    b: float
    c: float

    def _txt_format(self) -> str:
        return ','.join(f'{k} {v}' for k, v in self.__dict__.items())

    def _csv_format(self) -> str:
        return ','.join(f'{k} {v}' for k, v in self.__dict__.items())

    def _json_format(self) -> str:
        return f"{{\n{','.join(f'\t\"{k}\": {v}' for k, v in self.__dict__.items())}\n}}"

    def _yaml_format(self) -> str:
        return ','.join(f'{k} {v}' for k, v in self.__dict__.items())

    def _xml_format(self) -> str:
        return ','.join(f'{k} {v}' for k, v in self.__dict__.items())

    def __format__(self, format_spec):
        match format_spec:
            case 'txt': return self._txt_format()
            case 'csv': return self._csv_format()
            case 'json': return self._json_format()
            case 'yaml': return self._yaml_format()
            case 'xml': return self._xml_format()
            case _: raise UnsupportedFileTypeError(f"Unsupported format: {format_spec}")

    def __str__(self):
        return f"{self:txt}"

    def __repr__(self):
        return f"\nConfiguration Data:\n{'\n'.join(f'{k}:{v}' for k, v in self.__dict__.items())}"


class UniversalConfigParser:
    def __init__(self, file_path: str | None = None):
        self.file_path = file_path
        if not self.file_path:
            print("Файл не указан. Пожалуйста, введите параметры вручную.")
        elif not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")

    @handle_exceptions
    def __call__(self) -> ConfigData:
        if not self.file_path:
            return self._manual_input()
        file_path_end = self.file_path.split('.')[-1]
        match file_path_end:
            case 'json': return self._parse_json()
            case 'xml': return self._parse_xml()
            case 'csv': return self._parse_csv()
            case 'yaml': return self._parse_yaml()
            case 'txt': return self._parse_txt()
            case '_': raise UnsupportedFileTypeError(f"Unsupported format: {self.file_path}")

    @handle_exceptions
    def _parse_json(self) -> ConfigData:
        with open(self.file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                raise ConfigParsingError(f"JSON parse error: {e}")
        return self._validate_data(data)

    @handle_exceptions
    def _parse_xml(self) -> ConfigData:
        try:
            tree = ET.parse(self.file_path)
        except ET.ParseError as e:
            raise ConfigParsingError(f"XML parse error: {e}")
        root = tree.getroot()
        data = {child.tag: child.text for child in root}
        return self._validate_data(data)

    @handle_exceptions
    def _parse_csv(self) -> ConfigData:
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = next(reader, None)
            if not data:
                raise ConfigParsingError("CSV is empty or malformed")
        return self._validate_data(data)

    @handle_exceptions
    def _parse_yaml(self) -> ConfigData:
        with open(self.file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise ConfigParsingError(f"YAML parse error: {e}")
        return self._validate_data(data)

    @handle_exceptions
    def _parse_txt(self) -> ConfigData:
        data = {}
        with open(self.file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                data[key.strip()] = float(value.strip()) if '.' in value else int(value.strip())
        return self._validate_data(data)

    def _manual_input(self) -> ConfigData:
        def get_int_input(prompt):
            while True:
                try:
                    return int(input(prompt))
                except ValueError:
                    print("Ошибка: введите целое число!")

        def get_float_input(prompt):
            while True:
                try:
                    return float(input(prompt))
                except ValueError:
                    print("Ошибка: введите число с плавающей точкой!")

        n0 = get_int_input("Введите значение n0 (int): ")
        h = get_int_input("Введите значение h (int): ")
        nk = get_int_input("Введите значение nk (int): ")
        a = get_float_input("Введите значение a (float): ")
        b = get_float_input("Введите значение b (float): ")
        c = get_float_input("Введите значение c (float): ")

        return ConfigData(n0=n0, h=h, nk=nk, a=a, b=b, c=c)

    def _validate_data(self, data: dict[str, float | int]) -> ConfigData:

        if not all(key in data for key in REQUIRED_KEYS):
            raise ConfigParsingError(f"Missing required key")

        return ConfigData(
            n0=int(data['n0']),
            h=int(data['h']),
            nk=int(data['nk']),
            a=float(data['a']),
            b=float(data['b']),
            c=float(data['c'])
        )
