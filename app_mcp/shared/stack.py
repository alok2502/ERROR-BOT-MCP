import re

def extract_stack_summary(stack: str) -> str:
    if not stack:
        return "No stack trace available"

    hits = []
    for line in stack.splitlines():
        if any(k in line for k in ("Controllers.", "Services.", "MyTE.")):
            m = re.search(r'([\w\.]+)\(', line)
            if m:
                hits.append(m.group(1))
            if len(hits) == 6:
                break

    return " → ".join(hits) if hits else "Stack trace available"
