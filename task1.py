import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\Users\Omkar\Downloads\task1\task1\task1_marketplace_delivery_sla_raw.csv"  
df = pd.read_csv(file_path)

df.columns = df.columns.str.strip().str.lower()  # Strip whitespace from column names

for col in ["order_date", "shipped_at", "delivered_at", "updated_at"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)


df["promised_days"] = pd.to_numeric(df["promised_days"], errors="coerce")


df["courier"] = df["courier"].astype(str).str.strip().str.lower()  # Normalize courier names to lowercase and strip whitespace      
courier_names = {
    "shipquick": "ShipQuick",
    "fastbee": "FastBee",
    "blue dart": "Blue Dart",
    "bluedart": "Blue Dart",
}
df["courier"] = df["courier"].map(courier_names).fillna(df["courier"].str.title())  # Map known courier names and title case others


test_flag = df["is_test_order"].astype(str).str.strip().str.lower()  # Normalize test order flags to lowercase and strip whitespace
df = df[~test_flag.isin(["yes", "true", "1", "y"])].copy()  # Filter out test orders


df = df[
    (df["delivered_at"] >= pd.Timestamp("2026-05-01"))
    & (df["delivered_at"] < pd.Timestamp("2026-06-01"))
].copy()  # Filter for deliveries in May 2026


df = df[
    df["shipped_at"].notna()
    & df["delivered_at"].notna()
    & df["promised_days"].notna()
    & df["courier"].notna()
    & (df["courier"] != "")
].copy()  # Filter out rows with missing values in critical columns


df["actual_transit_days"] = (
    df["delivered_at"].dt.normalize() - df["shipped_at"].dt.normalize()
).dt.days  # Calculate actual transit days

df = df[
    (df["actual_transit_days"] >= 0)
    & (df["promised_days"] >= 0)
].copy()  # Filter out rows with negative transit or promised days


df["delivery_status"] = df.apply(
    lambda row: "On Time"
    if row["actual_transit_days"] <= row["promised_days"]
    else "Late",
    axis=1,
)  # Determine delivery status based on promised days


summary = (
    df.groupby("courier")
    .agg(
        eligible_orders=("order_id", "nunique"),
        on_time_orders=(
            "delivery_status",
            lambda values: (
                df.loc[values.index, ["order_id", "delivery_status"]]
                .drop_duplicates(subset="order_id")["delivery_status"]
                .eq("On Time")
                .sum()
            ),
        ),
    )
    .reset_index()    
)


dedup = df.sort_values("updated_at").drop_duplicates(subset="order_id", keep="last")
summary = (
    dedup.groupby("courier")
    .agg(
        eligible_orders=("order_id", "nunique"),
        on_time_orders=("delivery_status", lambda s: s.eq("On Time").sum()),
    )
    .reset_index()
)
summary["on_time_rate"] = (
    summary["on_time_orders"] / summary["eligible_orders"]
).round(4)
summary = summary.sort_values("on_time_rate", ascending=False).reset_index(drop=True)

print("\nCourier-level summary — deliveries in May 2026")
print(summary.to_string(index=False))

summary.to_csv("courier_delivery_summary.csv", index=False)
dedup.to_csv("eligible_orders_may_2026.csv", index=False)


if not summary.empty:
    chart_data = summary.sort_values("on_time_rate", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(chart_data["courier"], chart_data["on_time_rate"] * 100)
    ax.set_title("On-Time Delivery Rate by Courier (May 2026)")
    ax.set_xlabel("On-time delivery rate (%)")
    ax.set_ylabel("Courier")
    ax.set_xlim(0, 100)
    ax.bar_label(bars, fmt="%.1f%%", padding=3)
    fig.tight_layout()
    fig.savefig("chart1_on_time_rate_by_courier.png", dpi=200)
    plt.show()


    counts = (
        dedup.assign(
            On_Time=dedup["delivery_status"].eq("On Time").astype(int),
            Late=dedup["delivery_status"].eq("Late").astype(int),
        )
        .groupby("courier")[["On_Time", "Late"]]
        .sum()
        .reindex(summary["courier"])
        .fillna(0)
    )


    ax = counts.plot(kind="bar", stacked=True, figsize=(9, 5))
    ax.set_title("On-Time vs Late Orders by Courier (May 2026)")
    ax.set_xlabel("Courier")
    ax.set_ylabel("Number of eligible orders")
    ax.legend(["On Time", "Late"], title="Delivery status")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig("chart2_on_time_vs_late.png", dpi=200)
    plt.show()
else:


  print(
        "No eligible orders found. Verify the CSV date format and check "
        "whether any orders were delivered in May 2026."
    )
  

print("\nSaved: courier_delivery_summary.csv")
print("Saved: eligible_orders_may_2026.csv")
print("Saved: chart1_on_time_rate_by_courier.png")
print("Saved: chart2_on_time_vs_late.png")

