from dataclasses import dataclass

@dataclass
class TransportUserOutData:
    user_id: int
    user_name: str
    display_name: str
    hashed_password: str


@dataclass
class TransportUserPublicOutData:
    user_id: int
    user_name: str
    display_name: str