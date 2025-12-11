import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse


app = FastAPI(title="Blood on the Clocktower")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)