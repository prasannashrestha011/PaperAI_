from fastapi import FastAPI
from pydantic import BaseModel
api=FastAPI()

class ResponseModel(BaseModel):
    success:bool 
    message:str
@api.get("/",response_model=ResponseModel)
async def main():
    return {"success":True,"message":"Hle"}   
