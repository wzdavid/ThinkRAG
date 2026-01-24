# server/utils_json.py
# 注解：把任意 metadata 转成“可 JSON 序列化”的安全结构，避免 bs4.Tag 等对象导致 json.dumps 失败

from __future__ import annotations

from datetime import datetime, date
from pathlib import Path
from typing import Any


def sanitize_for_json(obj: Any) -> Any:
    """
    注解：
    - 递归处理 dict/list/tuple/set
    - 处理常见不可序列化对象：datetime/Path/bytes/bs4.Tag 等
    - 兜底：转成 str，保证 json.dumps 一定能过
    """
    # 基础类型：直接返回
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj

    # dict：递归处理 key/value（key 也强制转 str）
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[str(k)] = sanitize_for_json(v)
        return out

    # list/tuple/set：递归处理（set 转 list）
    if isinstance(obj, (list, tuple, set)):
        return [sanitize_for_json(x) for x in obj]

    # datetime/date：转 ISO 字符串
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    # Path：转字符串路径
    if isinstance(obj, Path):
        return str(obj)

    # bytes：尽量 decode
    if isinstance(obj, (bytes, bytearray)):
        try:
            return obj.decode("utf-8", errors="ignore")
        except Exception:
            return str(obj)

    # bs4.Tag / BeautifulSoup：通常有 get_text 方法
    # 注解：用 hasattr 不硬依赖 bs4 包，避免 import 失败
    if hasattr(obj, "get_text"):
        try:
            return obj.get_text(" ", strip=True)
        except Exception:
            return str(obj)

    # 兜底：字符串化
    return str(obj)

