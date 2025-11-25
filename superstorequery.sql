-- SELECT
--     COUNT(order_id) AS total_transaksi,
--     COUNT(DISTINCT customer_id) AS jumlah_pelanggan,

--     SUM(NULLIF(regexp_replace(sales, '[^0-9.\-]', '', 'g'), '')::float) AS total_penjualan,
--     AVG(NULLIF(regexp_replace(profit, '[^0-9.\-]', '', 'g'), '')::float) AS rata_rata_profit,

--     MAX(NULLIF(regexp_replace(sales, '[^0-9.\-]', '', 'g'), '')::float) AS penjualan_tertinggi,
--     MIN(NULLIF(regexp_replace(profit, '[^0-9.\-]', '', 'g'), '')::float) AS keuntungan_terendah

-- FROM superstore_order;

-- SELECT
--     customer_id,
--     customer_name,
--     UPPER(customer_name) AS nama_besar,
--     LOWER(customer_name) AS nama_kecil,
--     INITCAP(customer_name) AS kapital_awal
-- FROM superstore_customer
-- LIMIT 3;

-- SELECT
--     order_date,
--     EXTRACT(YEAR FROM order_date::date) AS tahun,
--     EXTRACT(MONTH FROM order_date::date) AS bulan,
--     TO_CHAR(order_date::date, 'Day') AS nama_hari,
--     TO_CHAR(order_date::date, 'YYYY-MM-DD') AS format_rapi
-- FROM superstore_order
-- LIMIT 3;

-- SELECT
--     order_id,
--     (regexp_replace(sales, '[^0-9.\-]', '', 'g')::float) AS sales_asli,
--     ROUND(regexp_replace(sales, '[^0-9.\-]', '', 'g')::float) AS sales_bulat,
--     ABS(regexp_replace(sales, '[^0-9.\-]', '', 'g')::float) AS sales_absolut,
--     FLOOR(regexp_replace(sales, '[^0-9.\-]', '', 'g')::float) AS sales_bawah
-- FROM superstore_order
-- LIMIT 3;

-- SELECT
--     order_id,
--     (regexp_replace(sales, '[^0-9.\-]', '', 'g')::float) AS sales_asli,
--     CASE
--         WHEN (regexp_replace(sales, '[^0-9.\-]', '', 'g')::float) > 500 THEN 'Tinggi'
--         WHEN (regexp_replace(sales, '[^0-9.\-]', '', 'g')::float) >= 100 THEN 'Sedang'
--         ELSE 'Rendah'
--     END AS kategori_sales
-- FROM superstore_order
-- LIMIT 3;

-- SELECT
--     order_id,
--     customer_id,
--     region
-- FROM superstore_order
-- WHERE region = 'West'
-- LIMIT 3;

-- SELECT
--     order_id,
--     NULLIF(regexp_replace(sales, '[^0-9.\-]', '', 'g'), '')::float AS sales
-- FROM superstore_order
-- ORDER BY NULLIF(regexp_replace(sales, '[^0-9.\-]', '', 'g'), '')::float ASC
-- LIMIT 3;

-- SELECT
--     region,
--     COUNT(*) AS jumlah_order
-- FROM superstore_order
-- GROUP BY region
-- ORDER BY jumlah_order DESC;
