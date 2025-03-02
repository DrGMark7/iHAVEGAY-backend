from fastapi import APIRouter, HTTPException, status
from src.controllers.storage_controller import StorageController
from src.models.hardware_models import SSD, M2, UpdateSSD, UpdateM2
from typing import List

router = APIRouter(
    prefix="/storage",
    tags=["Storage"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Storage device not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Storage device not found"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal server error",
        }
    }
)

controller = StorageController()

# SSD Routes
@router.get(
    "/ssds", 
    response_model=List[SSD],
    summary="Get all SSDs",
    description="Retrieve a list of all SSD storage devices from the database",
    response_description="List of SSD objects"
)
async def get_ssds():
    """
    Retrieve all SSDs from the database.
    
    Returns:
        List[SSD]: A list containing all SSD objects with their details:
        - ssd_id: Unique identifier (starts with 42)
        - title: SSD name/model
        - price: Price in THB
        - brand: Manufacturer
        - size_GB: Storage capacity in GB
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no SSDs are found
    """
    return await controller.get_all_ssds()

@router.get(
    "/ssds/{ssd_id}", 
    response_model=SSD,
    summary="Get SSD by ID",
    description="Retrieve a specific SSD by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "SSD not found",
            "content": {
                "application/json": {
                    "example": {"detail": "SSD with specified ID not found"}
                }
            }
        }
    }
)
async def get_ssd(ssd_id: int):
    """
    Retrieve a specific SSD by its ID.
    
    Parameters:
        ssd_id (int): The ID of the SSD to retrieve (must start with 42)
        
    Returns:
        SSD: The SSD object with the specified ID
        
    Raises:
        HTTPException(404): If SSD with specified ID is not found
    """
    return await controller.get_ssd_by_id(ssd_id)

@router.post(
    "/ssds", 
    response_model=dict,
    summary="Create new SSD",
    description="Add a new SSD to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "SSD created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "SSD added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid SSD data"
        }
    }
)
async def create_ssd(ssd: SSD):
    """
    Create a new SSD in the database.
    
    Parameters:
        ssd (SSD): SSD object containing:
        - ssd_id: Unique identifier (must start with 42)
        - title: SSD name/model
        - price: Price in THB
        - brand: Manufacturer
        - size_GB: Storage capacity in GB
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new SSD ID
        
    Raises:
        HTTPException(400): If SSD data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create_ssd(ssd)

@router.patch(
    "/ssds/{ssd_id}", 
    response_model=dict,
    summary="Update SSD",
    description="Update an existing SSD by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "SSD not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_ssd(ssd_id: int, ssd: UpdateSSD):
    """
    Update an SSD in the database.
    
    Parameters:
        ssd_id (int): The ID of the SSD to update
        ssd (UpdateSSD): SSD update object containing optional fields:
        - title: New SSD name/model
        - price: New price
        - brand: New manufacturer
        - size_GB: New storage capacity
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If SSD with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update_ssd(ssd_id, ssd)

@router.delete(
    "/ssds/{ssd_id}", 
    response_model=dict,
    summary="Delete SSD",
    description="Delete an SSD from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "SSD not found"
        },
        status.HTTP_200_OK: {
            "description": "SSD deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "SSD deleted successfully",
                        "ssd_id": 42001
                    }
                }
            }
        }
    }
)
async def delete_ssd(ssd_id: int):
    """
    Delete an SSD from the database.
    
    Parameters:
        ssd_id (int): The ID of the SSD to delete
        
    Returns:
        dict: Message confirming deletion with SSD ID
        
    Raises:
        HTTPException(404): If SSD with specified ID is not found
    """
    return await controller.delete_ssd(ssd_id)

