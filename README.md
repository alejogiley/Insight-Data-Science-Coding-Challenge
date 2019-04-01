# Insight Data Engineering Coding Challenge

## Summary

This GitHub repository contains my solution to the coding challenge for the Fellows Program organized by Insight Data Science. The challenge requieres, using the Instacart dataset, to calculate, for each department, the number of times a product was requested, number of times a product was requested for the first time and a ratio of those two numbers. 

## Libraries Required

This script requieres:

```
sys
time
```

## Usage

```python
python3 instacart_sales_analytics.py order_products.csv products.csv report.csv
```

## Approach

This program processes the `order_products.csv` and `products.csv` files one line at a time, to avoid the memory required to read an entire file. It uses a **Product_Record** object to keep track of `product_id` information and the number of total and first orders for each product, from `order_products.csv`. A second class, **Department_Record** tracks the `deparment_id` and `product_id` data from file `products.csv`, and keeps a list of all products belonging to a department. The script uses dictionaries to track these objects. Dictionaries enable rapid lookup of the records, even in cases of big datasets. Finally, for each deparment the total number of orders and first orders are calculated, as well as the ratio between these variables. Results are saved in an output file in adherence to the rules of this challenge.
