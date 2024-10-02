import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from manual_execution.router import manual_router

app = FastAPI(title="Trading App")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(manual_router)


@app.get("/")
def welcome():
    return "Hello Fast API!!"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app="main:app", port=5000, log_level="info", reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
