import requests
from typing import Union

from fastapi import FastAPI
import uvicorn
import WiseTestData

#uvicorn src.api:app
#uvicorn.run("api:app", port=5001, log_level="info")
#uvicorn.run

app = FastAPI()


@app.get("/")
def read_root():
    runer = WiseTestData.WiseTestData("api", 30, 'TestData2.xlsx', True, False, False)
    runer.make_data()
    return {"sas"}


#Main REST API:
#http://127.0.0.1:8009/generate/True/rows/11/skipshuffle/False/skippairs/False?excel=TestData.xlsx

@app.get("/generate/{generate}/rows/{rows}/skipshuffle/{skipshuffle}/skippairs/{skippairs}")
def read_item(rows: int, generate:str, skipshuffle:str, skippairs:str, excel: Union[str, None] = None):

    if rows<3: return ("ERROR: Please provide at least 3 rows for data generation")
    try:
        if generate=="False": no_generate="True"
        else:
            no_generate="False"
        runer = WiseTestData.WiseTestData("api", rows, excel, no_generate, skipshuffle, skippairs)
        return_json = runer.make_data()
    except: return {"Error in job execution. Make sure you provide correct data in URL and your Excel file path exists. API spec: http://HOST:port/generate/{True|False}/rows/{#rows_to_generate}/skipshuffle/{True|False}/skippairs/{True|False}"}

    return {"Download data from "+ str(excel) +" All pairs JSON:    "+ str(return_json)}



#unnededed class for now
class DataAPI ():

    _instance = None
    api_version="api1"
    rows=10
    excel='TestData.xlsx'
    no_gen=True
    no_pair=False
    no_shuffle=False


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_version, rows, excel, no_gen, no_pair, no_shuffle):
        if api_version!="" and api_version!=None:
            self.api_version = api_version
        if rows != "" and rows != None:
            self.rows = rows
        if excel != "" and excel != None:
            self.excel = excel
        if no_gen != "" and no_gen != None:
            self.no_gen = no_gen
        if no_pair != "" and no_pair != None:
            self.no_pair = no_pair
        if no_shuffle != "" and no_shuffle != None:
            self.no_shuffle = no_shuffle

