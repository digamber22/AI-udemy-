from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/contact-us")
def read_root():
    return {"email": "digamberbosak22@gamil.com"}