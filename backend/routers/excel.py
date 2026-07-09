from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from utils.json_utils import read_json, write_json, next_id
from utils.excel_utils import export_rules_to_excel, parse_excel_to_rules

router = APIRouter()

DATA_FILE = "shipping_rules.json"


@router.get("/export-excel")
async def export_excel():
    rules = read_json(DATA_FILE)
    output = export_rules_to_excel(rules)
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=shipping_rules.xlsx"},
    )


@router.post("/import-excel")
async def import_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="请上传 .xlsx 文件")

    content = await file.read()
    try:
        imported_rules = parse_excel_to_rules(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"解析 Excel 失败: {str(e)}")

    if not imported_rules:
        raise HTTPException(status_code=400, detail="Excel 中没有有效数据")

    existing = read_json(DATA_FILE)
    start_id = next_id(existing)

    for i, rule in enumerate(imported_rules):
        rule["id"] = start_id + i
        existing.append(rule)

    write_json(DATA_FILE, existing)

    return {
        "message": f"成功导入 {len(imported_rules)} 条规则",
        "count": len(imported_rules),
    }
