import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
from matplotlib.ticker import FormatStrFormatter

output_folder = "./test_results"

def analyze_results(path):

    if os.path.isdir(path):
        csv_files = glob.glob(f'{path}/*.csv')
    elif os.path.isfile(path) and path.endswith('.csv'):
        csv_files = [path]
    else:
        raise ValueError(f"Invalid path or no CSV files found at {path}")
    print("Files found:", csv_files)

    frames = [pd.read_csv(file) for file in csv_files]

    if not frames:
        raise ValueError("No CSV data to process. Please check the input.")
    
    all_results = pd.concat(frames)
    status_counts = all_results.pivot_table(index='file', columns='status', aggfunc='size', fill_value=0)
    status_proportions = status_counts.div(status_counts.sum(axis=1), axis=0)
    average_durations = all_results.groupby('file')['duration'].mean()
    return status_proportions, average_durations, all_results

def calculate_test_frequencies(results, name):
    os.makedirs(output_folder, exist_ok=True)

    aggregated = results.pivot_table(index='id', columns='status', aggfunc='size', fill_value=0)
    aggregated['total_runs'] = aggregated.sum(axis=1)

    mean_durations = results.groupby('id')['duration'].mean()

    pass_fail_counts = aggregated.copy()
    pass_fail_counts['pass_rate (%)'] = (aggregated['passed'] / aggregated['total_runs'] * 100 )if 'passed' in aggregated.columns else 0
    pass_fail_counts['skip_rate (%)'] = (aggregated['skipped']  / aggregated['total_runs'] * 100) if 'skipped' in aggregated.columns else 0
    pass_fail_counts['fail_rate (%)'] = (aggregated['failed' ]/ aggregated['total_runs'] * 100) if 'failed' in aggregated.columns else 0
    pass_fail_counts['xfail_rate (%)'] = (aggregated['xfailed']/ aggregated['total_runs'] * 100) if 'xfailed' in aggregated.columns else 0

    pass_fail_counts['mean_duration (s)'] = mean_durations

    pass_fail_counts.reset_index(inplace=True)

    excel_path = f'{output_folder}/pass_fail_rates_{name}.xlsx'
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        pass_fail_counts.to_excel(writer, index= False, sheet_name= 'pass_fail_rates')
        workbook = writer.book
        worksheet = writer.sheets['pass_fail_rates']

        header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#D3D3D3', 'border': 1})
        
        for col_num, value in enumerate(pass_fail_counts.columns.values):
            worksheet.write(0, col_num, value, header_format)

        for i, col in enumerate(pass_fail_counts.columns):
            max_len = pass_fail_counts[col].astype(str).map(len).max()
            max_len = max(max_len, len(col))
            worksheet.set_column(i, i, max_len)
    
    return pass_fail_counts

def plot_fail_rates(pass_fail_counts, name):
    os.makedirs(output_folder, exist_ok=True)

    fail_rates = pass_fail_counts[pass_fail_counts['fail_rate (%)'] > 0 ]

    if fail_rates.empty:
        print("No failed tests to display.")
        return

    plt.figure(figsize=(14, 6))
    fail_rates.set_index('id')['fail_rate (%)'].plot(kind='barh', color='red', ax=plt.gca())
    plt.title(f'Fail Rates of Tests for {name}')
    plt.xlabel('Failure Rate')
    plt.ylabel('Test ID')
    plt.legend(['Fail Rate (%)'])
    plt.tight_layout()
    plt.savefig(f'{output_folder}/fail_rates_{name}.png')
    # plt.show()

def plot_results(pass_fail_counts, name):
    os.makedirs(output_folder, exist_ok=True)

    color_map = {
        'passed': 'green',
        'skipped': 'blue',
        'failed': 'red',
        'xfailed': 'orange'
    }

    status_to_key = {
        'pass_rate (%)': 'passed',
        'skip_rate (%)': 'skipped',
        'fail_rate (%)': 'failed',
        'xfail_rate (%)': 'xfailed'
    }

    filtered_data = pass_fail_counts[pass_fail_counts['total_runs'] > 0]

    if filtered_data.empty:
        print("No test data to display.")
        return

    ids_per_graph = 21
    total_ids = filtered_data.shape[0]
    num_graphs = (total_ids + ids_per_graph - 1) // ids_per_graph  
    
    status_columns = ['pass_rate (%)', 'skip_rate (%)', 'fail_rate (%)', 'xfail_rate (%)']
    existing_statuses = [col for col in status_columns if col in filtered_data.columns]
    colors = [color_map[status_to_key[col]] for col in existing_statuses]  
    
    for i in range(num_graphs):
        start_index = i * ids_per_graph
        end_index = start_index + ids_per_graph
        subset = filtered_data.iloc[start_index:end_index]

        plt.figure(figsize=(14, 8))
        ax = subset.set_index('id')[existing_statuses].plot(kind='barh', stacked=True, color=colors, ax=plt.gca())
        plt.title(f'Test Result Rates for {name} Part {i+1}')
        plt.xlabel('Rates (%)')
        plt.ylabel('Test ID')
        plt.legend([status_to_key[col].capitalize() for col in existing_statuses], title='Test Outcomes')  
        plt.tight_layout()
        plt.savefig(f'{output_folder}/status_rate_{name}_part_{i+1}.png')
        # plt.show()

def plot_mean_durations(pass_fail_counts, name):
    os.makedirs(output_folder, exist_ok=True)

    mean_durations = pass_fail_counts[pass_fail_counts['mean_duration (s)'] > 0]
    sorted_durations = mean_durations.sort_values(by='mean_duration (s)')

    ids_per_graph = 21
    total_ids = sorted_durations.shape[0]
    num_graphs = (total_ids + ids_per_graph - 1) // ids_per_graph  
    
    for i in range(num_graphs):
        start_index = i * ids_per_graph
        end_index = start_index + ids_per_graph
        subset = sorted_durations.iloc[start_index:end_index]

        plt.figure(figsize=(14, 8))
        plt.barh(subset['id'], subset['mean_duration (s)'], color='blue')
        plt.title(f'Average Test Durations for {name} Part {i+1}')
        plt.xlabel('Duration (seconds)')
        plt.ylabel('Test ID')
        plt.xscale('log')
        plt.tight_layout()
        plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.5f'))
        plt.savefig(f'{output_folder}/average_durations_{name}_part_{i+1}.png')
        # plt.show()

def main(directory='./result/csv_xtrack', pattern='results_xtrack_*.csv'):
    csv_files = glob.glob(os.path.join(directory, pattern))
    last_parts = []
    all_results_list = []

    for path in csv_files:
        filename = os.path.splitext(os.path.basename(path))[0]
        last_part = filename.split('_')[-2] + filename.split('_')[-1]
        name = filename.split('_')[-2]
        last_parts.append(last_part)
        status_proportions, average_durations, results = analyze_results(path)
        all_results_list.append(results)
        
    all_results = pd.concat(all_results_list)
    pass_fail_counts = calculate_test_frequencies(all_results, name)
    plot_fail_rates(pass_fail_counts, name)
    plot_results(pass_fail_counts, name)
    plot_mean_durations(pass_fail_counts, name)  

if __name__ == '__main__':
    main()