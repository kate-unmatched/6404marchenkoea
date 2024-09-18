from dataclasses import dataclass
import json
import csv
import xml.etree.ElementTree as ET
import yaml
import os

@dataclass
class ConfigData:
    n0: int
    h: int
    nk: int
    a: float
    b: float
    c: float

class UniversalConfigParser:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def __call__(self) -> ConfigData:
        if self.file_path.endswith('.json'):
            return self._parse_json()
        elif self.file_path.endswith('.xml'):
            return self._parse_xml()
        elif self.file_path.endswith('.csv'):
            return self._parse_csv()
        elif self.file_path.endswith('.yaml'):
            return self._parse_yaml()
        elif self.file_path.endswith('.txt'):
            return self._parse_txt()
        else:
            raise ValueError('Unsupported format')

    def _parse_json(self) -> ConfigData:
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return ConfigData(n0=data['n0'], h=data['h'], nk=data['nk'],
                          a=data['a'], b=data['b'], c=data['c'])

    def _parse_xml(self) -> ConfigData:
        tree = ET.parse(self.file_path)
        root = tree.getroot()
        return ConfigData(
            n0=int(root.find('n0').text), h=int(root.find('h').text),
            nk=int(root.find('nk').text), a=float(root.find('a').text),
            b=float(root.find('b').text), c=float(root.find('c').text)
        )

    def _parse_csv(self) -> ConfigData:
        with open(self.file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = next(reader)
            return ConfigData(
                n0=int(data['n0']), h=int(data['h']), nk=int(data['nk']),
                a=float(data['a']), b=float(data['b']), c=float(data['c'])
            )

    def _parse_yaml(self) -> ConfigData:
        with open(self.file_path, 'r') as file:
            data = yaml.safe_load(file)
        return ConfigData(n0=data['n0'], h=data['h'], nk=data['nk'],
                          a=data['a'], b=data['b'], c=data['c'])

    def _parse_txt(self) -> ConfigData:
        data = {}
        with open(self.file_path, 'r') as file:
            line = file.readline().strip()
            pairs = line.split()
            for pair in pairs:
                key, value = pair.split('=')
                data[key.strip()] = float(value.strip()) if '.' in value else int(value.strip())
        return ConfigData(n0=data['n0'], h=data['h'], nk=data['nk'],
                          a=data['a'], b=data['b'], c=data['c'])

