import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_aqi_charts():
    db_path = os.path.join('data', 'aqi_data.db')
    output_dir = os.path.join('outputs', 'charts')
    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM india_aqi", conn)
    conn.close()

    df['Date'] = pd.to_datetime(df['Date'])
    df['MonthNum'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.strftime('%B')

    df_city_avg = df.groupby('City').mean(numeric_only=True).reset_index()
    df_monthly_avg = df.groupby(['MonthNum', 'Month']).mean(numeric_only=True).reset_index().sort_values('MonthNum')

    # Apply global Times New Roman rules
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']

    title_font = {'fontsize': 14, 'fontweight': 'bold', 'pad': 15}
    label_font = {'fontsize': 11, 'labelpad': 10}

    # 1. BAR CHART (Horizontal Mean AQI Profile)
    print("Exporting Chart 1: Bar Chart...")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df_city_avg, x='AQI', y='City', hue='City', legend=False, palette='Reds_r', ax=ax)
    ax.set_title('Average Air Quality Index (AQI) across Cities', **title_font)
    ax.set_xlabel('AQI Value', **label_font)
    plt.savefig(os.path.join(output_dir, '1_bar_aqi.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 2. COLUMN CHART (Vertical PM2.5 Profile)
    print("Exporting Chart 2: Column Chart...")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df_city_avg, x='City', y='PM2.5', hue='City', legend=False, palette='copper', ax=ax)
    ax.set_title('Average Fine Particulate Matter Concentration (PM2.5)', **title_font)
    ax.set_ylabel('Concentration (µg/m³)', **label_font)
    plt.savefig(os.path.join(output_dir, '2_column_pm25.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 3. SCATTER CHART (PM2.5 vs PM10 Distribution Correlation)
    print("Exporting Chart 3: Scatter Chart...")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.scatterplot(data=df, x='PM2.5', y='PM10', hue='City', alpha=0.6, palette='Dark2', ax=ax)
    ax.set_title('Correlation Analysis: PM2.5 vs. PM10 Particulate Load', **title_font)
    ax.set_xlabel('PM2.5 (µg/m³)', **label_font)
    ax.set_ylabel('PM10 (µg/m³)', **label_font)
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    plt.savefig(os.path.join(output_dir, '3_scatter_pollutants.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 4. LINE CHART (Seasonal Timeline AQI Trend Tracking)
    print("Exporting Chart 4: Line Chart...")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_monthly_avg['Month'], df_monthly_avg['AQI'], marker='s', color='#C0392B', linewidth=2.5)
    ax.set_title('Annual Macro AQI Trajectory (India Trendline)', **title_font)
    ax.set_ylabel('Mean AQI Value', **label_font)
    ax.tick_params(axis='x', rotation=35)
    plt.savefig(os.path.join(output_dir, '4_line_aqi_trend.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # 5. HEATMAP (Pollutant Cross-Correlation Matrix)
    print("Exporting Chart 5: Heatmap Matrix...")
    fig, ax = plt.subplots(figsize=(7, 5.5))
    corr = df[['PM2.5', 'PM10', 'NO2', 'SO2', 'AQI']].corr()
    sns.heatmap(corr, annot=True, cmap='YlOrRd', fmt=".2f", linewidths=1.5, ax=ax, annot_kws={'family':'serif'})
    ax.set_title('Pollutant Interactions & AQI Correlation Weights', **title_font)
    plt.savefig(os.path.join(output_dir, '5_heatmap_aqi_corr.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print("All 5 clean Times New Roman charts exported to outputs/charts/.")

if __name__ == "__main__":
    generate_aqi_charts()
