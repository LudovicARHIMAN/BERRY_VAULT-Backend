from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/test")
async def test(request: Request):
    # Get the request body data sent by the client
    data = await request.json()  # If the client sends JSON data

    # Assuming the client sends two values named "value1" and "value2"
    value1 = data.get("value1")
    value2 = data.get("value2")

    # Print the received values
    print("Received value1 from client:", value1)
    print("Received value2 from client:", value2)

    return {"message": "Data received successfully"}
    