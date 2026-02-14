import re


def extract_stack_fingerprint(stack: str, max_items: int = 5):
    if not stack:
        return []

    lines = stack.splitlines()
    results = []

    for line in lines:
        m = re.search(r'([\w\.]+)\(', line)
        if m:
            results.append(m.group(1).split('.')[-1])
        if len(results) >= max_items:
            break

    return results


def extract_stack_signature(stack: str):
    return " > ".join(extract_stack_fingerprint(stack))


def build_error_table(rows: list[dict], max_rows: int = 20):
    header = "| ID | Count | Message |\n|----|-------|---------|\n"
    body = ""

    for r in rows[:max_rows]:
        body += f"| {r['error_id']} | {r.get('count',0)} | {r.get('message','')[:80]} |\n"

    return header + body
