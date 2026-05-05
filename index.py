import pandas as pd
import asyncio
data = pd.read_csv("./churn-bigml-20_new.csv")

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




async def callmetrics() :
    behavior_mean = analysis_call(data)
    print("Churn vs Call Metrics")
    print(behavior_mean)
    
async def chargemetrics() :
    charge_mean = analysis_charge(data)
    print("Churn vs Charge Metrics")
    print(charge_mean)
    
async def minutemetrics() :
    minute_mean = analysis_minute(data)
    print("Churn vs Minute Metrics")
    print(minute_mean)
    
    
if __name__ == "__main__":
    asyncio.run(callmetrics())
    asyncio.run(chargemetrics())
    asyncio.run(minutemetrics())