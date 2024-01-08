/* This file will be used to run SQL queries on the sales_data database to return useful business information to the owner.*/


/* 1. How many stores does the business have and in which countries?

The Operations team would like to know which countries we currently 
operate in and which country now has the most stores.  */

SELECT country_code AS country,
COUNT(country_code) AS total_num_stores
FROM dim_store_details
GROUP BY country 
ORDER BY total_num_stores DESC;

/* 2. Which locations currently have the most stores? 
The business stakeholders want to know.*/

SELECT locality,
COUNT(locality) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC;


/* 3. Which months produced the largest amount of sales?*/

SELECT SUM(dim_products.product_price_sterling * orders_table.product_quantity) AS total_sales,
month
FROM dim_date_times
INNER JOIN orders_table ON dim_date_times.date_uuid = orders_table.date_uuid
INNER JOIN dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY dim_date_times.month
ORDER BY total_sales DESC;

/* 4. Calculate how many products were sold and the amount of sales made for online and offline purchases.*/

SELECT * FROM dim_store_details;

-- Add column for 'offline' vs 'online'
ALTER TABLE dim_store_details
ADD COLUMN location VARCHAR(7);

-- Note store_types
SELECT DISTINCT store_type 
FROM dim_store_details;

-- Create case to fill location colum
UPDATE dim_store_details
SET location =
	CASE 
		WHEN store_type IN ('Local', 'Super Store', 'Mall Kiosk', 'Outlet') THEN 'Offline'
        WHEN store_type = 'Web Portal' THEN 'Web'
        ELSE NULL
	END;

-- Compare offline vs online
SELECT COUNT(product_quantity) AS number_of_sales,
SUM(product_quantity) AS product_quantity_count,
location
FROM dim_store_details
INNER JOIN orders_table ON dim_store_details.store_code = orders_table.store_code
GROUP BY location;

/* 5. What percentage of sales come through each type of store? */

SELECT store_type,
SUM(dim_products.product_price_sterling * orders_table.product_quantity) AS total_sales, -- orders_table.store_code
((SUM(dim_products.product_price_sterling * orders_table.product_quantity)) /
      SUM(SUM(dim_products.product_price_sterling * orders_table.product_quantity)) OVER ()) * 100 AS percentage_total
FROM dim_store_details
INNER JOIN orders_table ON orders_table.store_code = dim_store_details.store_code
INNER JOIN dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY store_type
ORDER BY total_sales DESC;

/* 6. Which months in which years have had the most sales historically?
The company stakeholders want assurances that the company has been doing well recently.*/

SELECT 
SUM(dim_products.product_price_sterling * orders_table.product_quantity) AS total_sales, -- orders_table.store_code
year,
month
FROM dim_date_times
INNER JOIN orders_table ON orders_table.date_uuid = dim_date_times.date_uuid
INNER JOIN dim_products ON dim_products.product_code = orders_table.product_code
GROUP BY month, year
ORDER BY total_sales DESC; -- March 1994 was the golden year

/* 7. What is the staff headcount?
The operations team would like to know the overall staff numbers in each location around the world. 
Perform a query to determine the staff numbers in each of the countries the company sells in.*/

SELECT SUM(staff_numbers) AS total_staff_numbers,
country_code
FROM dim_store_details
GROUP BY country_code
ORDER BY total_staff_numbers DESC; -- GB: 13307, DE: 6123, US: 1384

/* 8. Which German store is selling the most?
The sales team is looking to expand their territory in Germany. 
Determine which type of store is generating the most sales in Germany.*/

SELECT SUM(dim_products.product_price_sterling * orders_table.product_quantity) AS total_sales,
store_type,
dim_store_details.country_code
FROM dim_store_details
INNER JOIN orders_table ON dim_store_details.store_code = orders_table.store_code
INNER JOIN dim_products ON dim_products.product_code = orders_table.product_code
WHERE country_code LIKE 'DE'
GROUP BY dim_store_details.store_type, dim_store_details.country_code
ORDER BY total_sales DESC;

-- Ans: Local stores make the most at £1109909.59

/* 9. How quickly is the company making sales?
Determine the average time taken between each sale grouped by year. */







