from dataclasses import dataclass

@dataclass
class DataClassSources:
    name: str = ""
    suffix: str = ""
    zone: str = ""
    region: str = ""
    externalIP: str = ""
    token: str = ""
    api_server: str = ""
    context: str = ""