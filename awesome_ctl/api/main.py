from fastapi import FastAPI
from loguru import logger
from awesome_ctl.api.routes import kubernetes

app = FastAPI()

app.include_router(kubernetes.k8s_router, prefix="/kubernetes", tags=["kubernetes"])


@app.on_event("startup")
async def startup_event():
    logger.info("Starting API up")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
