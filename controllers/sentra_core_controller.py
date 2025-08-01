from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from database.connection import get_collection
from models.sentra_core import SentraCoreModel, SentraCoreCreate, SentraCoreUpdate

class SentraCoreController:
    def __init__(self):
        self.collection = get_collection("sentra_core")

    async def create_sentra_core(self, sentra_core_data: SentraCoreCreate) -> SentraCoreModel:
        """Create a new SentraCore configuration."""
        try:
            # Convert to model with timestamps
            sentra_core_model = SentraCoreModel(
                name=sentra_core_data.name,
                description=sentra_core_data.description,
                labels=sentra_core_data.labels,
                connections=sentra_core_data.connections,
                selected_option=sentra_core_data.selected_option
            )
            
            # Insert into database
            result = await self.collection.insert_one(sentra_core_model.model_dump(by_alias=True))
            
            # Get the created document
            created_doc = await self.collection.find_one({"_id": result.inserted_id})
            return SentraCoreModel(**created_doc)
            
        except Exception as e:
            raise Exception(f"Error creating SentraCore configuration: {str(e)}")

    async def get_sentra_core_by_id(self, sentra_core_id: str) -> Optional[SentraCoreModel]:
        """Get a SentraCore configuration by ID."""
        try:
            if not ObjectId.is_valid(sentra_core_id):
                raise ValueError("Invalid ObjectId format")
                
            doc = await self.collection.find_one({"_id": ObjectId(sentra_core_id)})
            if doc:
                return SentraCoreModel(**doc)
            return None
            
        except Exception as e:
            raise Exception(f"Error retrieving SentraCore configuration: {str(e)}")

    async def get_all_sentra_core(self, skip: int = 0, limit: int = 100) -> List[SentraCoreModel]:
        """Get all SentraCore configurations with pagination."""
        try:
            cursor = self.collection.find().skip(skip).limit(limit).sort("created_at", -1)
            documents = await cursor.to_list(length=limit)
            return [SentraCoreModel(**doc) for doc in documents]
            
        except Exception as e:
            raise Exception(f"Error retrieving SentraCore configurations: {str(e)}")

    async def update_sentra_core(self, sentra_core_id: str, update_data: SentraCoreUpdate) -> Optional[SentraCoreModel]:
        """Update a SentraCore configuration."""
        try:
            if not ObjectId.is_valid(sentra_core_id):
                raise ValueError("Invalid ObjectId format")
            
            # Prepare update data
            update_dict = update_data.model_dump(exclude_unset=True)
            update_dict["updated_at"] = datetime.utcnow()
            
            # Update the document
            result = await self.collection.update_one(
                {"_id": ObjectId(sentra_core_id)},
                {"$set": update_dict}
            )
            
            if result.modified_count:
                # Return the updated document
                updated_doc = await self.collection.find_one({"_id": ObjectId(sentra_core_id)})
                return SentraCoreModel(**updated_doc)
            return None
            
        except Exception as e:
            raise Exception(f"Error updating SentraCore configuration: {str(e)}")

    async def delete_sentra_core(self, sentra_core_id: str) -> bool:
        """Delete a SentraCore configuration."""
        try:
            if not ObjectId.is_valid(sentra_core_id):
                raise ValueError("Invalid ObjectId format")
                
            result = await self.collection.delete_one({"_id": ObjectId(sentra_core_id)})
            return result.deleted_count > 0
            
        except Exception as e:
            raise Exception(f"Error deleting SentraCore configuration: {str(e)}")

    async def search_sentra_core_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[SentraCoreModel]:
        """Search SentraCore configurations by name."""
        try:
            cursor = self.collection.find(
                {"name": {"$regex": name, "$options": "i"}}
            ).skip(skip).limit(limit).sort("created_at", -1)
            
            documents = await cursor.to_list(length=limit)
            return [SentraCoreModel(**doc) for doc in documents]
            
        except Exception as e:
            raise Exception(f"Error searching SentraCore configurations: {str(e)}")

    async def get_sentra_core_count(self) -> int:
        """Get total count of SentraCore configurations."""
        try:
            return await self.collection.count_documents({})
        except Exception as e:
            raise Exception(f"Error counting SentraCore configurations: {str(e)}")

    async def save_current_state(self, name: str, labels: List, connections: List, selected_option: str, description: str = "") -> SentraCoreModel:
        """Save the current state from the frontend."""
        try:
            # Convert frontend data format to our model format
            converted_labels = []
            for label in labels:
                converted_labels.append({
                    "id": label.id,
                    "text": label.text,
                    "value": label.value,
                    "x": label.x,
                    "y": label.y,
                    "category": label.category
                })
            
            converted_connections = []
            for connection in connections:
                converted_connections.append({
                    "id": connection.id,
                    "from_id": connection.from_,  # FrontendConnection model maps 'from' to 'from_'
                    "to_id": connection.to
                })
            
            # Create the data
            sentra_core_data = SentraCoreCreate(
                name=name,
                description=description,
                labels=converted_labels,
                connections=converted_connections,
                selected_option=selected_option
            )
            # Save to database
            return await self.create_sentra_core(sentra_core_data)
            
        except Exception as e:
            raise Exception(f"Error saving current state: {str(e)}") 