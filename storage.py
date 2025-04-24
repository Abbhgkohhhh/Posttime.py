# data/storage.py
from .models import Page

pending_pages: list[Page] = []
detailed_pages: dict[str, list[Page]] = {}
rated: dict[str, bool] = {}
