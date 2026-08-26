# fast_test.py
"""A simple FastAPI application with detailed comments.

This file demonstrates how to set up a basic FastAPI server,
including route definitions and example request handling.
"""

# Import FastAPI class from the fastapi package.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create an instance of the FastAPI class.
app = FastAPI()

# Define a Pydantic model for request bodies.
class Item(BaseModel):
    """Schema for an item.

    Attributes:
        name: Name of the item (string).
        price: Price of the item (float).
        is_offer: Optional flag indicating if the item is on offer.
    """
    name: str
    price: float
    is_offer: bool = False

# Root path endpoint.
@app.get("/", summary="Root endpoint", description="Returns a simple greeting message.")
async def read_root():
    """GET / - Returns a welcome message."""
    return {"message": "Welcome to FastAPI!"}

# Example GET endpoint with path parameter.
@app.get("/items/{item_id}", summary="Get item by ID", description="Returns details of an item given its ID.")
async def read_item(item_id: int, q: str | None = None):
    """GET /items/{item_id}
    
    Args:
        item_id: The ID of the item to retrieve.
        q: Optional query string.
    """
    item = {"item_id": item_id, "name": f"Item {item_id}", "price": 9.99}
    if q:
        item["query"] = q
    return item

# Example POST endpoint to create a new item.
@app.post("/items/", summary="Create an item", description="Creates a new item using the provided JSON body.")
async def create_item(item: Item):
    """POST /items/ - Create a new item.
    
    The request body must conform to the Item model defined above.
    """
    # In a real application you would save the item to a database.
    # Here we simply return the received item with an ID.
    return {"item_id": 1, **item.dict()}

# Example endpoint that raises an HTTPException.
@app.get("/error", summary="Trigger error", description="Endpoint that always raises a 404 error for demonstration.")
async def trigger_error():
    """GET /error - Demonstrates raising an HTTPException."""
    raise HTTPException(status_code=404, detail="Item not found")

# If this script is run directly, start the server (useful for local testing).
if __name__ == "__main__":
    import uvicorn
    # uvicorn will run the app on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
