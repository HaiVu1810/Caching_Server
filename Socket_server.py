import os
import uvicorn
from Fetchinghandle import app
def server_program(port, url):
    os.environ["ORIGIN_URL"] = url
    uvicorn.run("Fetchinghandle:app", host="localhost", port=port , reload=True)   