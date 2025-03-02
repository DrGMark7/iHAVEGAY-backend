from fastapi import APIRouter, HTTPException, status
from src.controllers.psu_controller import PSUController
from src.models.hardware_models import PSU, UpdatePSU
from typing import List

router = APIRouter(
    prefix="/PSUs",
    tags=["PSUs"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "PSU not found",
            "content": {
                "application/json": {
                    "example": {"detail": "PSU not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = PSUController()

@router.get(
    "/", 
    response_model=List[PSU],
    summary="Get all PSUs",
    description="Retrieve a list of all Power Supply Units from the database",
    response_description="List of PSU objects"
)
async def get_psus():
    """
    Retrieve all PSUs from the database.
    
    Returns:
        List[PSU]: A list containing all PSU objects with their details:
        - psu_id: Unique identifier (starts with 7)
        - title: PSU name/model
        - price: Price in THB
        - Max_Watt: Maximum power output in watts
        - brand: Manufacturer
        - certs: Power supply certifications
        - grade: PSU rating/grade (0-5)
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no PSUs are found
    """
    return await controller.get_all()

@router.get(
    "/{psu_id}", 
    response_model=PSU,
    summary="Get PSU by ID",
    description="Retrieve a specific Power Supply Unit by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "PSU not found",
            "content": {
                "application/json": {
                    "example": {"detail": "PSU with specified ID not found"}
                }
            }
        }
    }
)
async def get_psu(psu_id: int):
    """
    Retrieve a specific PSU by its ID.
    
    Parameters:
        psu_id (int): The ID of the PSU to retrieve (must start with 7)
        
    Returns:
        PSU: The PSU object with the specified ID containing:
        - psu_id: Unique identifier
        - title: PSU name/model
        - price: Price in THB
        - Max_Watt: Maximum power output
        - brand: Manufacturer
        - certs: Certifications
        - grade: Rating/grade
        - imgUrl: Product image URL
        
    Raises:
        HTTPException(404): If PSU with specified ID is not found
    """
    return await controller.get_by_id(psu_id)

@router.post(
    "/", 
    response_model=dict,
    summary="Create new PSU",
    description="Add a new Power Supply Unit to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "PSU created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "PSU added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid PSU data"
        }
    }
)
async def create_psu(psu: PSU):
    """
    Create a new PSU in the database.
    
    Parameters:
        psu (PSU): PSU object containing:
        - psu_id: Unique identifier (must start with 7)
        - title: PSU name/model (non-empty string)
        - price: Price in THB (non-negative integer)
        - Max_Watt: Maximum power output (non-negative integer)
        - brand: Manufacturer (non-empty string)
        - certs: Power supply certifications (non-empty string)
        - grade: PSU rating/grade (0-5)
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new PSU ID
        
    Raises:
        HTTPException(400): If PSU data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create(psu)

@router.patch(
    "/{psu_id}", 
    response_model=dict,
    summary="Update PSU",
    description="Update an existing Power Supply Unit by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "PSU not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_psu(psu_id: int, psu: UpdatePSU):
    """
    Update a PSU in the database.
    
    Parameters:
        psu_id (int): The ID of the PSU to update
        psu (UpdatePSU): PSU update object containing optional fields:
        - title: New PSU name/model
        - price: New price
        - Max_Watt: New maximum power output
        - brand: New manufacturer
        - certs: New certifications
        - grade: New rating/grade
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If PSU with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update(psu_id, psu)

@router.delete(
    "/{psu_id}", 
    response_model=dict,
    summary="Delete PSU",
    description="Delete a Power Supply Unit from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "PSU not found"
        },
        status.HTTP_200_OK: {
            "description": "PSU deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "PSU deleted successfully",
                        "psu_id": 70001
                    }
                }
            }
        }
    }
)
async def delete_psu(psu_id: int):
    """
    Delete a PSU from the database.
    
    Parameters:
        psu_id (int): The ID of the PSU to delete
        
    Returns:
        dict: Message confirming deletion with PSU ID
        
    Raises:
        HTTPException(404): If PSU with specified ID is not found
    """
    return await controller.delete(psu_id)
