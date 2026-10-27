-- SQL starter compatible with PostgreSQL and SQLite.
-- 1) Top categories by net revenue
SELECT category, SUM(net_revenue) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- 2) Estimated gross margin by channel
SELECT channel,
       SUM(net_revenue) AS revenue,
       SUM(net_revenue - cost) AS gross_margin
FROM sales
GROUP BY channel
ORDER BY gross_margin DESC;

-- 3) Customers with the highest cumulative revenue (LTV proxy)
SELECT customer_id,
       SUM(net_revenue) AS ltv_proxy,
       COUNT(*) AS orders
FROM sales
GROUP BY customer_id
ORDER BY ltv_proxy DESC
LIMIT 20;
