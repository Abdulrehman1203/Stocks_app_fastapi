from fastapi import FastAPI

from database.db import engine, Base
from routes import user_routes, stock_routes, transaction_routes
import uvicorn
app = FastAPI()

# Include the route files
app.include_router(user_routes.router)
app.include_router(stock_routes.router)
app.include_router(transaction_routes.router)

Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True)
