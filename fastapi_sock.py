from fastapi import FastAPI, WebSocket


app = FastAPI()

@app.websocket('/ws')
async def websocket_entry(websocket: WebSocket):
    await websocket.accept()
    while True:
        print(await websocket.receive())
        await websocket.send_text('w')