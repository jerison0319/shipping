from fastapi import APIRouter, HTTPException
from utils.json_utils import read_json, write_json, next_id
from pydantic import BaseModel

router = APIRouter()

DATA_FILE = "countries.json"


class CountryCreate(BaseModel):
    name: str
    currency: str


class CountryUpdate(BaseModel):
    name: str
    currency: str


@router.get("/countries")
def list_countries():
    return read_json(DATA_FILE)


@router.post("/countries")
def create_country(data: CountryCreate):
    countries = read_json(DATA_FILE)
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="国家名称不能为空")
    for c in countries:
        if c["name"].lower() == name.lower():
            raise HTTPException(status_code=400, detail="国家已存在")
    new_country = {"id": next_id(countries), "name": name, "currency": data.currency}
    countries.append(new_country)
    write_json(DATA_FILE, countries)
    return {"message": "国家创建成功", "country": new_country}


@router.put("/countries/{country_id}")
def update_country(country_id: int, data: CountryUpdate):
    countries = read_json(DATA_FILE)
    name = data.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="国家名称不能为空")
    for i, c in enumerate(countries):
        if c["id"] == country_id:
            for other in countries:
                if other["id"] != country_id and other["name"].lower() == name.lower():
                    raise HTTPException(status_code=400, detail="国家已存在")
            countries[i]["name"] = name
            countries[i]["currency"] = data.currency
            write_json(DATA_FILE, countries)
            return {"message": "国家更新成功"}
    raise HTTPException(status_code=404, detail="国家不存在")


@router.delete("/countries/{country_id}")
def delete_country(country_id: int):
    countries = read_json(DATA_FILE)
    filtered = [c for c in countries if c["id"] != country_id]
    if len(filtered) == len(countries):
        raise HTTPException(status_code=404, detail="国家不存在")
    write_json(DATA_FILE, filtered)
    return {"message": "国家删除成功"}
