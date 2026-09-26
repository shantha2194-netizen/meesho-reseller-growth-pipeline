-- ============================================================
-- MEESHO RESELLER GROWTH & ALERT INTELLIGENCE PIPELINE
-- PART 1 - SQL ANALYSIS
-- ============================================================


-- ============================================================
-- DATABASE VALIDATION
-- ============================================================

-- Check total number of resellers
SELECT COUNT(*) AS total_resellers
FROM resellers;


-- Check total number of orders
SELECT COUNT(*) AS total_orders
FROM orders;


-- Check available regions
SELECT DISTINCT region
FROM resellers
ORDER BY region;


-- Check available categories
SELECT DISTINCT category
FROM orders
ORDER BY category;


-- Check orders by month
SELECT
    month,
    COUNT(*) AS order_count
FROM orders
GROUP BY month
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END;


-- ============================================================
-- QUESTION 1
-- MONTHLY REVENUE BY CATEGORY
-- ============================================================

SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY
    month,
    category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;


-- ============================================================
-- QUESTION 2
-- REGION-WISE REVENUE AND ORDER COUNT
-- ============================================================

SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS revenue,
    COUNT(o.order_id) AS n_orders
FROM resellers r
JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY
    r.region
ORDER BY
    revenue DESC;


-- ============================================================
-- QUESTION 3
-- TOP 5 RESELLERS BY TOTAL SPEND
-- ============================================================

SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM resellers r
JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY
    r.reseller_id,
    r.reseller_name
HAVING
    total_spend > 50000
ORDER BY
    total_spend DESC
LIMIT 5;


-- ============================================================
-- QUESTION 4
-- ZERO-ORDER RESELLER
-- Demonstrates COUNT(*) vs COUNT(order_id)
-- ============================================================

SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS row_count,
    COUNT(o.order_id) AS order_count
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
GROUP BY
    r.reseller_id,
    r.reseller_name
HAVING
    COUNT(o.order_id) = 0;


-- ============================================================
-- QUESTION 5
-- JUNE DELIVERED AOV
-- ============================================================

SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE
    month = 'June'
    AND status = 'Delivered';