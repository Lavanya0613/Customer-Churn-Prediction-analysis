import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def setup_style():
    """Configure matplotlib/seaborn style for professional portfolio charts."""
    plt.style.use('default')
    sns.set_theme(style="whitegrid")
    sns.set_palette("muted")
    plt.rcParams.update({
        'font.size': 12,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 11,
        'figure.titlesize': 16,
        'figure.figsize': (10, 6)
    })

def plot_churn_rate_by_category(df, category_col, target_col='churn', title=None):
    """Plots both the absolute count and the churn rate for a categorical variable."""
    if title is None:
        title = f'Churn Rate by {category_col}'
        
    stats = df.groupby(category_col)[target_col].agg(['count', 'mean']).reset_index()
    stats = stats.rename(columns={'mean': 'churn_rate'})
    stats = stats.sort_values('churn_rate', ascending=False)
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Bar chart for counts
    sns.barplot(data=stats, x=category_col, y='count', color='lightgrey', ax=ax1, alpha=0.6)
    ax1.set_ylabel('Total Customers', color='grey')
    ax1.tick_params(axis='y', labelcolor='grey')
    
    # Line chart for churn rate
    ax2 = ax1.twinx()
    sns.pointplot(data=stats, x=category_col, y='churn_rate', color='red', ax=ax2, markers='o')
    ax2.set_ylabel('Churn Rate', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.set_ylim(0, max(stats['churn_rate']) * 1.2)
    
    # Format as percentage
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
    
    plt.title(title, pad=20)
    fig.tight_layout()
    return fig

def plot_distribution_by_churn(df, numeric_col, target_col='churn', title=None):
    """Plots a KDE/Histogram for a numeric variable split by churn status."""
    if title is None:
        title = f'Distribution of {numeric_col} by Churn Status'
        
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x=numeric_col, hue=target_col, kde=True, stat='density', 
                 common_norm=False, palette={0: 'green', 1: 'red'}, alpha=0.3, ax=ax)
    
    plt.title(title)
    fig.tight_layout()
    return fig

def plot_correlation_heatmap(df, numeric_cols, title="Correlation Heatmap"):
    """Plots a correlation heatmap for numerical features."""
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df[numeric_cols].corr()
    
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', 
                vmin=-1, vmax=1, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
    
    plt.title(title)
    fig.tight_layout()
    return fig
