from fastapi import APIRouter, HTTPException, status
from src.controllers.case_controller import CaseController
from src.models.hardware_models import Case, UpdateCase
from typing import List

router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Case not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Case not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = CaseController()

@router.get(
    "/", 
    response_model=List[Case],
    summary="Get all Cases",
    description="Retrieve a list of all PC Cases from the database",
    response_description="List of Case objects"
)
async def get_cases():
    """
    Retrieve all PC Cases from the database.
    
    Returns:
        List[Case]: A list containing all Case objects with their details:
        - case_id: Unique identifier (starts with 6)
        - title: Case name/model
        - price: Price in THB
        - brand: Manufacturer
        - support_mb: List of supported motherboard form factors
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no Cases are found
    """
    return await controller.get_all()

@router.get(
    "/{case_id}", 
    response_model=Case,
    summary="Get Case by ID",
    description="Retrieve a specific PC Case by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Case not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Case with specified ID not found"}
                }
            }
        }
    }
)
async def get_case(case_id: int):
    """
    Retrieve a specific PC Case by its ID.
    
    Parameters:
        case_id (int): The ID of the Case to retrieve (must start with 6)
        
    Returns:
        Case: The Case object with the specified ID containing:
        - case_id: Unique identifier
        - title: Case name/model
        - price: Price in THB
        - brand: Manufacturer
        - support_mb: Supported motherboard form factors
        - imgUrl: Product image URL
        
    Raises:
        HTTPException(404): If Case with specified ID is not found
    """
    return await controller.get_by_id(case_id)

@router.post(
    "/", 
    response_model=dict,
    summary="Create new Case",
    description="Add a new PC Case to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Case created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Case added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid Case data"
        }
    }
)
async def create_case(case: Case):
    """
    Create a new PC Case in the database.
    
    Parameters:
        case (Case): Case object containing:
        - case_id: Unique identifier (must start with 6)
        - title: Case name/model (non-empty string)
        - price: Price in THB (non-negative integer)
        - brand: Manufacturer (non-empty string)
        - support_mb: List of supported motherboard form factors
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new Case ID
        
    Raises:
        HTTPException(400): If Case data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create(case)

@router.patch(
    "/{case_id}", 
    response_model=dict,
    summary="Update Case",
    description="Update an existing PC Case by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Case not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_case(case_id: int, case: UpdateCase):
    """
    Update a PC Case in the database.
    
    Parameters:
        case_id (int): The ID of the Case to update
        case (UpdateCase): Case update object containing optional fields:
        - title: New Case name/model
        - price: New price
        - brand: New manufacturer
        - support_mb: New list of supported motherboard form factors
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If Case with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update(case_id, case)

@router.delete(
    "/{case_id}", 
    response_model=dict,
    summary="Delete Case",
    description="Delete a PC Case from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Case not found"
        },
        status.HTTP_200_OK: {
            "description": "Case deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Case deleted successfully",
                        "case_id": 60001
                    }
                }
            }
        }
    }
)
async def delete_case(case_id: int):
    """
    Delete a PC Case from the database.
    
    Parameters:
        case_id (int): The ID of the Case to delete
        
    Returns:
        dict: Message confirming deletion with Case ID
        
    Raises:
        HTTPException(404): If Case with specified ID is not found
    """
    return await controller.delete(case_id)
