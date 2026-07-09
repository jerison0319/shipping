from fastapi import APIRouter, HTTPException
from utils.json_utils import read_json, write_json, next_id
from pydantic import BaseModel

router = APIRouter()

DATA_FILE = "product_types.json"


class ProductTypeCreate(BaseModel):
    name: str


class ProductTypeUpdate(BaseModel):
    name: str


@router.get("/product-types")
def list_product_types():
    return read_json(DATA_FILE)


@router.post("/product-types")
def create_product_type(data: ProductTypeCreate):
    types = read_json(DATA_FILE)
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="商品类型不能为空")
    for t in types:
        if t["name"].lower() == name.lower():
            raise HTTPException(status_code=400, detail="商品类型已存在")
    new_type = {"id": next_id(types), "name": name}
    types.append(new_type)
    write_json(DATA_FILE, types)
    return {"message": "商品类型创建成功", "product_type": new_type}


@router.put("/product-types/{type_id}")
def update_product_type(type_id: int, data: ProductTypeUpdate):
    types = read_json(DATA_FILE)
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="商品类型不能为空")
    for i, t in enumerate(types):
        if t["id"] == type_id:
            for other in types:
                if other["id"] != type_id and other["name"].lower() == name.lower():
                    raise HTTPException(status_code=400, detail="商品类型已存在")
            types[i]["name"] = name
            write_json(DATA_FILE, types)
            return {"message": "商品类型更新成功"}
    raise HTTPException(status_code=404, detail="商品类型不存在")


@router.delete("/product-types/{type_id}")
def delete_product_type(type_id: int):
    types = read_json(DATA_FILE)
    filtered = [t for t in types if t["id"] != type_id]
    if len(filtered) == len(types):
        raise HTTPException(status_code=404, detail="商品类型不存在")
    write_json(DATA_FILE, filtered)
    return {"message": "商品类型删除成功"}
