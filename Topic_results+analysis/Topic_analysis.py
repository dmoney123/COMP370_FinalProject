import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# This script builds on Topic_Results.py by adding additional analysis pns

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# File paths (relative to script directory)
raw_data_path = os.path.join(script_dir, "topic_frequencies.csv")
file_path = os.path.join(script_dir, "percent_topic_frequency.csv")
output_path_1 = os.path.join(script_dir, "percent_topic_frequency_cleaned.csv")
output_path_2 = os.path.join(script_dir, "left_vs_right_vs_center.csv")
output_path_3 = os.path.join(script_dir, "pre_vs_post_election.csv")


def clean_percent_frequency_csv(input_path, output_path):
    """
    Clean the percent topic frequency CSV by removing ICE column and renaming from_json values.
    
    Args:
        input_path: Path to the input CSV file
        output_path: Path to save the cleaned CSV file
    """
    df = pd.read_csv(input_path)
    
    # Remove the ICE and US Politics columns
    columns_to_drop = ['ICE']
    if 'US Politics' in df.columns:
        columns_to_drop.append('US Politics')
    df = df.drop(columns=columns_to_drop)
    
    # Rename values in the from_json column to be more intuitive
    rename_mapping = {
        'Nov18_Center_post.json': 'center_postn',
        'Nov18_Center_pre.json': 'center_pre',
        'Nov18_Left_post.json': 'left_postn',
        'Nov18_Left_pre.json': 'left_pre',
        'Nov18_Right_post.json': 'right_post',
        'Nov18_Right_pre.json': 'right_pre'
    }
    
    df['from_json'] = df['from_json'].replace(rename_mapping)
    
    # Save the cleaned CSV
    df.to_csv(output_path, index=False)
    
    print("Cleaned CSV saved!")
    print(df.head())
    return df


def create_left_right_center_csv(input_path, output_path):
    """
    Create a CSV combining pre/post values for each political category (left, right, center).
    
    Args:
        input_path: Path to the raw topic frequencies CSV file
        output_path: Path to save the output CSV file
    """
    # Read raw data
    raw_df = pd.read_csv(input_path)
    
    # Remove ICE and US Politics columns
    columns_to_drop = ['ICE']
    if 'US Politics' in raw_df.columns:
        columns_to_drop.append('US Politics')
    raw_df = raw_df.drop(columns=columns_to_drop)
    
    # Extract category from from_json column
    def extract_category(row):
        if 'Left' in row or 'left' in row:
            return 'left'
        elif 'Right' in row or 'right' in row:
            return 'right'
        elif 'Center' in row or 'center' in row:
            return 'center'
        return None
    
    raw_df['category'] = raw_df['from_json'].apply(extract_category)
    
    # Group by category and sum all topic columns (exclude US Politics)
    topic_columns = [col for col in raw_df.columns if col not in ['from_json', 'category', 'US Politics']]
    grouped = raw_df.groupby('category')[topic_columns].sum().reset_index()
    
    # Rename category column to match desired output format
    grouped = grouped.rename(columns={'category': 'from_json'})
    
    # Calculate percentages for each row (each topic / row total * 100)
    row_totals = grouped[topic_columns].sum(axis=1)
    for col in topic_columns:
        grouped[col] = (grouped[col] / row_totals * 100).round(2)
    
    # Save to output path
    grouped.to_csv(output_path, index=False)
    
    print("\nLeft vs Right vs Center CSV saved!")
    print(grouped)
    return grouped


def create_pre_post_election_csv(input_path, output_path):
    """
    Create a CSV combining left/right/center values for each time period (pre, post).
    
    Args:
        input_path: Path to the raw topic frequencies CSV file
        output_path: Path to save the output CSV file
    """
    # Read raw data
    raw_df = pd.read_csv(input_path)
    
    # Remove ICE and US Politics columns
    columns_to_drop = ['ICE']
    if 'US Politics' in raw_df.columns:
        columns_to_drop.append('US Politics')
    raw_df = raw_df.drop(columns=columns_to_drop)
    
    # Extract pre/post from from_json column
    def extract_time_period(row):
        if 'pre' in row.lower() or 'Pre' in row:
            return 'pre'
        elif 'post' in row.lower() or 'Post' in row:
            return 'post'
        return None
    
    raw_df['time_period'] = raw_df['from_json'].apply(extract_time_period)
    
    # Group by time period and sum all topic columns (exclude US Politics)
    topic_columns = [col for col in raw_df.columns if col not in ['from_json', 'time_period', 'US Politics']]
    grouped = raw_df.groupby('time_period')[topic_columns].sum().reset_index()
    
    # Rename time_period column to match desired output format
    grouped = grouped.rename(columns={'time_period': 'from_json'})
    
    # Calculate percentages for each row (each topic / row total * 100)
    row_totals = grouped[topic_columns].sum(axis=1)
    for col in topic_columns:
        grouped[col] = (grouped[col] / row_totals * 100).round(2)
    
    # Save to output path
    grouped.to_csv(output_path, index=False)
    
    print("\nPre vs Post Election CSV saved!")
    print(grouped)
    return grouped


