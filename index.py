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
def plot_clustered_metrics(df_summary, title, ylabel, filename):
    """
    Utility helper to plot clustered bar charts using Pandas and Seaborn themes.
    """
    # Set Seaborn design aesthetics
    sns.set_theme(style="whitegrid")
    # Custom bar colors: Active (Light Blue-Gray), Churned (Dark Red)
    colors = ["#C5D0D6", "#D32F2F"]
    
    # Transpose the data: X-axis becomes Time Period, Colors become Churn Status
    df_transposed = df_summary.T
    
    # Plot clustered bars
    ax = df_transposed.plot(
        kind='bar',
        stacked=False,
        color=colors,
        figsize=(8, 6),
        width=0.6,
        edgecolor='none'
    )
    
    # Add data labels on top of the bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', padding=3, fontsize=9)
        
    # Premium title and axis styling
    plt.title(title, fontsize=13, fontweight="bold", pad=15)
    plt.ylabel(ylabel, fontsize=11, labelpad=8)
    plt.xlabel("Time Period", fontsize=11, labelpad=8)
    
    # Format X ticks dynamically based on index names (e.g. 'Total day calls' -> 'Day Calls')
    x_labels = [col.replace('Total ', '').title() for col in df_transposed.index]
    ax.set_xticklabels(x_labels, rotation=0)
    
    # Custom beautiful legend for Churn Status
    plt.legend(
        ["Active (False)", "Churned (True)"],
        title="Customer Status",
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
        frameon=True,
        facecolor="white",
        edgecolor="none"
    )
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"[OK] Saved clustered chart to {filename}")

async def callmetrics() :
    behavior_mean = analysis_call(data)
    print("Churn vs Call Metrics")
    print(behavior_mean)
    # Generate and save call metrics clustered chart
    plot_clustered_metrics(
        df_summary=behavior_mean,
        title="Average Number of Calls by Churn Status",
        ylabel="Average Calls",
        filename="churn_call_metrics_clustered.png"
    )
    
async def chargemetrics() :
    charge_mean = analysis_charge(data)
    print("Churn vs Charge Metrics")
    print(charge_mean)
    # Generate and save charge metrics clustered chart
    plot_clustered_metrics(
        df_summary=charge_mean,
        title="Average Charges by Churn Status",
        ylabel="Average Charge ($)",
        filename="churn_charge_metrics_clustered.png"
    )
    
async def minutemetrics() :
    minute_mean = analysis_minute(data)
    print("Churn vs Minute Metrics")
    print(minute_mean)
    # Generate and save minute metrics clustered chart
    plot_clustered_metrics(
        df_summary=minute_mean,
        title="Average Minutes by Churn Status",
        ylabel="Average Minutes",
        filename="churn_minute_metrics_clustered.png"
    )

async def combine_all_metrics():
    # 1. Fetch all data summaries
    behavior_mean = analysis_call(data)
    charge_mean = analysis_charge(data)
    minute_mean = analysis_minute(data)
    
    print("\n[OK] Generating combined metrics 3-panel clustered chart...")
    
    # 2. Set Seaborn aesthetics
    sns.set_theme(style="whitegrid")
    # Custom bar colors: Active (Light Blue-Gray), Churned (Dark Red)
    colors = ["#C5D0D6", "#D32F2F"]
    
    # 3. Create a 1x3 subplots figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 6.5), dpi=150)
    
    plots_config = [
        (behavior_mean, "Average Call Volume", "Average Calls", axes[0]),
        (charge_mean, "Average Monetary Charges", "Average Charge ($)", axes[1]),
        (minute_mean, "Average Usage Minutes", "Average Minutes", axes[2])
    ]
    
    for df, title, ylabel, ax in plots_config:
        df_transposed = df.T
        
        # Plot clustered bars onto the subplot axis
        df_transposed.plot(
            kind='bar',
            stacked=False,
            color=colors,
            width=0.6,
            edgecolor='none',
            ax=ax
        )
        
        # Add data labels on top of the bars
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f', padding=3, fontsize=8)
            
        # Subplot Titles and Axes
        ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
        ax.set_ylabel(ylabel, fontsize=10, labelpad=5)
        ax.set_xlabel("Time Period", fontsize=10, labelpad=5)
        
        # X-axis labels
        x_labels = [col.replace('Total ', '').title() for col in df_transposed.index]
        ax.set_xticklabels(x_labels, rotation=0)
        
        # Custom beautiful legend for each subplot
        ax.legend(
            ["Active (False)", "Churned (True)"],
            title="Customer Status",
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
    filename = "churn_combined_metrics_clustered.png"
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"[OK] Saved combined multi-panel clustered chart to {filename}")

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