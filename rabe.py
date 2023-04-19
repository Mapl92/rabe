from fastapi import FastAPI, HTTPException, File, Form
from pydantic import BaseModel
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.openapi.utils import get_openapi

app = FastAPI()

class InputData(BaseModel):
    word: str

class HintImageData(BaseModel):
    image_id: str

@app.post("/get-auth-key", summary="Get authentication key", description="This endpoint accepts a word as input and returns an authentication key if the input is correct.")
async def get_auth_key(input_data: InputData):
    if input_data.word == "Rabe":
        return {"auth_key": "cI2PqdL7ja"}
    else:
        raise HTTPException(status_code=400, detail="Ungültige Eingabe. Bitte das korrekte Wort übermitteln.")

@app.get("/",include_in_schema=False, summary="View the image viewer form", description="This endpoint serves an HTML form for entering the authentication code to view the image.")
async def read_root():
    with open("index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

# Set include_in_schema to False for the /show-image endpoint
@app.post("/show-image", include_in_schema=False)
async def show_image(code: str = Form(...)):
    if code == "cI2PqdL7ja":
        return FileResponse("rabebilder/hint0.jpeg", media_type="image/jpeg")
    else:
        raise HTTPException(status_code=403, detail="Ungültiger Code. Zugriff verweigert.")

@app.get("/show-raven", include_in_schema=False)
async def show_raven():
    return FileResponse("rabebilder/raven.png", media_type="image/png")


@app.post("/show-hint-image",include_in_schema=False)
async def show_hint_image(image_data: HintImageData):
    image_path = f"rabebilder/{image_data.image_id}.jpeg"
    return FileResponse(image_path, media_type="image/jpeg")



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Rabe Love API",
        version="1.0.0",
        description="This is the API documentation for the Rabe Love application. It provides an endpoint for getting an authentication key.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
