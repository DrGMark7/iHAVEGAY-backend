from fastapi import APIRouter, HTTPException, status
from src.controllers.cpu_controller import CPUController
from src.models.hardware_models import CPU, UpdateCPU
from typing import List

router = APIRouter(
    prefix="/CPUs",
    tags=["CPUs"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "CPU not found",
            "content": {
                "application/json": {
                    "example": {"detail": "CPU not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = CPUController()

@router.get(
    "/", 
    response_model=List[CPU],
    summary="Get all CPUs",
    description="Retrieve a list of all CPU components from the database",
    response_description="List of CPU objects"
)
async def get_cpus():
    """
    Retrieve all CPUs from the database.
    
    Returns:
        List[CPU]: A list containing all CPU objects with their details:
        - cpu_id: Unique identifier (starts with 1)
        - title: CPU name/model
        - price: Price in THB
        - Socket: CPU socket type
        - brand: Manufacturer (e.g., AMD, Intel)
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no CPUs are found
    """
    return await controller.get_all()

@router.get(
    "/{cpu_id}", 
    response_model=CPU,
    summary="Get CPU by ID",
    description="Retrieve a specific CPU by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "CPU not found",
            "content": {
                "application/json": {
                    "example": {"detail": "CPU with specified ID not found"}
                }
            }
        }
    }
)
async def get_cpu(cpu_id: int):
    """
    Retrieve a specific CPU by its ID.
    
    Parameters:
        cpu_id (int): The ID of the CPU to retrieve (must start with 1)
        
    Returns:
        CPU: The CPU object with the specified ID containing:
        - cpu_id: Unique identifier
        - title: CPU name/model
        - price: Price in THB
        - Socket: CPU socket type
        - brand: Manufacturer
        - imgUrl: Product image URL
        
    Raises:
        HTTPException(404): If CPU with specified ID is not found
    """
    return await controller.get_by_id(cpu_id)

@router.post(
    "/", 
    response_model=dict,
    summary="Create new CPU",
    description="Add a new CPU to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "CPU created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "CPU added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid CPU data"
        }
    }
)
async def create_cpu(cpu: CPU):
    """
    Create a new CPU in the database.
    
    Parameters:
        cpu (CPU): CPU object containing:
        - cpu_id: Unique identifier (must start with 1)
        - title: CPU name/model (non-empty string)
        - price: Price in THB (non-negative integer)
        - Socket: CPU socket type (non-empty string)
        - brand: Manufacturer (non-empty string)
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new CPU ID
        
    Raises:
        HTTPException(400): If CPU data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create(cpu)

@router.patch(
    "/{cpu_id}", 
    response_model=dict,
    summary="Update CPU",
    description="Update an existing CPU by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "CPU not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_cpu(cpu_id: int, cpu: UpdateCPU):
    """
    Update a CPU in the database.
    
    Parameters:
        cpu_id (int): The ID of the CPU to update
        cpu (UpdateCPU): CPU update object containing optional fields:
        - title: New CPU name/model
        - price: New price in THB
        - Socket: New CPU socket type
        - brand: New manufacturer
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If CPU with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update(cpu_id, cpu)

@router.delete(
    "/{cpu_id}", 
    response_model=dict,
    summary="Delete CPU",
    description="Delete a CPU from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "CPU not found"
        },
        status.HTTP_200_OK: {
            "description": "CPU deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "CPU deleted successfully",
                        "cpu_id": 10001
                    }
                }
            }
        }
    }
)
async def delete_cpu(cpu_id: int):
    """
    Delete a CPU from the database.
    
    Parameters:
        cpu_id (int): The ID of the CPU to delete
        
    Returns:
        dict: Message confirming deletion with CPU ID
        
    Raises:
        HTTPException(404): If CPU with specified ID is not found
    """
    return await controller.delete(cpu_id) 