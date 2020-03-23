from fastapi import APIRouter

root_router = APIRouter()

@root_router.get("/health")
def health():
    return {"heathy" : True}