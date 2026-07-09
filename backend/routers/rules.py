from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from typing import Optional
from utils.json_utils import read_json, write_json, next_id
from utils.conflict_detector import has_conflict
from pydantic import BaseModel

router = APIRouter()

DATA_FILE = "shipping_rules.json"


class RuleCreate(BaseModel):
    country: str
    productType: str
    productGrade: str
    productPriceMin: float
    productPriceMax: float
    lengthUnit: str = "cm"
    weightUnit: str = "g"
    lengthMin: float
    lengthMax: float
    widthMin: float
    widthMax: float
    heightMin: float
    heightMax: float
    weightMin: float
    weightMax: float
    price: float
    currency: str
    remark: str = ""
    force: bool = False


class RuleUpdate(BaseModel):
    country: str
    productType: str
    productGrade: str
    productPriceMin: float
    productPriceMax: float
    lengthUnit: str = "cm"
    weightUnit: str = "g"
    lengthMin: float
    lengthMax: float
    widthMin: float
    widthMax: float
    heightMin: float
    heightMax: float
    weightMin: float
    weightMax: float
    price: float
    currency: str
    remark: str = ""
    force: bool = False


@router.get("/rules")
def list_rules(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    country: Optional[str] = None,
    product_type: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc",
):
    rules = read_json(DATA_FILE)

    if country:
        rules = [r for r in rules if r["country"] == country]
    if product_type:
        rules = [r for r in rules if r["productType"] == product_type]
    if search:
        search_lower = search.lower()
        rules = [
            r for r in rules
            if search_lower in r["country"].lower()
            or search_lower in r["productType"].lower()
            or search_lower in r.get("remark", "").lower()
        ]

    if sort_by and sort_by in ("country", "productType", "price", "currency"):
        reverse = sort_order == "desc"
        rules.sort(key=lambda r: str(r.get(sort_by, "")), reverse=reverse)

    total = len(rules)
    start = (page - 1) * page_size
    end = start + page_size
    items = rules[start:end]

    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.post("/rules")
def create_rule(rule: RuleCreate):
    rules = read_json(DATA_FILE)

    new_rule = rule.model_dump()
    new_rule.pop("force", None)

    if not rule.force:
        conflict = has_conflict(new_rule, rules)
        if conflict:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "发现规则区间重叠，是否继续保存？",
                    "conflict": conflict
                }
            )

    new_rule["id"] = next_id(rules)
    rules.append(new_rule)
    write_json(DATA_FILE, rules)
    return {"message": "规则创建成功", "rule": new_rule}


@router.put("/rules/{rule_id}")
def update_rule(rule_id: int, rule: RuleUpdate):
    rules = read_json(DATA_FILE)

    for i, r in enumerate(rules):
        if r["id"] == rule_id:
            updated = rule.model_dump()
            updated.pop("force", None)
            updated["id"] = rule_id

            if not rule.force:
                conflict = has_conflict(updated, rules, exclude_id=rule_id)
                if conflict:
                    raise HTTPException(
                        status_code=409,
                        detail={
                            "message": "发现规则区间重叠，是否继续保存？",
                            "conflict": conflict
                        }
                    )

            rules[i] = updated
            write_json(DATA_FILE, rules)
            return {"message": "规则更新成功", "rule": updated}

    raise HTTPException(status_code=404, detail="规则不存在")


@router.delete("/rules/{rule_id}")
def delete_rule(rule_id: int):
    rules = read_json(DATA_FILE)
    filtered = [r for r in rules if r["id"] != rule_id]
    if len(filtered) == len(rules):
        raise HTTPException(status_code=404, detail="规则不存在")
    write_json(DATA_FILE, filtered)
    return {"message": "规则删除成功"}


@router.post("/rules/batch-delete")
def batch_delete_rules(ids: List[int]):
    rules = read_json(DATA_FILE)
    filtered = [r for r in rules if r["id"] not in ids]
    write_json(DATA_FILE, filtered)
    return {"message": f"已删除 {len(rules) - len(filtered)} 条规则"}
