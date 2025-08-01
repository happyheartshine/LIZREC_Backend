from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from models.sentra_core import SentraCoreModel, SentraCoreCreate, SentraCoreUpdate, LabelModel, ConnectionModel
from controllers.sentra_core_controller import SentraCoreController
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/sentra-core", tags=["SentraCore"])

# Dependency to get controller instance
def get_controller():
    return SentraCoreController()

# Request model for saving current state
class FrontendLabel(BaseModel):
    id: str
    text: str
    value: str
    x: float
    y: float
    category: str

class FrontendConnection(BaseModel):
    id: str
    from_: str = Field(alias="from")
    to: str

class SaveStateRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    labels: List[FrontendLabel]
    connections: List[FrontendConnection]
    selected_option: str

@router.post("/", response_model=SentraCoreModel, status_code=201)
async def create_sentra_core(
    sentra_core_data: SentraCoreCreate,
    controller: SentraCoreController = Depends(get_controller)
):
    """Create a new SentraCore configuration."""
    try:
        return await controller.create_sentra_core(sentra_core_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{sentra_core_id}", response_model=SentraCoreModel)
async def get_sentra_core(
    sentra_core_id: str,
    controller: SentraCoreController = Depends(get_controller)
):
    """Get a SentraCore configuration by ID."""
    try:
        sentra_core = await controller.get_sentra_core_by_id(sentra_core_id)
        if not sentra_core:
            raise HTTPException(status_code=404, detail="SentraCore configuration not found")
        return sentra_core
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[SentraCoreModel])
async def get_all_sentra_core(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    controller: SentraCoreController = Depends(get_controller)
):
    """Get all SentraCore configurations with pagination."""
    try:
        return await controller.get_all_sentra_core(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{sentra_core_id}", response_model=SentraCoreModel)
async def update_sentra_core(
    sentra_core_id: str,
    update_data: SentraCoreUpdate,
    controller: SentraCoreController = Depends(get_controller)
):
    """Update a SentraCore configuration."""
    try:
        updated_sentra_core = await controller.update_sentra_core(sentra_core_id, update_data)
        if not updated_sentra_core:
            raise HTTPException(status_code=404, detail="SentraCore configuration not found")
        return updated_sentra_core
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{sentra_core_id}")
async def delete_sentra_core(
    sentra_core_id: str,
    controller: SentraCoreController = Depends(get_controller)
):
    """Delete a SentraCore configuration."""
    try:
        deleted = await controller.delete_sentra_core(sentra_core_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="SentraCore configuration not found")
        return {"message": "SentraCore configuration deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/", response_model=List[SentraCoreModel])
async def search_sentra_core(
    name: str = Query(..., description="Name to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    controller: SentraCoreController = Depends(get_controller)
):
    """Search SentraCore configurations by name."""
    try:
        return await controller.search_sentra_core_by_name(name, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/count/")
async def get_sentra_core_count(
    controller: SentraCoreController = Depends(get_controller)
):
    """Get total count of SentraCore configurations."""
    try:
        count = await controller.get_sentra_core_count()
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save-state/", response_model=SentraCoreModel, status_code=201)
async def save_current_state(
    request: SaveStateRequest,
    controller: SentraCoreController = Depends(get_controller)
):
    """Save the current state from the frontend."""
    try:
        return await controller.save_current_state(
            name=request.name,
            labels=request.labels,
            connections=request.connections,
            selected_option=request.selected_option,
            description=request.description
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 