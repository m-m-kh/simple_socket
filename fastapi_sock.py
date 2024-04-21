from fastapi import FastAPI, WebSocket
from fastapi.responses import Response, HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import asyncio
import pathlib

template = Jinja2Templates(pathlib.Path(__file__).parent/'templates')

app = FastAPI()

app.mount('/static',StaticFiles(directory='static'),name='static')


app.sockets = set() 


async def check_socket(tasks, websocket: WebSocket):
    while websocket.client_state.name == "CONNECTED":
        await asyncio.sleep(5)
    
    for task in tasks:
        task:asyncio.Task
        task.cancel()
    
        
        

async def reciver(websocket: WebSocket):
    while True:
        print(await websocket.receive_text())
    
        
async def sender(websocket: WebSocket):
    while True:
        txt = await asyncio.to_thread(input,':>>>>>>> ')
        print(await websocket.send_text(txt))


async def worker(websocket: WebSocket):
    t1 = asyncio.create_task(reciver(websocket))
    t2 = asyncio.create_task(sender(websocket))
    t3 = asyncio.create_task(check_socket([t1,t2],websocket))

    await asyncio.gather(t1,t2,t3)


    
    
@app.websocket('/ws')
async def websocket_entry(websocket: WebSocket):
    await websocket.accept()  
    websocket.app.sockets.add(websocket)  
    await worker(websocket)
    
    
    
@app.route('/')
async def view_sockets(request:Request):
    
    discoonect = set()
    for sock in request.app.sockets:
        if sock.client_state.name != "CONNECTED":
            discoonect.add(sock)
    sockets = request.app.sockets.difference(discoonect)
            
    
    return template.TemplateResponse('index.html',
                                     context={
                                         'request':request,
                                         'sockets':sockets})