def create_plots(left_right_center_path, pre_post_path, save_plots=False, output_dir=None):
    """
    Create visualizations for topic analysis data.
    
    Args:
        left_right_center_path: Path to the left_vs_right_vs_center CSV file
        pre_post_path: Path to the pre_vs_post_election CSV file
        save_plots: If True, save plots to files. If False, display them (default: False)
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 8)
    
    # Read the data
    lrc_df = pd.read_csv(left_right_center_path)
    pp_df = pd.read_csv(pre_post_path)
    
    # Set output directory if saving
    if save_plots and output_dir is None:
        output_dir = script_dir
    
    # Color mapping: center=black, left=blue, right=red
    color_map = {
        'center': 'black',
        'left': 'blue',
        'right': 'red'
    }
    
    # Get topic columns (exclude from_json and US Politics)
    topic_cols_lrc = [col for col in lrc_df.columns if col not in ['from_json', 'US Politics']]
    topic_cols_pp = [col for col in pp_df.columns if col not in ['from_json', 'US Politics']]
    
    # Ensure consistent ordering for left/right/center plots
    lrc_df = lrc_df.sort_values('from_json').reset_index(drop=True)
    
    # Plot 1: Stacked bar chart - Left vs Right vs Center
    fig, ax = plt.subplots(figsize=(12, 6))
    plot_data = lrc_df.set_index('from_json')[topic_cols_lrc].T
    # Get colors for each category in the order they appear
    colors_list = [color_map.get(cat, 'gray') for cat in plot_data.columns]
    # Use color parameter - pandas will apply colors to each series
    ax = plot_data.plot(kind='bar', stacked=True, ax=ax, color=colors_list)
    ax.set_title('Topic Distribution: Left vs Right vs Center', fontsize=16, fontweight='bold')
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.legend(title='Political Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    if save_plots:
        plt.savefig(f"{output_dir}/left_right_center_stacked.png", dpi=300, bbox_inches='tight')
        print(f"\nSaved: {output_dir}/left_right_center_stacked.png")
        plt.close()
    else:
        plt.show()
    
    # Plot 2: Grouped bar chart - Left vs Right vs Center
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(topic_cols_lrc))
    width = 0.25
    for i, category in enumerate(lrc_df['from_json']):
        values = lrc_df[lrc_df['from_json'] == category][topic_cols_lrc].values[0]
        color = color_map.get(category, 'gray')
        ax.bar(x + i*width, values, width, label=category.capitalize(), color=color)
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_title('Topic Distribution Comparison: Left vs Right vs Center', fontsize=16, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(topic_cols_lrc, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    if save_plots:
        plt.savefig(f"{output_dir}/left_right_center_grouped.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/left_right_center_grouped.png")
        plt.close()
    else:
        plt.show()
    
    # Plot 3: Stacked bar chart - Pre vs Post Election
    fig, ax = plt.subplots(figsize=(12, 6))
    pp_df.set_index('from_json')[topic_cols_pp].T.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
    ax.set_title('Topic Distribution: Pre vs Post Election', fontsize=16, fontweight='bold')
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.legend(title='Time Period', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    plt.tight_layout()
    if save_plots:
        plt.savefig(f"{output_dir}/pre_post_stacked.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/pre_post_stacked.png")
        plt.close()
    else:
        plt.show()
    
    # Plot 4: Grouped bar chart - Pre vs Post Election
    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(topic_cols_pp))
    width = 0.35
    for i, period in enumerate(pp_df['from_json']):
        values = pp_df[pp_df['from_json'] == period][topic_cols_pp].values[0]
        ax.bar(x + i*width, values, width, label=period.capitalize())
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_title('Topic Distribution Comparison: Pre vs Post Election', fontsize=16, fontweight='bold')
    ax.set_xticks(x + width/2)
    ax.set_xticklabels(topic_cols_pp, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    if save_plots:
        plt.savefig(f"{output_dir}/pre_post_grouped.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/pre_post_grouped.png")
        plt.close()
    else:
        plt.show()
    


def plot_top_topics_by_bias(cleaned_csv_path, n_topics=5, save_plots=False, output_dir=None):
    """
    Create horizontal bar chart showing top N topics for each political bias.
    
    Args:
        cleaned_csv_path: Path to the cleaned percent topic frequency CSV
        n_topics: Number of top topics to show per bias (default: 5)
        save_plots: If True, save plots to files. If False, display them
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    df = pd.read_csv(cleaned_csv_path)
    
    # Color mapping
    color_map = {
        'center': 'black',
        'left': 'blue',
        'right': 'red'
    }
    
    # Extract bias from from_json column
    df['bias'] = df['from_json'].str.split('_').str[0]
    
    # Get topic columns (exclude from_json, bias, and US Politics)
    topic_cols = [col for col in df.columns if col not in ['from_json', 'bias', 'US Politics']]
    
    # Aggregate by bias (average across pre/post)
    bias_df = df.groupby('bias')[topic_cols].mean().reset_index()
    
    # Create subplots for each bias
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    biases = ['left', 'center', 'right']
    
    for idx, bias in enumerate(biases):
        ax = axes[idx]
        bias_data = bias_df[bias_df['bias'] == bias].iloc[0]
        
        # Get top N topics - convert to Series and ensure numeric
        topic_values = bias_data[topic_cols].astype(float)
        top_topics = topic_values.nlargest(n_topics)
        top_topics = top_topics.sort_values()
        
        # Create horizontal bar chart
        color = color_map.get(bias, 'gray')
        ax.barh(range(len(top_topics)), top_topics.values, color=color)
        ax.set_yticks(range(len(top_topics)))
        ax.set_yticklabels(top_topics.index, fontsize=10)
        ax.set_xlabel('Percentage (%)', fontsize=11)
        ax.set_title(f'Top {n_topics} Topics: {bias.capitalize()}', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    if save_plots:
        if output_dir is None:
            output_dir = script_dir
        plt.savefig(f"{output_dir}/top_topics_by_bias.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/top_topics_by_bias.png")
        plt.close()
    else:
        plt.show()


def plot_pre_post_change_by_bias(cleaned_csv_path, save_plots=False, output_dir=None):
    """
    Create grouped bar chart showing pre/post changes for key topics by bias.
    
    Args:
        cleaned_csv_path: Path to the cleaned percent topic frequency CSV
        save_plots: If True, save plots to files. If False, display them
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    df = pd.read_csv(cleaned_csv_path)
    
    # Color mapping
    color_map = {
        'center': 'black',
        'left': 'blue',
        'right': 'red'
    }
    
    # Extract bias and time period
    df['bias'] = df['from_json'].str.split('_').str[0]
    df['time'] = df['from_json'].str.split('_').str[1].str.replace('postn', 'post')
    
    # Get topic columns (exclude from_json, bias, time, and US Politics)
    topic_cols = [col for col in df.columns if col not in ['from_json', 'bias', 'time', 'US Politics']]
    
    # Select key topics (top 5 most prominent overall)
    all_means = df[topic_cols].astype(float).mean()
    key_topics = all_means.nlargest(5).index.tolist()
    
    # Create plot
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    biases = ['left', 'center', 'right']
    
    for idx, bias in enumerate(biases):
        ax = axes[idx]
        bias_data = df[df['bias'] == bias]
        
        x = np.arange(len(key_topics))
        width = 0.35
        
        pre_values = bias_data[bias_data['time'] == 'pre'][key_topics].iloc[0].values
        post_values = bias_data[bias_data['time'] == 'post'][key_topics].iloc[0].values
        
        color = color_map.get(bias, 'gray')
        ax.bar(x - width/2, pre_values, width, label='Pre', color=color, alpha=0.6)
        ax.bar(x + width/2, post_values, width, label='Post', color=color, alpha=1.0)
        
        ax.set_xlabel('Topics', fontsize=11)
        ax.set_ylabel('Percentage (%)', fontsize=11)
        ax.set_title(f'Pre/Post Comparison: {bias.capitalize()}', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(key_topics, rotation=45, ha='right', fontsize=9)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    if save_plots:
        if output_dir is None:
            output_dir = script_dir
        plt.savefig(f"{output_dir}/pre_post_change_by_bias.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/pre_post_change_by_bias.png")
        plt.close()
    else:
        plt.show()


def plot_topic_prominence_heatmap(cleaned_csv_path, save_plots=False, output_dir=None):
    """
    Create heatmap showing topic prominence across all biases.
    
    Args:
        cleaned_csv_path: Path to the cleaned percent topic frequency CSV
        save_plots: If True, save plots to files. If False, display them
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    df = pd.read_csv(cleaned_csv_path)
    
    # Extract bias from from_json column
    df['bias'] = df['from_json'].str.split('_').str[0]
    
    # Get topic columns (exclude from_json, bias, and US Politics)
    topic_cols = [col for col in df.columns if col not in ['from_json', 'bias', 'US Politics']]
    
    # Aggregate by bias (average across pre/post)
    bias_df = df.groupby('bias')[topic_cols].mean().reset_index()
    bias_df = bias_df.set_index('bias')
    
    # Reorder rows: center, left, right
    desired_order = ['center', 'left', 'right']
    bias_df = bias_df.reindex([cat for cat in desired_order if cat in bias_df.index])
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(14, 4))
    sns.heatmap(bias_df, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, 
                cbar_kws={'label': 'Percentage (%)'}, linewidths=0.5)
    ax.set_title('Topic Prominence Heatmap by Political Bias', fontsize=16, fontweight='bold')
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Political Bias', fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    if save_plots:
        if output_dir is None:
            output_dir = script_dir
        plt.savefig(f"{output_dir}/topic_prominence_heatmap.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/topic_prominence_heatmap.png")
        plt.close()
    else:
        plt.show()


