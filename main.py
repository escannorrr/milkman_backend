import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import dairy_routes, milkman_routes
from db.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Milkman API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

# Startup and shutdown events
@app.on_event("startup")
async def startup_db_client():
    try:
        await connect_to_mongo()
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable for Render
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)