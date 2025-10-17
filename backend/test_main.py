from fastapi import FastAPI

test_app = FastAPI()

@test_app.get("/")
def read_root():
    return {"test": "works"}
