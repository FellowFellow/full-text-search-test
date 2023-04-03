import sys
sys.path.append(".")

from fastapi import FastAPI

app = FastAPI(title="FTS-Test", description="Full Text Search test api server", docs_url="/")


from api.routers.doc_router.router import router as document_router

app.include_router(document_router)





if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="api:app", reload=True, reload_dirs=["api/db", "api/routers"])



