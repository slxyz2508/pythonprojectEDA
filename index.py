import pandas as pd
import asyncio
import matplotlib.pyplot as plt
import seaborn as sns

# READ DATA .csv USING PANDAS
data = pd.read_csv("./churn-bigml-20_new.csv")

# ANALYSIS
def analysis_call(data, export_name='call_summary.csv'):
    target_cols = ['Total day calls', 'Total eve calls', 'Total night calls']
    df_clean = data.dropna(subset=['Churn'] + target_cols)[['Churn'] + target_cols]
    
    result_summary = df_clean.groupby('Churn')[target_cols].mean()
    return result_summary

def analysis_charge(data, export_name='call_summary.csv'):
    target_cols = ['Total day charge', 'Total eve charge', 'Total night charge']
    df_clean = data.dropna(subset=['Churn'] + target_cols)[['Churn'] + target_cols]
    
    result_summary = df_clean.groupby('Churn')[target_cols].mean()
    return result_summary

def analysis_minute(data, export_name='call_summary.csv'):
    target_cols = ['Total day minutes', 'Total eve minutes', 'Total night minutes']
    df_clean = data.dropna(subset=['Churn'] + target_cols)[['Churn'] + target_cols]
    
    result_summary = df_clean.groupby('Churn')[target_cols].mean()
    return result_summary

# GRAPH
def plot_stacked_metrics(df_summary, title, ylabel, filename):
    """
    Utility helper to plot stacked bar charts using Pandas and Seaborn themes.
    """
    # Set Seaborn design aesthetics
    sns.set_theme(style="whitegrid")
    colors = sns.color_palette("muted", n_colors=3)
    
    # Plot stacked bars
    ax = df_summary.plot(
        kind='bar',
        stacked=True,
        color=colors,
        figsize=(8, 6),
        width=0.45,
        edgecolor='none'
    )
    
    # Premium title and axis styling
    plt.title(title, fontsize=13, fontweight="bold", pad=15)
    plt.ylabel(ylabel, fontsize=11, labelpad=8)
    plt.xlabel("Customer Churn Status", fontsize=11, labelpad=8)
    
    # Format X ticks
    ax.set_xticklabels(["Active (False)", "Churned (True)"], rotation=0)
    
    # Custom beautiful legend (removes "Total" prefix and capitalizes words)
    legend_labels = [col.replace('Total ', '').title() for col in df_summary.columns]
    plt.legend(
        legend_labels,
        title="Metrics Segment",
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
        frameon=True,
        facecolor="white",
        edgecolor="none"
    )
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"[OK] Saved stacked chart to {filename}")

async def callmetrics() :
    behavior_mean = analysis_call(data)
    print("Churn vs Call Metrics")
    print(behavior_mean)
    # Generate and save call metrics stacked chart
    plot_stacked_metrics(
        df_summary=behavior_mean,
        title="Average Number of Calls by Churn Status\n(Stacked by Time Period)",
        ylabel="Average Calls",
        filename="churn_call_metrics_stacked.png"
    )
    
async def chargemetrics() :
    charge_mean = analysis_charge(data)
    print("Churn vs Charge Metrics")
    print(charge_mean)
    # Generate and save charge metrics stacked chart
    plot_stacked_metrics(
        df_summary=charge_mean,
        title="Average Charges by Churn Status\n(Stacked by Time Period)",
        ylabel="Average Charge ($)",
        filename="churn_charge_metrics_stacked.png"
    )
    
async def minutemetrics() :
    minute_mean = analysis_minute(data)
    print("Churn vs Minute Metrics")
    print(minute_mean)
    # Generate and save minute metrics stacked chart
    plot_stacked_metrics(
        df_summary=minute_mean,
        title="Average Minutes by Churn Status\n(Stacked by Time Period)",
        ylabel="Average Minutes",
        filename="churn_minute_metrics_stacked.png"
    )

async def combine_all_metrics():
    # 1. Fetch all data summaries
    behavior_mean = analysis_call(data)
    charge_mean = analysis_charge(data)
    minute_mean = analysis_minute(data)
    
    print("\n[OK] Generating combined metrics 3-panel stacked chart...")
    
    # 2. Set Seaborn aesthetics
    sns.set_theme(style="whitegrid")
    colors = sns.color_palette("muted", n_colors=3)
    
    # 3. Create a 1x3 subplots figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.5), dpi=150)
    
    plots_config = [
        (behavior_mean, "Average Call Volume", "Average Calls", axes[0]),
        (charge_mean, "Average Monetary Charges", "Average Charge ($)", axes[1]),
        (minute_mean, "Average Usage Minutes", "Average Minutes", axes[2])
    ]
    
    for df, title, ylabel, ax in plots_config:
        # Plot stacked bars onto the subplot axis
        df.plot(
            kind='bar',
            stacked=True,
            color=colors,
            width=0.45,
            edgecolor='none',
            ax=ax
        )
        
        # Subplot Titles and Axes
        ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
        ax.set_ylabel(ylabel, fontsize=10, labelpad=5)
        ax.set_xlabel("Customer Churn Status", fontsize=10, labelpad=5)
        ax.set_xticklabels(["Active (False)", "Churned (True)"], rotation=0)
        
        # Custom beautiful legend for each subplot
        legend_labels = [col.replace('Total ', '').title() for col in df.columns]
        ax.legend(
            legend_labels,
            title="Time Period",
            loc="upper left",
            frameon=True,
            facecolor="white",
            edgecolor="none",
            fontsize=9,
            title_fontsize=9
        )
        
    # Overall super-title for the entire infographic
    plt.suptitle("Customer Churn vs. Telecom Usage Metrics Comparison", fontsize=16, fontweight="bold", y=0.98)
    
    # Optimize layout and save
    plt.tight_layout()
    filename = "churn_combined_metrics_stacked.png"
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"[OK] Saved combined multi-panel stacked chart to {filename}")

# MAIN
async def main():
    # Run all metrics printing, individual chart saves, and the combined chart concurrently
    await asyncio.gather(
        callmetrics(),
        chargemetrics(),
        minutemetrics(),
        combine_all_metrics()
    )
if __name__ == "__main__":
    asyncio.run(main())