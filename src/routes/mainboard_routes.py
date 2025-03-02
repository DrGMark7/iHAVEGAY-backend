from fastapi import APIRouter, HTTPException, status
from src.controllers.mainboard_controller import MainboardController
from src.models.hardware_models import Mainboard, UpdateMainboard
from typing import List

router = APIRouter(
    prefix="/mainboards",
    tags=["Mainboards"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Mainboard not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Mainboard not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = MainboardController()

@router.get(
    "/", 
    response_model=List[Mainboard],
    summary="Get all Mainboards",
    description="Retrieve a list of all Mainboard components from the database",
    response_description="List of Mainboard objects"
)
async def get_mainboards():
    """
    Retrieve all Mainboards from the database.
    
    Returns:
        List[Mainboard]: A list containing all Mainboard objects with their details:
        - mainboard_id: Unique identifier (starts with 3)
        - title: Mainboard name/model
        - price: Price in THB
        - memory_type: Supported memory type (e.g., DDR4)
        - size: Form factor (e.g., ATX, Micro-ATX)
        - socket: CPU socket type
        - brand: Manufacturer
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no Mainboards are found
    """
    return await controller.get_all()

@router.get(
    "/{mainboard_id}", 
    response_model=Mainboard,
    summary="Get Mainboard by ID",
    description="Retrieve a specific Mainboard by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Mainboard not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Mainboard with specified ID not found"}
                }
            }
        }
    }
)
async def get_mainboard(mainboard_id: int):
    """
    Retrieve a specific Mainboard by its ID.
    
    Parameters:
        mainboard_id (int): The ID of the Mainboard to retrieve (must start with 3)
        
    Returns:
        Mainboard: The Mainboard object with the specified ID
        
    Raises:
        HTTPException(404): If Mainboard with specified ID is not found
    """
    return await controller.get_by_id(mainboard_id)

@router.post(
    "/", 
    response_model=dict,
    summary="Create new Mainboard",
    description="Add a new Mainboard to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Mainboard created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Mainboard added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Mainboard data"
        }
    }
)
async def create_mainboard(mainboard: Mainboard):
    """
    Create a new Mainboard in the database.
    
    Parameters:
        mainboard (Mainboard): Mainboard object containing:
        - mainboard_id: Unique identifier (must start with 3)
        - title: Mainboard name/model
        - price: Price in THB
        - memory_type: Supported memory type
        - size: Form factor
        - socket: CPU socket type
        - brand: Manufacturer
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new Mainboard ID
        
    Raises:
        HTTPException(400): If Mainboard data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create(mainboard)

@router.patch(
    "/{mainboard_id}", 
    response_model=dict,
    summary="Update Mainboard",
    description="Update an existing Mainboard by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Mainboard not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_mainboard(mainboard_id: int, mainboard: UpdateMainboard):
    """
    Update a Mainboard in the database.
    
    Parameters:
        mainboard_id (int): The ID of the Mainboard to update
        mainboard (UpdateMainboard): Mainboard update object containing optional fields:
        - title: New Mainboard name/model
        - price: New price
        - memory_type: New memory type
        - size: New form factor
        - socket: New CPU socket type
        - brand: New manufacturer
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If Mainboard with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update(mainboard_id, mainboard)

@router.delete(
    "/{mainboard_id}", 
    response_model=dict,
    summary="Delete Mainboard",
    description="Delete a Mainboard from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Mainboard not found"
        },
        status.HTTP_200_OK: {
            "description": "Mainboard deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Mainboard deleted successfully",
                        "mainboard_id": 30001
                    }
                }
            }
        }
    }
)
async def delete_mainboard(mainboard_id: int):
    """
    Delete a Mainboard from the database.
    
    Parameters:
        mainboard_id (int): The ID of the Mainboard to delete
        
    Returns:
        dict: Message confirming deletion with Mainboard ID
        
    Raises:
        HTTPException(404): If Mainboard with specified ID is not found
    """
    return await controller.delete(mainboard_id)
