#!/usr/bin/env python3
from fastapi import FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from stepper import Stepper
import atexit
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
stepper = Stepper()

def turn_off():
    print("shutting down")
    stepper.shutdown()

#atexit.register(turn_off)


@app.get("/", response_class=HTMLResponse)
async def get_index():
    return open("static/index.html", "r").read()



@app.get("/stepper/{status}")
async def toggle_status(status: bool, background_tasks: BackgroundTasks):

    if status:
        stepper.setState(True)
        return {"message": "Status is On", "status": True}
    stepper.setState(False)
    return {"message": "Status is Off", "status": False}


@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(stepper.background())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
