from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.sentra_core_routes import router as sentra_core_router
from database.connection import connect_to_mongo, close_mongo_connection
import uvicorn
import os
from pathlib import Path
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

# Create FastAPI app
app = FastAPI(
    title="SentraCore API",
    description="API for managing SentraCore robot configurations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sentra_core_router)

# Mount static files from the built Next.js frontend
frontend_static_path = Path(__file__).parent.parent / "LIZREC" / ".next" / "static"
if frontend_static_path.exists():
    app.mount("/_next/static", StaticFiles(directory=str(frontend_static_path)), name="static")

# Mount public files from the frontend
frontend_public_path = Path(__file__).parent.parent / "LIZREC" / "public"
if frontend_public_path.exists():
    app.mount("/images", StaticFiles(directory=str(frontend_public_path / "images")), name="images")
    app.mount("/favicon.ico", StaticFiles(directory=str(frontend_public_path)), name="favicon")
    app.mount("/favicon.png", StaticFiles(directory=str(frontend_public_path)), name="favicon_png")
    app.mount("/favicon.svg", StaticFiles(directory=str(frontend_public_path)), name="favicon_svg")

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "SentraCore API is operational"}

# Handle Next.js image optimization requests
@app.get("/_next/image")
async def handle_next_image(request: Request):
    """Handle Next.js image optimization requests by serving the original image."""
    # Extract the image path from the query parameters
    url = request.query_params.get("url", "")
    
    if url.startswith("/images/"):
        # Remove the leading slash and serve from public directory
        image_path = frontend_public_path / url[1:]  # Remove leading slash
        if image_path.exists():
            return FileResponse(str(image_path))
    
    return {"error": "Image not found"}

# Serve the frontend for all other routes (client-side routing)
@app.get("/{full_path:path}")
async def serve_frontend(request: Request, full_path: str):
    # Don't serve frontend for API routes
    if full_path.startswith("api/"):
        return {"error": "API endpoint not found"}
    
    # Don't serve frontend for static asset routes that are already mounted
    if (full_path.startswith("_next/") or 
        full_path.startswith("images/") or 
        full_path in ["favicon.ico", "favicon.png", "favicon.svg"]):
        return {"error": "Static asset not found"}
    
    # Path to the built Next.js frontend
    frontend_build_path = Path(__file__).parent.parent / "LIZREC" / ".next" / "server" / "app"
    
    # Clean the path and remove leading slash
    clean_path = full_path.strip("/")
    
    # If it's the root path, serve index.html
    if not clean_path:
        index_path = frontend_build_path / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
    
    # Try to serve the specific page
    page_path = frontend_build_path / f"{clean_path}.html"
    if page_path.exists():
        return FileResponse(str(page_path))
    
    # If not found, serve the main page (for client-side routing)
    main_page_path = frontend_build_path / "index.html"
    if main_page_path.exists():
        return FileResponse(str(main_page_path))
    
    # If no frontend files found, return a simple message
    return {"message": "Frontend not built. Please run 'npm run build' in the LIZREC directory."}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=80,
        reload=True,
        log_level="info"
    ) 