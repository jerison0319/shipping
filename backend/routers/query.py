from fastapi import APIRouter, HTTPException
from utils.json_utils import read_json
from pydantic import BaseModel

router = APIRouter()

DATA_FILE = "shipping_rules.json"


class QueryRequest(BaseModel):
    country: str
    productType: str
    productPrice: float
    lengthUnit: str = "cm"
    weightUnit: str = "g"
    length: float
    width: float
    height: float
    weight: float


@router.post("/query")
def query_price(req: QueryRequest):
    rules = read_json(DATA_FILE)

    matched = []
    for rule in rules:
        if rule["country"] != req.country:
            continue
        if rule["productType"] != req.productType:
            continue
        if not (rule["productPriceMin"] <= req.productPrice <= rule["productPriceMax"]):
            continue
        if rule.get("lengthUnit", "cm") != req.lengthUnit or rule.get("weightUnit", "g") != req.weightUnit:
            continue
        if not (rule["lengthMin"] <= req.length <= rule["lengthMax"]):
            continue
        if not (rule["widthMin"] <= req.width <= rule["widthMax"]):
            continue
        if not (rule["heightMin"] <= req.height <= rule["heightMax"]):
            continue
        if not (rule["weightMin"] <= req.weight <= rule["weightMax"]):
            continue
        matched.append(rule)

    if not matched:
        raise HTTPException(status_code=404, detail="未找到匹配的配送规则")

    # Return the cheapest matching rule
    matched.sort(key=lambda r: r["price"])
    best = matched[0]

    return {
        "matched": True,
        "country": best["country"],
        "productType": best["productType"],
        "productGrade": best.get("productGrade", ""),
        "productPriceMin": best.get("productPriceMin", 0),
        "productPriceMax": best.get("productPriceMax", 0),
        "lengthUnit": best.get("lengthUnit", "cm"),
        "weightUnit": best.get("weightUnit", "g"),
        "price": best["price"],
        "currency": best["currency"],
        "remark": best.get("remark", ""),
        "all_matches": [
            {
                "price": r["price"],
                "currency": r["currency"],
                "remark": r.get("remark", ""),
                "productGrade": r.get("productGrade", ""),
                "productPriceMin": r.get("productPriceMin", 0),
                "productPriceMax": r.get("productPriceMax", 0),
                "lengthUnit": r.get("lengthUnit", "cm"),
                "weightUnit": r.get("weightUnit", "g"),
            }
            for r in matched
        ],
    }