def plot_change_magnitude(cleaned_csv_path, save_plots=False, output_dir=None):
    """
    Create bar chart showing percentage point change (post - pre) for each topic by bias.
    
    Args:
        cleaned_csv_path: Path to the cleaned percent topic frequency CSV
        save_plots: If True, save plots to files. If False, display them
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    df = pd.read_csv(cleaned_csv_path)
    
    # Color mapping
    color_map = {
        'center': 'black',
        'left': 'blue',
        'right': 'red'
    }
    
    # Extract bias and time period
    df['bias'] = df['from_json'].str.split('_').str[0]
    df['time'] = df['from_json'].str.split('_').str[1].str.replace('postn', 'post')
    
    # Get topic columns (exclude from_json, bias, time, and US Politics)
    topic_cols = [col for col in df.columns if col not in ['from_json', 'bias', 'time', 'US Politics']]
    
    # Calculate changes for each bias
    changes_data = []
    biases = ['left', 'center', 'right']
    
    for bias in biases:
        bias_data = df[df['bias'] == bias]
        pre_data = bias_data[bias_data['time'] == 'pre'][topic_cols].iloc[0]
        post_data = bias_data[bias_data['time'] == 'post'][topic_cols].iloc[0]
        changes = post_data - pre_data
        changes_data.append({
            'bias': bias,
            **changes.to_dict()
        })
    
    changes_df = pd.DataFrame(changes_data)
    
    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(16, 6))
    x = np.arange(len(topic_cols))
    width = 0.25
    
    for i, bias in enumerate(biases):
        values = changes_df[changes_df['bias'] == bias][topic_cols].iloc[0].values
        color = color_map.get(bias, 'gray')
        ax.bar(x + i*width, values, width, label=bias.capitalize(), color=color)
    
    ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Percentage Point Change (Post - Pre)', fontsize=12)
    ax.set_title('Topic Change Magnitude: Pre vs Post Election by Bias', fontsize=16, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(topic_cols, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    if save_plots:
        if output_dir is None:
            output_dir = script_dir
        plt.savefig(f"{output_dir}/change_magnitude.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/change_magnitude.png")
        plt.close()
    else:
        plt.show()


def plot_topic_composition_timeline(cleaned_csv_path, save_plots=False, output_dir=None):
    """
    Create stacked area/bar chart showing topic composition over time (pre → post) for each bias.
    
    Args:
        cleaned_csv_path: Path to the cleaned percent topic frequency CSV
        save_plots: If True, save plots to files. If False, display them
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    df = pd.read_csv(cleaned_csv_path)
    
    # Color mapping
    color_map = {
        'center': 'black',
        'left': 'blue',
        'right': 'red'
    }
    
    # Extract bias and time period
    df['bias'] = df['from_json'].str.split('_').str[0]
    df['time'] = df['from_json'].str.split('_').str[1].str.replace('postn', 'post')
    
    # Get topic columns (exclude from_json, bias, time, and US Politics)
    topic_cols = [col for col in df.columns if col not in ['from_json', 'bias', 'time', 'US Politics']]
    
    # Create subplots for each bias
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    biases = ['left', 'center', 'right']
    
    for idx, bias in enumerate(biases):
        ax = axes[idx]
        bias_data = df[df['bias'] == bias].sort_values('time')
        
        # Prepare data for stacked area
        time_order = ['pre', 'post']
        plot_data = []
        for time in time_order:
            row_data = bias_data[bias_data['time'] == time][topic_cols].iloc[0]
            plot_data.append(row_data.values)
        
        plot_df = pd.DataFrame(plot_data, columns=topic_cols, index=time_order)
        
        # Create stacked bar chart
        plot_df.T.plot(kind='bar', stacked=True, ax=ax, width=0.6)
        ax.set_xlabel('Topics', fontsize=11)
        ax.set_ylabel('Percentage (%)', fontsize=11)
        ax.set_title(f'Topic Composition: {bias.capitalize()}', fontsize=14, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=9)
        ax.legend(title='Time Period', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    if save_plots:
        if output_dir is None:
            output_dir = script_dir
        plt.savefig(f"{output_dir}/topic_composition_timeline.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/topic_composition_timeline.png")
        plt.close()
    else:
        plt.show()


def plot_top_topics_comparison(cleaned_csv_path, n_topics=3, save_plots=False, output_dir=None):
    """
    Create side-by-side comparison of top N topics for each bias.
    
    Args:
        cleaned_csv_path: Path to the cleaned percent topic frequency CSV
        n_topics: Number of top topics to show (default: 3)
        save_plots: If True, save plots to files. If False, display them
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    df = pd.read_csv(cleaned_csv_path)
    
    # Color mapping
    color_map = {
        'center': 'black',
        'left': 'blue',
        'right': 'red'
    }
    
    # Extract bias from from_json column
    df['bias'] = df['from_json'].str.split('_').str[0]
    
    # Get topic columns (exclude from_json, bias, and US Politics)
    topic_cols = [col for col in df.columns if col not in ['from_json', 'bias', 'US Politics']]
    
    # Aggregate by bias (average across pre/post)
    bias_df = df.groupby('bias')[topic_cols].mean().reset_index()
    
    # Get top N topics for each bias
    biases = ['left', 'center', 'right']
    all_top_topics = set()
    
    for bias in biases:
        bias_data = bias_df[bias_df['bias'] == bias].iloc[0]
        topic_values = bias_data[topic_cols].astype(float)
        top_topics = topic_values.nlargest(n_topics).index.tolist()
        all_top_topics.update(top_topics)
    
    # Create comparison plot
    fig, ax = plt.subplots(figsize=(16, 8))
    
    x = np.arange(len(all_top_topics))
    width = 0.25
    
    for i, bias in enumerate(biases):
        bias_data = bias_df[bias_df['bias'] == bias].iloc[0]
        values = [bias_data.get(topic, 0) for topic in all_top_topics]
        color = color_map.get(bias, 'gray')
        ax.bar(x + i*width, values, width, label=bias.capitalize(), color=color)
    
    ax.set_xlabel('Topics', fontsize=12)
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_title(f'Top {n_topics} Topics Comparison Across Political Biases', fontsize=16, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(all_top_topics, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    if save_plots:
        if output_dir is None:
            output_dir = script_dir
        plt.savefig(f"{output_dir}/top_topics_comparison.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/top_topics_comparison.png")
        plt.close()
    else:
        plt.show()


def plot_top_topics_pre_post_change(cleaned_csv_path, n_topics=5, save_plots=False, output_dir=None):
    """
    Create visualization showing how the most prominent topics for each bias change from pre to post election.
    
    Args:
        cleaned_csv_path: Path to the cleaned percent topic frequency CSV
        n_topics: Number of top topics to show per bias (default: 5)
        save_plots: If True, save plots to files. If False, display them
        output_dir: Directory to save plots (only used if save_plots=True)
    """
    df = pd.read_csv(cleaned_csv_path)
    
    # Color mapping
    color_map = {
        'center': 'black',
        'left': 'blue',
        'right': 'red'
    }
    
    # Extract bias and time period
    df['bias'] = df['from_json'].str.split('_').str[0]
    df['time'] = df['from_json'].str.split('_').str[1].str.replace('postn', 'post')
    
    # Get topic columns (exclude from_json, bias, time, and US Politics)
    topic_cols = [col for col in df.columns if col not in ['from_json', 'bias', 'time', 'US Politics']]
    
    # Create subplots for each bias
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    biases = ['left', 'center', 'right']
    
    for idx, bias in enumerate(biases):
        ax = axes[idx]
        bias_data = df[df['bias'] == bias]
        
        # Get pre and post data
        pre_data = bias_data[bias_data['time'] == 'pre'][topic_cols].iloc[0]
        post_data = bias_data[bias_data['time'] == 'post'][topic_cols].iloc[0]
        
        # Find top N topics based on average of pre and post
        pre_data = pre_data.astype(float)
        post_data = post_data.astype(float)
        avg_data = (pre_data + post_data) / 2
        top_topics = avg_data.nlargest(n_topics).index.tolist()
        
        # Get values for top topics
        pre_values = [pre_data[topic] for topic in top_topics]
        post_values = [post_data[topic] for topic in top_topics]
        
        # Create grouped bar chart
        x = np.arange(len(top_topics))
        width = 0.35
        color = color_map.get(bias, 'gray')
        
        bars1 = ax.bar(x - width/2, pre_values, width, label='Pre', color=color, alpha=0.6)
        bars2 = ax.bar(x + width/2, post_values, width, label='Post', color=color, alpha=1.0)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}%',
                       ha='center', va='bottom', fontsize=8)
        
        # Draw arrows showing change direction
        for i, topic in enumerate(top_topics):
            pre_val = pre_values[i]
            post_val = post_values[i]
            change = post_val - pre_val
            
            if abs(change) > 0.5:  # Only show arrows for meaningful changes
                arrow_color = 'green' if change > 0 else 'red'
                arrow_style = '->' if change > 0 else '<-'
                ax.annotate('', xy=(i + width/2, post_val), xytext=(i - width/2, pre_val),
                           arrowprops=dict(arrowstyle=arrow_style, color=arrow_color, lw=1.5, alpha=0.7))
        
        ax.set_xlabel('Top Topics', fontsize=11)
        ax.set_ylabel('Percentage (%)', fontsize=11)
        ax.set_title(f'Top {n_topics} Topics: {bias.capitalize()} (Pre vs Post)', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(top_topics, rotation=45, ha='right', fontsize=9)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    if save_plots:
        if output_dir is None:
            output_dir = script_dir
        plt.savefig(f"{output_dir}/top_topics_pre_post_change.png", dpi=300, bbox_inches='tight')
        print(f"Saved: {output_dir}/top_topics_pre_post_change.png")
        plt.close()
    else:
        print("\nDisplaying top topics pre/post change plot...")
        plt.show()


if __name__ == "__main__":
    # Run all three functions
    clean_percent_frequency_csv(file_path, output_path_1)
    create_left_right_center_csv(raw_data_path, output_path_2)
    create_pre_post_election_csv(raw_data_path, output_path_3)
    
    #Create original plots

    create_plots(output_path_2, output_path_3)
    plot_top_topics_pre_post_change(output_path_1, n_topics=5)
    plot_pre_post_change_by_bias(output_path_1)
    
    
    
    # Uncomment the ones you want to generate:
    
    """
    plot_pre_post_change_by_bias(output_path_1)
    plot_topic_prominence_heatmap(output_path_1)
    plot_change_magnitude(output_path_1)
    plot_topic_composition_timeline(output_path_1)
    plot_top_topics_comparison(output_path_1, n_topics=3)
"""