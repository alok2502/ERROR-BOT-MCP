def paginate(rows: list, page: int, page_size: int):
    start = (page - 1) * page_size
    end = start + page_size
    return rows[start:end], len(rows)


def page_info(page: int, page_size: int, total: int):
    total_pages = max(1, (total + page_size - 1) // page_size)
    start_idx = (page - 1) * page_size + 1 if total else 0
    end_idx = min(page * page_size, total)
    return start_idx, end_idx, total_pages
