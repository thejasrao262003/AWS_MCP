from pydantic import BaseModel

class ListEC2Params(BaseModel):
    region: str
