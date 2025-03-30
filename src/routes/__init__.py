from .cpu_routes import router as cpu_router
from .ram_routes import router as ram_router
from .mainboard_routes import router as mainboard_router
from .storage_routes import router as storage_router
from .gpu_routes import router as gpu_router
from .case_routes import router as case_router
from .psu_routes import router as psu_router
from .admin_routes import router as admin_router

__all__ = [
    'cpu_router',
    'ram_router',
    'mainboard_router',
    'storage_router',
    'gpu_router',
    'case_router',
    'psu_router',
    'admin_router'
]
