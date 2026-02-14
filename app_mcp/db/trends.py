from app_mcp.db.connection import get_conn


def fetch_error_trend(start, end, stack_like):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
    SELECT 
        CAST(ErrorTime AS DATE) as day,
        COUNT(*) as count
    FROM ApplicationErrors
    WHERE ErrorTime BETWEEN ? AND ?
      AND StackTrace LIKE ?
    GROUP BY CAST(ErrorTime AS DATE)
    ORDER BY day
    """

    cur.execute(sql, start, end, stack_like)

    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]
