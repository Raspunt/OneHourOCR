from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PIL import Image
import pytesseract
import io
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")



@app.get("/", response_class=HTMLResponse)
async def main_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/ocr/", response_class=HTMLResponse)
async def ocr_image(
    request: Request,
    file: UploadFile = File(...),
    lang: str = Form("rus")
):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        text = pytesseract.image_to_string(image, lang=lang)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": text,
                "filename": file.filename,
                "language": lang,
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
