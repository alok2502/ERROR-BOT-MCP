from app_mcp.db.connection import get_conn


def fetch_grouped_errors(start, end):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
    SELECT 
        ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS error_id,
        COUNT(*) as count,
        Message,
        MIN(ErrorTime) as first_seen,
        MAX(ErrorTime) as last_seen,
        StackTrace
    FROM ApplicationErrors
    WHERE ErrorTime BETWEEN ? AND ?
    GROUP BY Message, StackTrace
    ORDER BY count DESC
    """

    cur.execute(sql, start, end)

    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]

def fetch_impacted_users(start, end, stack_like):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
    SELECT 
        UserId,
        Country,
        Company,
        Status,
        COUNT(*) as Errors
    FROM ApplicationErrors
    WHERE ErrorTime BETWEEN ? AND ?
      AND StackTrace LIKE ?
    GROUP BY UserId, Country, Company, Status
    """

    cur.execute(sql, start, end, stack_like)

    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]
