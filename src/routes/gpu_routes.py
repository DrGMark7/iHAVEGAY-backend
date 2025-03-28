from fastapi import APIRouter, HTTPException, status
from src.controllers.gpu_controller import GPUController
from src.models.hardware_models import GPU, UpdateGPU
from typing import List

router = APIRouter(
    prefix="/GPUs",
    tags=["GPUs"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "GPU not found",
            "content": {
                "application/json": {
                    "example": {"detail": "GPU not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = GPUController()

@router.get(
    "/", 
    response_model=List[GPU],
    summary="Get all GPUs",
    description="Retrieve a list of all GPU components from the database",
    response_description="List of GPU objects"
)
async def get_gpus():
    """
    Retrieve all GPUs from the database.
    
    Returns:
        List[GPU]: A list containing all GPU objects with their details:
        - gpu_id: Unique identifier (starts with 5)
        - title: GPU name/model
        - price: Price in THB
        - series: GPU series (e.g., RTX 4000, RX 7000)
        - ram_capacity_GB: VRAM capacity in GB
        - brand: Manufacturer (e.g., ASUS, MSI, Gigabyte)
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no GPUs are found
    """
    return await controller.get_all()

@router.get(
    "/{gpu_id}", 
    response_model=GPU,
    summary="Get GPU by ID",
    description="Retrieve a specific GPU by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "GPU not found",
            "content": {
                "application/json": {
                    "example": {"detail": "GPU with specified ID not found"}
                }
            }
        }
    }
)
async def get_gpu(gpu_id: int):
    """
    Retrieve a specific GPU by its ID.
    
    Parameters:
        gpu_id (int): The ID of the GPU to retrieve (must start with 5)
        
    Returns:
        GPU: The GPU object with the specified ID containing:
        - gpu_id: Unique identifier
        - title: GPU name/model
        - price: Price in THB
        - series: GPU series
        - ram_capacity_GB: VRAM capacity
        - brand: Manufacturer
        - imgUrl: Product image URL
        
    Raises:
        HTTPException(404): If GPU with specified ID is not found
    """
    return await controller.get_by_id(gpu_id)

@router.post(
    "/", 
    response_model=dict,
    summary="Create new GPU",
    description="Add a new GPU to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "GPU created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "GPU added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid GPU data"
        }
    }
)
async def create_gpu(gpu: GPU):
    """
    Create a new GPU in the database.
    
    Parameters:
        gpu (GPU): GPU object containing:
        - gpu_id: Unique identifier (must start with 5)
        - title: GPU name/model (non-empty string)
        - price: Price in THB (non-negative integer)
        - series: GPU series (non-empty string)
        - ram_capacity_GB: VRAM capacity in GB (non-negative integer)
        - brand: Manufacturer (non-empty string)
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new GPU ID
        
    Raises:
        HTTPException(400): If GPU data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create(gpu)

@router.patch(
    "/{gpu_id}", 
    response_model=dict,
    summary="Update GPU",
    description="Update an existing GPU by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "GPU not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_gpu(gpu_id: int, gpu: UpdateGPU):
    """
    Update a GPU in the database.
    
    Parameters:
        gpu_id (int): The ID of the GPU to update
        gpu (UpdateGPU): GPU update object containing optional fields:
        - title: New GPU name/model
        - price: New price in THB
        - series: New GPU series
        - ram_capacity_GB: New VRAM capacity
        - brand: New manufacturer
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If GPU with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update(gpu_id, gpu)

@router.delete(
    "/{gpu_id}", 
    response_model=dict,
    summary="Delete GPU",
    description="Delete a GPU from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "GPU not found"
        },
        status.HTTP_200_OK: {
            "description": "GPU deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "GPU deleted successfully",
                        "gpu_id": 50001
                    }
                }
            }
        }
    }
)
async def delete_gpu(gpu_id: int):
    """
    Delete a GPU from the database.
    
    Parameters:
        gpu_id (int): The ID of the GPU to delete
        
    Returns:
        dict: Message confirming deletion with GPU ID
        
    Raises:
        HTTPException(404): If GPU with specified ID is not found
    """
    return await controller.delete(gpu_id)
