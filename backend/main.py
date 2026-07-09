import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import rules, countries, product_types, query, excel

app = FastAPI(title="International Shipping Price Query System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rules.router, prefix="/api", tags=["Rules"])
app.include_router(countries.router, prefix="/api", tags=["Countries"])
app.include_router(product_types.router, prefix="/api", tags=["Product Types"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(excel.router, prefix="/api", tags=["Excel"])


@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
