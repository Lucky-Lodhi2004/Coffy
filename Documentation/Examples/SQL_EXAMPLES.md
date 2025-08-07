# Advanced SQL Examples for Coffy

These examples demonstrate advanced SQL workflows using the `coffy.sql` module with SQLite. They go beyond basic queries by including joins, filtering, grouping, and exporting results  all without using any ORM.

---

## Example 1: Filter High Salary Employees and Export to CSV

This example filters employees based on a salary threshold, selects only required fields, and exports the result to CSV.

```python
from coffy.sql import init, query

init("company.sqlite")

query("CREATE TABLE employees (id INTEGER, name TEXT, role TEXT, salary INTEGER)")
query("INSERT INTO employees VALUES (1, 'Neel', 'Manager', 80000)")
query("INSERT INTO employees VALUES (2, 'Zara', 'Developer', 50000)")
query("INSERT INTO employees VALUES (3, 'Ravi', 'Intern', 20000)")

# Filter and project specific columns
result = query("SELECT name, role FROM employees WHERE salary > 40000")

print(result)
result.to_csv("high_salary_employees.csv")
```

### Output:

```sql
name  | role    
------+----------
Neel  | Manager  
Zara  | Developer
```



## Example 2: Group Sales by Region and Calculate Totals

This example demonstrates how to aggregate sales data by region using SQL's `GROUP BY` and `SUM()` functions. It outputs total sales per region and saves the result to a CSV file.

---

### Code

```python
from coffy.sql import init, query

# Initialize the SQLite database
init("sales.sqlite")

# Create and populate the sales table
query("CREATE TABLE sales (region TEXT, amount INTEGER)")
query("INSERT INTO sales VALUES ('South', 500), ('North', 1000), ('South', 300), ('North', 700)")

# Group by region and calculate total sales
result = query(\"\"\"
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
\"\"\")

# Print results in the terminal
print(result)

# Export result to a CSV file
result.to_csv("region_sales_summary.csv")
```
### Output:
```sql
region | total_sales
-------+------------
North  | 1700       
South  | 800
```


