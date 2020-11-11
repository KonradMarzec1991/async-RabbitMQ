import pydantic as pd


class Pair(pd.BaseModel):
    key: str
    value: float

    def __repr__(self):
        return f'Pair(key={self.key}, value={self.value})'

    def __str__(self):
        return repr(self)
