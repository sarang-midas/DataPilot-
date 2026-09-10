# Upload templates

For best results, start with stable headers and one row per record. Recommended semantic fields include:

- Dates: `date`, `order_date`, `created_at`
- Revenue: `sales`, `revenue`, `amount`
- Profit: `profit`, `net_income`
- Dimensions: `product`, `category`, `region`, `department`, `channel`
- IDs: `customer_id`, `order_id`, `employee_id`

The platform can still work with unrelated column names, but semantic names make automatic KPI detection stronger.
