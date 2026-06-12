"""
Superstore Analysis
Angles covered:
 1. The Bleeding Profit Deep-Dive (Discount vs Profit)
 2. Product-Level Profitability vs Shelf-Space Logic (Sub-Category / Product)
 3. Shipping Mode Economics (where to focus discount discipline)
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams.update({
    'figure.dpi': 120,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'font.size': 10
})

# ---------------------------------------------------------------
# Load data
# ---------------------------------------------------------------
df = pd.read_csv('data\Sample - Superstore.csv', encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print(f"Rows: {len(df):,} | Date range: {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
print(f"Overall Sales: ${df['Sales'].sum():,.0f} | Overall Profit: ${df['Profit'].sum():,.0f} "
      f"| Overall Margin: {df['Profit'].sum()/df['Sales'].sum()*100:.1f}%")

# =================================================================
# ANGLE 1: THE BLEEDING PROFIT DEEP-DIVE
# =================================================================
print("\n" + "="*70)
print("ANGLE 1: THE BLEEDING PROFIT DEEP-DIVE")
print("="*70)

df['Discount_Band'] = pd.cut(
    df['Discount'],
    bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.5, 1],
    labels=['0%', '0-10%', '10-20%', '20-30%', '30-50%', '50%+']
)

band_summary = df.groupby('Discount_Band').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Order ID', 'count')
)
band_summary['Margin %'] = (band_summary['Profit'] / band_summary['Sales'] * 100).round(1)
print("\nProfit margin by discount band:")
print(band_summary.round(1))

# Chart 1a: Margin by discount band (the "cliff")
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#2a9d8f' if m >= 0 else '#e63946' for m in band_summary['Margin %']]
bars = ax.bar(band_summary.index.astype(str), band_summary['Margin %'], color=colors)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('The Discount Cliff: Profit Margin Collapses Beyond 20% Discount', fontsize=12, fontweight='bold')
ax.set_xlabel('Discount Band')
ax.set_ylabel('Profit Margin (%)')
for bar, val in zip(bars, band_summary['Margin %']):
    ax.text(bar.get_x() + bar.get_width()/2, val + (3 if val >= 0 else -6),
            f"{val:.1f}%", ha='center', fontweight='bold', fontsize=9)
plt.tight_layout()
plt.savefig('charts\chart1_discount_cliff.png', bbox_inches='tight')
plt.close()
print("\n[Saved chart1_discount_cliff.png]")

# Chart 1b: Profit by Category x Discount Band (heatmap-style)
cat_band = df.groupby(['Category', 'Discount_Band'])['Profit'].sum().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(9, 5))
cat_band.T.plot(kind='bar', ax=ax, color=['#e76f51', '#2a9d8f', '#264653'])
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('Profit by Category Across Discount Bands', fontsize=12, fontweight='bold')
ax.set_xlabel('Discount Band')
ax.set_ylabel('Total Profit ($)')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.legend(title='Category')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts\chart2_category_discount_profit.png', bbox_inches='tight')
plt.close()
print("[Saved chart2_category_discount_profit.png]")

# Region x Category loss at high discount
hd = df[df['Discount'] > 0.2]
print("\nProfit loss at >20% discount, by Region x Category:")
region_cat_loss = hd.groupby(['Region', 'Category'])['Profit'].sum().round(0)
print(region_cat_loss)
print(f"\nTotal profit destroyed by discounts >20%: ${hd['Profit'].sum():,.0f}")

# =================================================================
# ANGLE 2: PRODUCT-LEVEL PROFITABILITY
# =================================================================
print("\n" + "="*70)
print("ANGLE 2: PRODUCT-LEVEL PROFITABILITY")
print("="*70)

subcat = df.groupby('Sub-Category').agg(
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Qty=('Quantity', 'sum'),
    AvgDiscount=('Discount', 'mean')
)
subcat['Margin %'] = (subcat['Profit'] / subcat['Sales'] * 100).round(1)
subcat = subcat.sort_values('Profit')
print("\nSub-Category profitability (sorted, worst first):")
print(subcat.round(1))

loss_makers = subcat[subcat['Profit'] < 0]
print(f"\nLoss-making sub-categories: {list(loss_makers.index)}")
print(f"Combined loss from these sub-categories: ${loss_makers['Profit'].sum():,.0f}")

# Chart 3: Sub-category sales vs profit (diverging bar)
fig, ax = plt.subplots(figsize=(9, 7))
colors = ['#e63946' if p < 0 else '#2a9d8f' for p in subcat['Profit']]
ax.barh(subcat.index, subcat['Profit'], color=colors)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_title('Profit by Sub-Category: Where the Money Goes (and Doesn\'t)', fontsize=12, fontweight='bold')
ax.set_xlabel('Total Profit ($)')
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig('charts\chart3_subcategory_profit.png', bbox_inches='tight')
plt.close()
print("\n[Saved chart3_subcategory_profit.png]")

# Worst individual products
worst_products = df.groupby('Product Name').agg(
    Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Orders=('Order ID', 'count')
).sort_values('Profit').head(10)
print("\nTop 10 worst individual products by total profit:")
print(worst_products.round(1))

# Chart 4: Worst products
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(worst_products.index, worst_products['Profit'], color='#e63946')
ax.set_title('10 Worst Products by Total Profit Loss', fontsize=12, fontweight='bold')
ax.set_xlabel('Total Profit ($)')
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('charts\chart4_worst_products.png', bbox_inches='tight')
plt.close()
print("[Saved chart4_worst_products.png]")

# =================================================================
# ANGLE 3: SHIPPING MODE ECONOMICS
# =================================================================
print("\n" + "="*70)
print("ANGLE 3: SHIPPING MODE ECONOMICS")
print("="*70)

ship = df.groupby('Ship Mode').agg(
    Orders=('Order ID', 'count'),
    Sales=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    AvgDiscount=('Discount', 'mean')
)
ship['Margin %'] = (ship['Profit'] / ship['Sales'] * 100).round(1)
ship['Order Share %'] = (ship['Orders'] / ship['Orders'].sum() * 100).round(1)
ship['Sales Share %'] = (ship['Sales'] / ship['Sales'].sum() * 100).round(1)
print("\nShipping mode summary:")
print(ship.round(2))

loss_rate = (df['Profit'] < 0).groupby(df['Ship Mode']).mean() * 100
print("\nLoss-making order rate by ship mode:")
print(loss_rate.round(1))

# Chart 5: Ship mode - volume share vs margin (combo chart)
fig, ax1 = plt.subplots(figsize=(8, 5))
ax2 = ax1.twinx()
x = range(len(ship))
ax1.bar(x, ship['Order Share %'], color='#264653', alpha=0.6, label='Share of Orders (%)')
ax2.plot(x, ship['Margin %'], color='#e63946', marker='o', linewidth=2.5, label='Profit Margin (%)')
ax1.set_xticks(x)
ax1.set_xticklabels(ship.index)
ax1.set_ylabel('Share of Total Orders (%)')
ax2.set_ylabel('Profit Margin (%)', color='#e63946')
ax1.set_title('Standard Class Dominates Volume but Lags on Margin', fontsize=12, fontweight='bold')
fig.legend(loc='upper center', bbox_to_anchor=(0.5, -0.02), ncol=2)
plt.tight_layout()
plt.savefig('charts\chart5_shipmode_economics.png', bbox_inches='tight')
plt.close()
print("\n[Saved chart5_shipmode_economics.png]")

# =================================================================
# CROSS-CUT: Highest leverage intersection
# =================================================================
print("\n" + "="*70)
print("CROSS-CUT: WHERE TO FOCUS FIRST")
print("="*70)
focus = df[(df['Ship Mode'] == 'Standard Class') &
           (df['Category'].isin(['Furniture', 'Office Supplies'])) &
           (df['Discount'] > 0.2)]
print("\nStandard Class + Furniture/Office Supplies + Discount>20%:")
print(f"  Orders: {len(focus):,}")
print(f"  Sales: ${focus['Sales'].sum():,.0f}")
print(f"  Profit: ${focus['Profit'].sum():,.0f}")
print(f"  Margin: {focus['Profit'].sum()/focus['Sales'].sum()*100:.1f}%")
