import re
from collections import Counter
from app_mcp.deps import TZ_LOCAL, TZ_UTC, ist_fmt


# -----------------------------
# Errors table (list_errors)
# -----------------------------
def build_errors_table_md(rows: list[dict], max_rows: int) -> str:
    header = "| ID | Errors | Message | First Seen | Last Seen |\n"
    header += "|---:|---:|---|---|---|\n"

    lines = []
    for r in rows[:max_rows]:
        msg = str(r.get("Message", "")).replace("|", "\\|")
        if len(msg) > 200:
            msg = msg[:200] + " …"

        first_utc = r.get("minErrorRaisedDttm")
        last_utc = r.get("maxErrorRaisedDttm")

        first_ist = (
            first_utc.replace(tzinfo=TZ_UTC).astimezone(TZ_LOCAL)
            if first_utc else None
        )
        last_ist = (
            last_utc.replace(tzinfo=TZ_UTC).astimezone(TZ_LOCAL)
            if last_utc else None
        )

        lines.append(
            f"| {r['error_id']} | {r['Errors']} | {msg} | "
            f"{ist_fmt(first_ist)} | {ist_fmt(last_ist)} |"
        )

    table = header + "\n".join(lines)

    if len(rows) > max_rows:
        table += f"\n\n_Showing top {max_rows}; {len(rows) - max_rows} more omitted._"

    return table


# -----------------------------
# Stack trace summary
# -----------------------------
def extract_stack_summary(stack: str) -> str:
    if not stack:
        return "No stack trace available"

    lines = stack.splitlines()
    hits = []

    for l in lines:
        if any(x in l for x in ["MyTE.", "Controllers.", "Services.", "Strategies"]):
            m = re.search(r'([\w\.]+)\(', l)
            if m:
                hits.append(m.group(1))
            if len(hits) == 6:
                break

    return " → ".join(hits) if hits else "Stack trace available (use 'show full stack')"


# -----------------------------
# Error details markdown
# -----------------------------
def build_error_details_md(row: dict) -> str:
    stack_summary = extract_stack_summary(row.get("StackTraceDesc"))

    return f"""
### 🚨 Error Details (ID {row['error_id']})

**Message:** {row.get('Message')}  
**Total Occurrences:** {row.get('Errors')}  
**First Seen:** {ist_fmt(row.get('minErrorRaisedDttm'))}  
**Last Seen:** {ist_fmt(row.get('maxErrorRaisedDttm'))}  

**Stack Fingerprint:** `{row.get('stack_fingerprint', 'N/A')}`  
**Stack Summary:** {stack_summary}
"""


# -----------------------------
# Impacted users table
# -----------------------------
def build_impacted_users_md(
    error_id: int,
    users: list[dict],
    start_dt,
    end_dt,
    max_rows: int = 10,
) -> str:
    header = f"""
### 👥 Impacted Users — Error ID {error_id}

**Total impacted users:** {len(users)}  
**Time window:** {ist_fmt(start_dt)} → {ist_fmt(end_dt)} (IST)
"""

    if not users:
        return header + "\n_No impacted users found._"

    table = "| User | Country | Company | Period | Status | Errors |\n"
    table += "|------|---------|---------|--------|--------|--------|\n"

    for u in users[:max_rows]:
        period = (
            u["PeriodEndDttm"].strftime("%Y-%m-%d")
            if u.get("PeriodEndDttm") else "N/A"
        )

        table += (
            f"| {u.get('EnterpriseId')} "
            f"| {u.get('CountryKey')} "
            f"| {u.get('CompanyCd')} "
            f"| {period} "
            f"| {u.get('Status')} "
            f"| {u.get('Errors')} |\n"
        )

    if len(users) > max_rows:
        table += (
            f"\n_Showing top {max_rows} users. "
            f"Use **export impacted users** for full list._"
        )

    return header + "\n" + table
