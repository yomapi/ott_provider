def _set_foreign_key_suffix(data: dict, foreign_key_name: str) -> dict:
    """
    인스턴스 생성을 위해, _id 접미사를 붙혀줍니다.
    """
    fk_value = data[foreign_key_name]
    del data[foreign_key_name]
    fk_with_suffix = f"{foreign_key_name}_id"
    return {**data, fk_with_suffix: fk_value}


def set_multi_foreign_key_suffix(data: dict, foreign_key_names: list[str]) -> dict:
    """
    인스턴스 생성을 위해, 외부키 목록을 받아, _id 접미사를 붙혀줍니다.
    """
    for name in foreign_key_names:
        data = _set_foreign_key_suffix(data, name)
    return data
