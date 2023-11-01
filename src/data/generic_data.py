from dataclasses import dataclass


@dataclass
class GenericData:
    @staticmethod
    def get_header():
        pass

    def to_csv(self):
        pass

    def to_json(self):
        pass

    @classmethod
    def from_csv(cls, csv: str):
        pass

    @classmethod
    def from_json(cls, json: dict):
        pass

    @classmethod
    def from_dict(cls, dict: dict):
        pass

    @classmethod
    def from_csv_list(cls, csv_list: list):
        pass

    @classmethod
    def from_json_list(cls, json_list: list):
        pass
