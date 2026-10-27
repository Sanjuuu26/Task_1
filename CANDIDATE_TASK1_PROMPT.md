# Task 1: Marketplace Delivery Performance Analysis

You are given a small dataset from an e-commerce marketplace.

The operations team wants to know:

> For orders delivered in **May 2026**, what is the **on-time delivery rate by courier**?

---

# File Provided

- `task1_marketplace_delivery_sla_raw.csv`

---

# Dataset Column Definitions

| Column Name | Description |
|---|---|
| `order_id` | Unique identifier for an order |
| `order_date` | Date when the order was placed |
| `shipped_at` | Date when the order was shipped |
| `delivered_at` | Date when the order was delivered |
| `updated_at` | Timestamp of the most recent update made to the order record
| `courier` | Courier partner name |
| `city` | Delivery city |
| `payment_status` | Payment status of the order |
| `order_status` | Current status of the order |
| `promised_days` | Promised delivery time in days |
| `is_test_order` | Indicates whether the order is a test/internal order so it is not included in actual delivery calculations |

---

# Metric Definition

Calculate the number of days taken to deliver each order:

```python
actual_transit_days = delivered_at - shipped_at
```

An order is considered **On Time** if:

```python
actual_transit_days <= promised_days
```

Otherwise:

```python
delivery_status = "Late"
```

---

# Expected Output

Provide results in dataframe format.

Create a courier-level summary dataframe showing delivery performance metrics.

The output dataframe should contain:

| Column | Description |
|---|---|
| `courier` | Courier partner name |
| `eligible_orders` | Total number of orders eligible for delivery performance calculation |
| `on_time_orders` | Number of eligible orders delivered on or before the promised delivery time |
| `on_time_rate` | Percentage or ratio of on-time orders out of total eligible orders |

Example:

| courier | eligible_orders | on_time_orders | on_time_rate |
|---|---|---|---|
| ShipQuick | 10 | 8 | 0.80 |

---

# Visualization Requirement

Create at least 2 charts to extract insights from the given data.

Use Python libraries to complete this entire task.