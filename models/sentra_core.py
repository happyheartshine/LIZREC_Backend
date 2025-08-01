from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Union
from datetime import datetime
from bson import ObjectId

class LabelModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the label")
    text: str = Field(..., description="Display text/title of the label")
    value: str = Field(..., description="Value/parameter of the label")
    x: float = Field(..., description="X coordinate position")
    y: float = Field(..., description="Y coordinate position")
    category: str = Field(..., description="Category of the action (move, turn, grip, wait)")

class ConnectionModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the connection")
    from_id: str = Field(..., description="Source label ID")
    to_id: str = Field(..., description="Target label ID")

class SentraCoreModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Robot Movement Sequence",
                "description": "A sequence of robot movements and actions",
                "labels": [
                    {
                        "id": "1",
                        "text": "Forward",
                        "value": "100",
                        "x": 150.0,
                        "y": 200.0,
                        "category": "move"
                    },
                    {
                        "id": "2", 
                        "text": "Turn Right",
                        "value": "90",
                        "x": 300.0,
                        "y": 200.0,
                        "category": "turn"
                    }
                ],
                "connections": [
                    {
                        "id": "1-2",
                        "from_id": "1",
                        "to_id": "2"
                    }
                ],
                "selected_option": "move-forward"
            }
        }
    )
    
    id: Optional[Union[str, ObjectId]] = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(..., description="Name of the SentraCore configuration")
    description: Optional[str] = Field(default="", description="Description of the configuration")
    labels: List[LabelModel] = Field(default_factory=list, description="List of action labels/blocks")
    connections: List[ConnectionModel] = Field(default_factory=list, description="List of connections between labels")
    selected_option: Optional[str] = Field(default="", description="Currently selected action option")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

class SentraCoreCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    labels: List[LabelModel] = []
    connections: List[ConnectionModel] = []
    selected_option: Optional[str] = ""

class SentraCoreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[List[LabelModel]] = None
    connections: Optional[List[ConnectionModel]] = None
    selected_option: Optional[str] = None 