# M.2 Routes
@router.get(
    "/m2s", 
    response_model=List[M2],
    summary="Get all M.2 drives",
    description="Retrieve a list of all M.2 storage devices from the database",
    response_description="List of M.2 objects"
)
async def get_m2s():
    """
    Retrieve all M.2 drives from the database.
    
    Returns:
        List[M2]: A list containing all M.2 objects with their details:
        - m2_id: Unique identifier (starts with 43)
        - title: M.2 drive name/model
        - price: Price in THB
        - read: Read speed
        - write: Write speed
        - brand: Manufacturer
        - capacity: Storage capacity in GB
        - imgUrl: Product image URL
    
    Raises:
        HTTPException(404): If no M.2 drives are found
    """
    return await controller.get_all_m2s()

@router.get(
    "/m2s/{m2_id}", 
    response_model=M2,
    summary="Get M.2 drive by ID",
    description="Retrieve a specific M.2 drive by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "M.2 drive not found",
            "content": {
                "application/json": {
                    "example": {"detail": "M.2 drive with specified ID not found"}
                }
            }
        }
    }
)
async def get_m2(m2_id: int):
    """
    Retrieve a specific M.2 drive by its ID.
    
    Parameters:
        m2_id (int): The ID of the M.2 drive to retrieve (must start with 43)
        
    Returns:
        M2: The M.2 drive object with the specified ID
        
    Raises:
        HTTPException(404): If M.2 drive with specified ID is not found
    """
    return await controller.get_m2_by_id(m2_id)

@router.post(
    "/m2s", 
    response_model=dict,
    summary="Create new M.2 drive",
    description="Add a new M.2 drive to the database",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {
            "description": "M.2 drive created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "M.2 drive added successfully",
                        "id": "123456789"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid M.2 drive data"
        }
    }
)
async def create_m2(m2: M2):
    """
    Create a new M.2 drive in the database.
    
    Parameters:
        m2 (M2): M.2 drive object containing:
        - m2_id: Unique identifier (must start with 43)
        - title: M.2 drive name/model
        - price: Price in THB
        - read: Read speed
        - write: Write speed
        - brand: Manufacturer
        - capacity: Storage capacity in GB
        - imgUrl: Product image URL
        
    Returns:
        dict: Message confirming creation with new M.2 drive ID
        
    Raises:
        HTTPException(400): If M.2 drive data is invalid
        HTTPException(500): If database operation fails
    """
    return await controller.create_m2(m2)

@router.patch(
    "/m2s/{m2_id}", 
    response_model=dict,
    summary="Update M.2 drive",
    description="Update an existing M.2 drive by its ID",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "M.2 drive not found"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid update data"
        }
    }
)
async def update_m2(m2_id: int, m2: UpdateM2):
    """
    Update an M.2 drive in the database.
    
    Parameters:
        m2_id (int): The ID of the M.2 drive to update
        m2 (UpdateM2): M.2 drive update object containing optional fields:
        - title: New M.2 drive name/model
        - price: New price
        - read: New read speed
        - write: New write speed
        - brand: New manufacturer
        - capacity: New storage capacity
        - imgUrl: New product image URL
        
    Returns:
        dict: Message confirming update with modified fields
        
    Raises:
        HTTPException(404): If M.2 drive with specified ID is not found
        HTTPException(400): If update data is invalid
    """
    return await controller.update_m2(m2_id, m2)

@router.delete(
    "/m2s/{m2_id}", 
    response_model=dict,
    summary="Delete M.2 drive",
    description="Delete an M.2 drive from the database",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "M.2 drive not found"
        },
        status.HTTP_200_OK: {
            "description": "M.2 drive deleted successfully",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "M.2 drive deleted successfully",
                        "m2_id": 43001
                    }
                }
            }
        }
    }
)
async def delete_m2(m2_id: int):
    """
    Delete an M.2 drive from the database.
    
    Parameters:
        m2_id (int): The ID of the M.2 drive to delete
        
    Returns:
        dict: Message confirming deletion with M.2 drive ID
        
    Raises:
        HTTPException(404): If M.2 drive with specified ID is not found
    """
    return await controller.delete_m2(m2_id)
