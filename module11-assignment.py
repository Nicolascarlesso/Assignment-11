# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Group by quarter and sum all sales
    quarterly_totals = sales_df.groupby('QuarterLabel')['Sales'].sum()
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(quarter_labels, quarterly_totals.values, marker='o', linewidth=2, markersize=8)
    
    # Add labels and title
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel('Total Sales ($)', fontsize=12)
    ax.set_title('SunCoast Retail - Quarterly Sales Trend', fontsize=14, fontweight='bold')
    
    # Add gridlines for better readability
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45)
    
    # Format y-axis to show values in millions
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    
    plt.tight_layout()
    return fig

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Group by quarter and location
    location_quarterly = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Define colors and markers for each location
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    markers = ['o', 's', '^', 'D']
    
    # Plot each location
    for i, location in enumerate(locations):
        ax.plot(quarter_labels, location_quarterly[location].values, 
                marker=markers[i], label=location, linewidth=2, 
                markersize=8, color=colors[i])
    
    # Add labels and title
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel('Total Sales ($)', fontsize=12)
    ax.set_title('Sales Trends Comparison by Location', fontsize=14, fontweight='bold')
    
    # Add legend
    ax.legend(loc='best', fontsize=10)
    
    # Add gridlines
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    
    plt.tight_layout()
    return fig


# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Filter for most recent quarter (Q4 2023)
    recent_quarter = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    
    # Group by location and category
    category_by_location = recent_quarter.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Set bar width and positions
    bar_width = 0.15
    x = np.arange(len(locations))
    
    # Plot bars for each category
    for i, category in enumerate(categories):
        offset = bar_width * (i - 2)
        ax.bar(x + offset, category_by_location[category].values, 
               bar_width, label=category)
    
    # Add labels and title
    ax.set_xlabel('Location', fontsize=12)
    ax.set_ylabel('Sales ($)', fontsize=12)
    ax.set_title('Product Category Performance by Location (Q4 2023)', 
                 fontsize=14, fontweight='bold')
    
    # Set x-axis labels
    ax.set_xticks(x)
    ax.set_xticklabels(locations)
    
    # Add legend
    ax.legend(loc='best', fontsize=9)
    
    # Add gridlines
    ax.grid(True, alpha=0.3, axis='y')
    
    # Format y-axis
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
    
    plt.tight_layout()
    return fig

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Group by location and category, sum all sales
    composition = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    
    # Calculate percentages
    composition_pct = composition.div(composition.sum(axis=1), axis=0) * 100
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create stacked bar chart
    composition_pct.plot(kind='bar', stacked=True, ax=ax, 
                         colormap='Set3', width=0.7)
    
    # Add labels and title
    ax.set_xlabel('Location', fontsize=12)
    ax.set_ylabel('Percentage of Total Sales (%)', fontsize=12)
    ax.set_title('Sales Composition by Product Category', 
                 fontsize=14, fontweight='bold')
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Add legend
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add gridlines
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create scatter plot
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.5, s=50)
    
    # Calculate and plot best-fit line
    z = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax.plot(x_line, p(x_line), "r--", linewidth=2, label='Best Fit Line')
    
    # Add labels and title
    ax.set_xlabel('Advertising Spend ($)', fontsize=12)
    ax.set_ylabel('Sales ($)', fontsize=12)
    ax.set_title('Relationship Between Advertising Spend and Sales', 
                 fontsize=14, fontweight='bold')
    
    # Add legend
    ax.legend()
    
    # Add gridlines
    ax.grid(True, alpha=0.3)
    
    # Format axes
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
    
    plt.tight_layout()
    return fig

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Group by quarter and calculate average efficiency
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot line chart
    ax.plot(quarter_labels, efficiency.values, marker='o', 
            linewidth=2, markersize=8, color='green')
    
    # Add labels and title
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_ylabel('Sales per Dollar Spent ($)', fontsize=12)
    ax.set_title('Advertising Efficiency Over Time', 
                 fontsize=14, fontweight='bold')
    
    # Add gridlines
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45)
    
    # Add annotation for trend
    if efficiency.values[-1] > efficiency.values[0]:
        trend_text = 'Improving Efficiency'
    else:
        trend_text = 'Declining Efficiency'
    ax.annotate(trend_text, xy=(6, efficiency.values[-2]), 
                fontsize=10, color='green', fontweight='bold')
    
    plt.tight_layout()
    return fig


# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Create figure with subplots (2 rows, 3 columns)
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle('Customer Age Distribution Analysis', fontsize=16, fontweight='bold')
    
    # Overall distribution in first subplot
    ax = axes[0, 0]
    ax.hist(customer_df['Age'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
    mean_age = customer_df['Age'].mean()
    median_age = customer_df['Age'].median()
    ax.axvline(mean_age, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_age:.1f}')
    ax.axvline(median_age, color='green', linestyle='--', linewidth=2, label=f'Median: {median_age:.1f}')
    ax.set_xlabel('Age', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.set_title('Overall', fontsize=12, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    
    # Distribution by location in remaining subplots
    for i, location in enumerate(locations):
        row = (i + 1) // 3
        col = (i + 1) % 3
        ax = axes[row, col]
        
        location_data = customer_df[customer_df['Location'] == location]['Age']
        ax.hist(location_data, bins=15, color='coral', edgecolor='black', alpha=0.7)
        
        mean_age = location_data.mean()
        median_age = location_data.median()
        ax.axvline(mean_age, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_age:.1f}')
        ax.axvline(median_age, color='green', linestyle='--', linewidth=2, label=f'Median: {median_age:.1f}')
        
        ax.set_xlabel('Age', fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        ax.set_title(location, fontsize=12, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    # Hide the last empty subplot
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    return fig

# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Create age groups
    bins = [18, 30, 45, 60, 80]
    labels = ['18-30', '31-45', '46-60', '61+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels, include_lowest=True)
    
    # Prepare data for box plot
    age_group_data = [customer_df[customer_df['AgeGroup'] == group]['PurchaseAmount'].values 
                      for group in labels]
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create box plot
    bp = ax.boxplot(age_group_data, labels=labels, patch_artist=True)
    
    # Color the boxes
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    # Add labels and title
    ax.set_xlabel('Age Group', fontsize=12)
    ax.set_ylabel('Purchase Amount ($)', fontsize=12)
    ax.set_title('Purchase Amounts by Age Group', fontsize=14, fontweight='bold')
    
    # Add gridlines
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig


# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create histogram with appropriate bins
    ax.hist(customer_df['PurchaseAmount'], bins=30, color='steelblue', 
            edgecolor='black', alpha=0.7)
    
    # Add labels and title
    ax.set_xlabel('Purchase Amount ($)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Purchase Amounts', fontsize=14, fontweight='bold')
    
    # Add gridlines
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Calculate total sales by price tier
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define colors for tiers
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    
    # Find the largest slice to explode
    explode = [0.1 if i == tier_sales.argmax() else 0 for i in range(len(tier_sales))]
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(tier_sales.values, labels=tier_sales.index, 
                                        autopct='%1.1f%%', startangle=90, 
                                        colors=colors, explode=explode)
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    # Add title
    ax.set_title('Sales Breakdown by Price Tier', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig


# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Calculate total sales by category
    category_sales = sales_df.groupby('Category')['Sales'].sum()
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define colors
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    
    # Find the largest slice to explode
    explode = [0.1 if i == category_sales.argmax() else 0 for i in range(len(category_sales))]
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(category_sales.values, labels=category_sales.index, 
                                        autopct='%1.1f%%', startangle=90, 
                                        colors=colors, explode=explode)
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # Add title
    ax.set_title('Market Share by Product Category', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Calculate total sales by location
    location_sales = sales_df.groupby('Location')['Sales'].sum()
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define colors
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(location_sales.values, labels=location_sales.index, 
                                        autopct='%1.1f%%', startangle=90, 
                                        colors=colors)
    
    # Make percentage text bold
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    # Add title
    ax.set_title('Sales Distribution by Store Location', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig


# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    # Create figure with 2x2 grid of subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('SunCoast Retail - Executive Business Dashboard', 
                 fontsize=18, fontweight='bold', y=0.995)
    
    # Subplot 1: Quarterly Sales Trend (top-left)
    ax1 = axes[0, 0]
    quarterly_totals = sales_df.groupby('QuarterLabel')['Sales'].sum()
    ax1.plot(quarter_labels, quarterly_totals.values, marker='o', 
             linewidth=2, markersize=8, color='#1f77b4')
    ax1.set_xlabel('Quarter', fontsize=10)
    ax1.set_ylabel('Total Sales ($)', fontsize=10)
    ax1.set_title('Quarterly Sales Trend', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    
    # Subplot 2: Category Market Share (top-right)
    ax2 = axes[0, 1]
    category_sales = sales_df.groupby('Category')['Sales'].sum()
    colors_cat = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    wedges, texts, autotexts = ax2.pie(category_sales.values, labels=category_sales.index, 
                                         autopct='%1.1f%%', startangle=90, colors=colors_cat)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    ax2.set_title('Market Share by Category', fontsize=12, fontweight='bold')
    
    # Subplot 3: Sales by Location (bottom-left)
    ax3 = axes[1, 0]
    location_totals = sales_df.groupby('Location')['Sales'].sum()
    colors_loc = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars = ax3.bar(locations, location_totals.values, color=colors_loc, alpha=0.7)
    ax3.set_xlabel('Location', fontsize=10)
    ax3.set_ylabel('Total Sales ($)', fontsize=10)
    ax3.set_title('Total Sales by Location', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
    ax3.tick_params(axis='x', rotation=45)
    
    # Subplot 4: Ad Spend vs Sales (bottom-right)
    ax4 = axes[1, 1]
    ax4.scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.5, s=30, color='purple')
    z = np.polyfit(sales_df['AdSpend'], sales_df['Sales'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(sales_df['AdSpend'].min(), sales_df['AdSpend'].max(), 100)
    ax4.plot(x_line, p(x_line), "r--", linewidth=2, label='Trend')
    ax4.set_xlabel('Advertising Spend ($)', fontsize=10)
    ax4.set_ylabel('Sales ($)', fontsize=10)
    ax4.set_title('Ad Spend vs Sales Relationship', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e3:.0f}K'))
    
    plt.tight_layout()
    return fig


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    print("\nGenerating Time Series Visualizations...")
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    print("Generating Categorical Comparison Visualizations...")
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    print("Generating Relationship Analysis Visualizations...")
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    print("Generating Distribution Analysis Visualizations...")
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    print("Generating Sales Distribution Visualizations...")
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    print("Generating Market Share Analysis Visualizations...")
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    print("Generating Comprehensive Dashboard...")
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\n" + "=" * 60)
    print("KEY BUSINESS INSIGHTS:")
    print("=" * 60)
    
    # Calculate key metrics for insights
    total_sales = sales_df['Sales'].sum()
    sales_growth = ((sales_df[sales_df['QuarterLabel'] == 'Q4 2023']['Sales'].sum() - 
                     sales_df[sales_df['QuarterLabel'] == 'Q1 2022']['Sales'].sum()) / 
                    sales_df[sales_df['QuarterLabel'] == 'Q1 2022']['Sales'].sum() * 100)
    
    top_location = sales_df.groupby('Location')['Sales'].sum().idxmax()
    top_category = sales_df.groupby('Category')['Sales'].sum().idxmax()
    
    print(f"\n1. SALES PERFORMANCE:")
    print(f"   - Total sales across all periods: ${total_sales/1e6:.2f}M")
    print(f"   - Sales growth from Q1 2022 to Q4 2023: {sales_growth:.1f}%")
    print(f"   - Strong seasonal pattern with Q4 showing holiday boost")
    
    print(f"\n2. LOCATION INSIGHTS:")
    print(f"   - {top_location} is the top-performing location")
    print(f"   - Miami shows consistently higher sales due to larger market")
    print(f"   - All locations show positive growth trends")
    
    print(f"\n3. PRODUCT CATEGORY PERFORMANCE:")
    print(f"   - {top_category} is the leading category by sales volume")
    print(f"   - Electronics dominates sales across all locations")
    print(f"   - Category preferences vary by location demographics")
    
    print(f"\n4. CUSTOMER DEMOGRAPHICS:")
    print(f"   - Miami has younger customer base (mean age ~35)")
    print(f"   - Tampa has older demographic (mean age ~45)")
    print(f"   - Age groups show different purchasing patterns")
    
    print(f"\n5. ADVERTISING EFFECTIVENESS:")
    print(f"   - Positive correlation between ad spend and sales")
    print(f"   - Advertising efficiency has remained relatively stable")
    print(f"   - Opportunity to optimize ad spending across locations")
    
    print(f"\n6. PRICING TIER DISTRIBUTION:")
    print(f"   - Mid-range products account for largest share of sales")
    print(f"   - Premium tier represents growth opportunity")
    print(f"   - Budget tier maintains steady customer base")
    
    print("\n" + "=" * 60)
    print("BUSINESS RECOMMENDATIONS:")
    print("=" * 60)
    print("\n1. Focus marketing efforts in Miami to capitalize on high performance")
    print("2. Increase Electronics inventory during Q4 for holiday season")
    print("3. Develop targeted campaigns based on location demographics")
    print("4. Optimize advertising budget allocation across locations")
    print("5. Expand premium product offerings to increase average transaction value")
    print("6. Implement loyalty programs tailored to different age groups")
    
    print("\n" + "=" * 60)
    print("Visualizations generated successfully!")
    print("=" * 60)
    
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()