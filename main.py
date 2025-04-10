from fastapi import FastAPI
from order_routes import order_router
from auth_routes import auth_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Monace"}

# Include the routers
app.include_router(auth_router)
app.include_router(order_router)

