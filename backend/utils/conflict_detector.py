from typing import List, Optional


def has_conflict(new_rule: dict, existing_rules: List[dict], exclude_id: Optional[int] = None) -> Optional[dict]:
    """
    Check if a new/updated rule has overlapping dimensions with existing rules.
    Returns the first conflicting rule if found, None otherwise.
    """
    for rule in existing_rules:
        if exclude_id is not None and rule["id"] == exclude_id:
            continue
        if rule["country"] != new_rule["country"]:
            continue
        if rule["productType"] != new_rule["productType"]:
            continue
        if _ranges_overlap(
            new_rule["weightMin"], new_rule["weightMax"],
            rule["weightMin"], rule["weightMax"]
        ):
            if _ranges_overlap(
                new_rule["lengthMin"], new_rule["lengthMax"],
                rule["lengthMin"], rule["lengthMax"]
            ) and _ranges_overlap(
                new_rule["widthMin"], new_rule["widthMax"],
                rule["widthMin"], rule["widthMax"]
            ) and _ranges_overlap(
                new_rule["heightMin"], new_rule["heightMax"],
                rule["heightMin"], rule["heightMax"]
            ):
                return rule
    return None


def _ranges_overlap(min1: float, max1: float, min2: float, max2: float) -> bool:
    return min1 < max2 and min2 < max1
