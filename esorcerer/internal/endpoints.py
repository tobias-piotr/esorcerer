from fastapi import APIRouter, status

router = APIRouter(tags=["internal"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def check_health():
    """Check health status."""
    return {"detail": "Ok"}
