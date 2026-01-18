from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import dairy_routes, milkman_routes
from db.database import connect_to_mongo, close_mongo_connection
import os
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await connect_to_mongo()
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e
    
    yield
    
    # Shutdown
    await close_mongo_connection()

app = FastAPI(title="Milkman API", lifespan=lifespan)

# CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "*" # Keeping wildcard for now as per previous logic, but structured list
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dairy_routes.router, prefix="/api/v1/dairy", tags=["Dairy"])
app.include_router(milkman_routes.router, prefix="/api/v1/milkman", tags=["Milkman"])

# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Milkman API is running!", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Use PORT environment variable for Render
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)