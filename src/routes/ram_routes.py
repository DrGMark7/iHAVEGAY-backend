from fastapi import APIRouter, HTTPException, status
from src.controllers.ram_controller import RamController
from src.models.hardware_models import Ram, UpdateRam
from typing import List

router = APIRouter(
    prefix="/RAMs",
    tags=["RAMs"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "RAM not found",
            "content": {
                "application/json": {
                    "example": {"detail": "RAM not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = RamController()

@router.get(
    "/", 
    response_model=List[Ram],
    summary="Get all RAMs",
    description="Retrieve a list of all RAM components from the database",
    response_description="List of RAM objects"
)
async def get_rams():
    """
    Retrieve all RAMs from the database.
    
    Returns:
        List[Ram]: A list containing all RAM objects with their details:
        - ram_id: Unique identifier (starts with 2)
        - title: RAM name/model
        - price: Price in THB
        - brand: Manufacturer
        - memory_type: Type of memory (e.g., DDR4)
        - speed: Memory speed in MHz
        - number_of_DIMMs: Number of memory modules
        - capacity_per_DIMM: Capacity per module in GB
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no RAMs are found
    """
    return await controller.get_all()

@router.get(
    "/{ram_id}", 
    response_model=Ram,
    summary="Get RAM by ID",
    description="Retrieve a specific RAM by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "RAM not found",
            "content": {
                "application/json": {
                    "example": {"detail": "RAM with specified ID not found"}
                }
            }
        }
    }
)
async def get_ram(ram_id: int):
    """
    Retrieve a specific RAM by its ID.
    
    Parameters:
        ram_id (int): The ID of the RAM to retrieve (must start with 2)
        
    Returns:
        Ram: The RAM object with the specified ID
        
    Raises:
        HTTPException(404): If RAM with specified ID is not found
    """
    return await controller.get_by_id(ram_id)

@router.post(
    "/", 
    response_model=dict,
    summary="Create new RAM",
    description="Add a new RAM to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "RAM created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "RAM added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid RAM data"
        }
    }
)
async def create_ram(ram: Ram):
    """
    Create a new RAM in the database.
    
    Parameters:
        ram (Ram): RAM object containing:
        - ram_id: Unique identifier (must start with 2)
        - title: RAM name/model
        - price: Price in THB
        - brand: Manufacturer
        - memory_type: Type of memory
        - speed: Memory speed
        - number_of_DIMMs: Number of modules
        - capacity_per_DIMM: Capacity per module
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new RAM ID
        
    Raises:
        HTTPException(400): If RAM data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create(ram)

@router.patch(
    "/{ram_id}", 
    response_model=dict,
    summary="Update RAM",
    description="Update an existing RAM by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "RAM not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_ram(ram_id: int, ram: UpdateRam):
    """
    Update a RAM in the database.
    
    Parameters:
        ram_id (int): The ID of the RAM to update
        ram (UpdateRam): RAM update object containing optional fields:
        - title: New RAM name/model
        - price: New price
        - brand: New manufacturer
        - memory_type: New memory type
        - speed: New speed
        - number_of_DIMMs: New number of modules
        - capacity_per_DIMM: New capacity per module
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If RAM with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update(ram_id, ram)

@router.delete(
    "/{ram_id}", 
    response_model=dict,
    summary="Delete RAM",
    description="Delete a RAM from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "RAM not found"
        },
        status.HTTP_200_OK: {
            "description": "RAM deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "RAM deleted successfully",
                        "ram_id": 20001
                    }
                }
            }
        }
    }
)
async def delete_ram(ram_id: int):
    """
    Delete a RAM from the database.
    
    Parameters:
        ram_id (int): The ID of the RAM to delete
        
    Returns:
        dict: Message confirming deletion with RAM ID
        
    Raises:
        HTTPException(404): If RAM with specified ID is not found
    """
    return await controller.delete(ram_id)
