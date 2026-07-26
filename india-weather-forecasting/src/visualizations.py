import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_all_charts():
    # 1. Setup file directories
    db_path = os.path.join('data', 'weather_data.db')
    output_dir = os.path.join('outputs', 'charts')
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(db_path):
        print(f"Error: Database not found at '{db_path}'. Run db_setup.py first.")
        return

    # 2. Extract operational data from the database
    print("Extracting weather trends from SQLite database...")
    conn = sqlite3.connect(db_path)
    query = "SELECT Date, City, Temperature, Humidity, Rainfall, WindSpeed FROM india_weather"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Process dates safely
    df['Date'] = pd.to_datetime(df['Date'])
    df['MonthNum'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.strftime('%B')

    # Create specialized aggregated datasets for visual clarity
    df_city_avg = df.groupby('City').mean(numeric_only=True).reset_index()
    df_monthly_avg = df.groupby(['MonthNum', 'Month']).mean(numeric_only=True).reset_index().sort_values('MonthNum')

    # 3. Configure global professional typography (Times New Roman) and layout padding
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    plt.rcParams['axes.edgecolor'] = '#CCCCCC'
    plt.rcParams['axes.linewidth'] = 0.8

    sns.set_theme(style="whitegrid")
    # Re-apply font setting after seaborn theme overrides it
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']

    # Font sizing dictionaries to prevent text collisions
    title_font = {'fontsize': 14, 'fontweight': 'bold', 'pad': 15}
    label_font = {'fontsize': 11, 'labelpad': 10}

    # ---------------------------------------------------------
    # CHART 1: Horizontal Bar Chart (Average Humidity by City)
    # ---------------------------------------------------------
    print("Generating Chart 1: Bar Chart...")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df_city_avg, x='Humidity', y='City', hue='City', legend=False, palette='Blues_r', ax=ax)
    ax.set_title('Average Relative Humidity (%) across Indian Cities', **title_font)
    ax.set_xlabel('Humidity (%)', **label_font)
    ax.set_ylabel('City', **label_font)
    ax.tick_params(axis='both', labelsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '1_bar_humidity.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # CHART 2: Vertical Column Chart (Average Rainfall by City)
    # ---------------------------------------------------------
    print("Generating Chart 2: Column Chart...")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=df_city_avg, x='City', y='Rainfall', hue='City', legend=False, palette='YlGnBu_r', ax=ax)
    ax.set_title('Average Daily Monsoon Rainfall Distribution (mm)', **title_font)
    ax.set_xlabel('City', **label_font)
    ax.set_ylabel('Rainfall (mm)', **label_font)
    ax.tick_params(axis='both', labelsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '2_column_rainfall.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # CHART 3: Scatter Chart (Temperature vs Humidity)
    # ---------------------------------------------------------
    print("Generating Chart 3: Scatter Chart...")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.scatterplot(data=df, x='Temperature', y='Humidity', hue='City', alpha=0.5, palette='Set2', ax=ax)
    ax.set_title('Correlation Profile: Temperature vs. Humidity', **title_font)
    ax.set_xlabel('Temperature (°C)', **label_font)
    ax.set_ylabel('Humidity (%)', **label_font)
    ax.tick_params(axis='both', labelsize=10)

    # Legend pushed safely outside the plotting canvas to stop it overlapping the dots
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '3_scatter_temp_hum.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # CHART 4: Line Chart (Seasonal National Temperature Trend)
    # ---------------------------------------------------------
    print("Generating Chart 4: Line Chart...")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_monthly_avg['Month'], df_monthly_avg['Temperature'], marker='o', color='#E67E22', linewidth=2.5,
            markersize=7)
    ax.set_title('Annual Micro-Climate Temperature Trajectory (India)', **title_font)
    ax.set_xlabel('Month', **label_font)
    ax.set_ylabel('Mean Temperature (°C)', **label_font)

    # Angle the months so long names like "September" do not crash into each other
    ax.tick_params(axis='x', rotation=35, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '4_line_temp_trend.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # CHART 5: Heatmap Matrix (Weather Variables Correlation)
    # ---------------------------------------------------------
    print("Generating Chart 5: Heatmap Matrix...")
    fig, ax = plt.subplots(figsize=(7, 5.5))
    corr_matrix = df[['Temperature', 'Humidity', 'Rainfall', 'WindSpeed']].corr()

    # Heatmap setup with padding, clean values, and explicit boundaries
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=1.5,
                cbar=True, ax=ax, annot_kws={'size': 11, 'family': 'serif'})
    ax.set_title('Atmospheric Variable Inter-dependencies', **title_font)
    ax.tick_params(axis='both', labelsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_heatmap_corr.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print("\nProcessing complete! All high-resolution charts saved cleanly in 'outputs/charts/'.")


if __name__ == "__main__":
    generate_all_charts()
