import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_histogram_msg_deleted_users(csv_file, output_folder):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(8, 6))
    plt.hist(df['msg_deleted_users'], bins=20, color='#7289DA', edgecolor='#445282')
    plt.title('Number of Deleted User Messages')
    plt.xlabel('Messages')
    plt.ylabel('Frequency')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'histogram_msg_deleted_users.png'))
    plt.show()

def plot_histogram_qtd_users(csv_file, output_folder):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(8, 6))
    plt.hist(df['qtd_users'], bins=20, color='#7289DA', edgecolor='#445282')
    plt.title('Number of Active Users')
    plt.xlabel('Users')
    plt.ylabel('Frequency')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'histogram_qtd_users.png'))
    plt.show()

def plot_histogram_tot_msg(csv_file, output_folder):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(8, 6))
    plt.hist(df['tot_msg'], bins=20, color='#7289DA', edgecolor='#445282')
    plt.title('Total Messages')
    plt.xlabel('Messages')
    plt.ylabel('Frequency')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'histogram_tot_msg.png'))
    plt.show()

def plot_histogram_rz_dlt_tot_msg(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    df_sorted = df.sort_values(by='rz_dlt_tot_msg', ascending=False)

    plt.figure(figsize=(8, 6))
    plt.hist(df_sorted['rz_dlt_tot_msg'], bins=20, color='#7289DA', edgecolor='#445282')
    plt.title('Ratio of Deleted Users to Total Messages')
    plt.xlabel('Ratio')
    plt.ylabel('Frequency')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'histogram_rz_dlt_tot_msg.png'))
    plt.show()

def plot_razao_mensagens_deletadas(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    df_sorted = df.sort_values(by='rz_dlt_tot_msg', ascending=False)

    razoes = df_sorted["rz_dlt_tot_msg"]

    plt.figure(figsize=(10, 6))
    plt.bar(df.index, razoes, color='#7289DA', edgecolor='#445282')
    plt.xlabel('Server')
    plt.ylabel('Ratio of Deleted Messages')
    plt.title('Ratio of Deleted Users Messages to Total Messages by Server')
    plt.xticks([])  # Remove os rótulos do eixo x
    plt.tight_layout()
    
    plt.savefig(output_folder + '/histograms_rz_msg_del.png')

    plt.show()

def plot_scatter_mensagens_deletadas(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    df_sorted = df.sort_values(by='rz_dlt_tot_msg', ascending=False)

    mensagens_totais = df_sorted["tot_msg"]
    mensagens_deletadas = df_sorted["msg_deleted_users"]

    plt.figure(figsize=(10, 6))
    plt.scatter(mensagens_totais, mensagens_deletadas, color='#7289DA', alpha=0.5)
    plt.xlabel('Total Number of Messages')
    plt.ylabel('Number of Deleted User Messages')
    plt.title('Relationship between Total Messages and Deleted User Messages by Server')
    plt.grid(True)
    
    plt.tight_layout()

    plt.savefig(output_folder + '/histograms_scatter_msg_del.png')

    plt.show()

def plot_barras_agrupadas_msg_tot(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    # df = df.sort_values(by='tot_msg', ascending=False)
    df_sorted = df.sort_values(by='tot_msg', ascending=False) 

    mensagens_totais = df_sorted["tot_msg"]

    plt.figure(figsize=(10, 6))
    plt.bar(df.index, mensagens_totais, color='#7289DA', edgecolor='#445282')
    plt.xlabel('Server')
    plt.ylabel('Total Number of Messages')
    plt.title('Total Messages per Server')
    plt.xticks([])
    plt.tight_layout()

    plt.savefig(output_folder + '/histograms_ag_msg_tot.png')

    plt.show()

def plot_barras_empilhadas_msg_tot_del(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    df_sorted = df.sort_values(by='tot_msg', ascending=False) 


    mensagens_totais = df_sorted["tot_msg"]
    mensagens_deletadas = df_sorted["msg_deleted_users"]

    plt.figure(figsize=(10, 6))
    plt.bar(df.index, mensagens_totais, color='#7289DA', label='Total Messages', edgecolor='#445282')
    plt.bar(df.index, mensagens_deletadas, bottom=mensagens_totais, color='#ecad46', label='Deleted User Messages', edgecolor='#445282')
    plt.xlabel('Server')
    plt.ylabel('Number of Messages')
    plt.title('Number of Messages per Server')
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_folder + '/histograms_be_msg_tot_del.png')

    plt.show()

def plot_pontos_msg_tot(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    df_sorted = df.sort_values(by='tot_msg', ascending=False) 

    plt.figure(figsize=(10, 6))
    plt.scatter(df.index, df_sorted['tot_msg'], color='#7289DA', alpha=0.5)
    plt.xlabel('Server Index')
    plt.ylabel('Total Number of Messages')
    plt.title('Total Messages per Server')
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'scatter_msg_tot.png'))
    plt.show()

def plot_boxplot(csv_file, output_folder):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10, 6))
    df[['tot_msg', 'msg_deleted_users']].plot(kind='box', vert=False)
    plt.title('Boxplot of Total Messages and Deleted User Messages')
    plt.xlabel('Messages')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'boxplot_msg.png'))
    plt.show()

def plot_density(csv_file, output_folder):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10, 6))
    df['tot_msg'].plot(kind='density', color='blue', label='Total Messages')
    df['msg_deleted_users'].plot(kind='density', color='red', label='Deleted User Messages')
    plt.title('Density Plot of Messages')
    plt.xlabel('Messages')
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'density_plot_msg.png'))
    plt.show()


def plot_correlation_heatmap(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    numeric_df = df.select_dtypes(include=[np.number])
    if 'rz_dlt_tot_msg' in numeric_df.columns:
        numeric_df = numeric_df.drop('rz_dlt_tot_msg', axis=1)
    
    correlation = numeric_df.corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='crest', center=0)
    plt.title('Correlation Heatmap')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'correlation_heatmap.png'))
    plt.show()

def plot_violin(csv_file, output_folder):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df[['tot_msg', 'msg_deleted_users']])
    plt.title('Violin Plot of Messages')
    plt.ylabel('Frequency')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'violin_plot_msg.png'))
    plt.show()

def plot_stacked_bar_normalized(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    df['deleted_ratio'] = df['msg_deleted_users'] / df['tot_msg']
    df_sorted = df.sort_values('deleted_ratio', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.bar(df_sorted.index, df_sorted['deleted_ratio'], color='red', edgecolor='black', alpha=0.7)
    plt.xlabel('Server')
    plt.ylabel('Ratio of Deleted Messages')
    plt.title('Normalized Stacked Bar of Deleted Messages Ratio')
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'normalized_stacked_bar.png'))
    plt.show()

def plot_binned_bar_chart(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    
    max_messages = df['tot_msg'].max()
    bin_edges = list(range(0, max_messages, max_messages // 20))
    bin_edges.append(max_messages)
    
    bin_labels = [f"{round(edge/1000)}k-{round(bin_edges[i+1]/1000)}k" for i, edge in enumerate(bin_edges[:-1])]

    df['message_bin'] = pd.cut(df['tot_msg'], bins=bin_edges, labels=bin_labels, right=False)
    
    bin_counts = df['message_bin'].value_counts().sort_index()
    
    plt.figure(figsize=(15, 8))
    bin_counts.plot(kind='bar', color='#7289DA', edgecolor='#445282')
    plt.xlabel('Number of Messages')
    plt.ylabel('Number of Servers')
    plt.title('Number of Servers per Message Bin')
    
    plt.xticks(ticks=range(len(bin_labels)), labels=bin_labels, rotation=45, ha='right')
    
    plt.tight_layout()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plt.savefig(os.path.join(output_folder, 'binned_bar_chart_bins.png'))
    plt.show()

def plot_stacked_binned_bar_chart(csv_file, output_folder):
    df = pd.read_csv(csv_file)
    
    max_messages = max(df['tot_msg'].max(), df['msg_deleted_users'].max())
    bin_edges = list(range(0, max_messages, max_messages // 20))
    bin_edges.append(max_messages)
    bin_labels = [f"{bin_edges[i]}-{bin_edges[i+1]}" for i in range(len(bin_edges)-1)]
    
    df['total_message_bin'] = pd.cut(df['tot_msg'], bins=bin_edges, labels=bin_labels, right=False)
    df['deleted_message_bin'] = pd.cut(df['msg_deleted_users'], bins=bin_edges, labels=bin_labels, right=False)
    
    total_bin_counts = df['total_message_bin'].value_counts().sort_index()
    deleted_bin_counts = df['deleted_message_bin'].value_counts().sort_index()
    
    plt.figure(figsize=(15, 8))
    total_bin_counts.plot(kind='bar', color='#7289DA', edgecolor='#445282', label='Total Messages')
    deleted_bin_counts.plot(kind='bar', color='#ecad46', edgecolor='#445282', label='Deleted User Messages', bottom=total_bin_counts)
    
    plt.xlabel('Message Bins')
    plt.ylabel('Number of Servers')
    plt.title('Number of Servers per Message Bin (Stacked)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(output_folder, 'stacked_binned_bar_chart.png'))
    plt.show()

def plot_histograms_from_csv(csv_file, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plot_histogram_msg_deleted_users(csv_file, output_folder)
    plot_histogram_qtd_users(csv_file, output_folder)
    plot_histogram_tot_msg(csv_file, output_folder)
    plot_histogram_rz_dlt_tot_msg(csv_file, output_folder)
    plot_razao_mensagens_deletadas(csv_file, output_folder)
    plot_scatter_mensagens_deletadas(csv_file, output_folder)
    plot_barras_agrupadas_msg_tot(csv_file, output_folder)
    plot_barras_empilhadas_msg_tot_del(csv_file, output_folder)
    plot_pontos_msg_tot(csv_file, output_folder)
    plot_boxplot(csv_file, output_folder)
    plot_density(csv_file, output_folder)
    plot_correlation_heatmap(csv_file, output_folder)
    plot_stacked_bar_normalized(csv_file, output_folder)
    plot_violin(csv_file, output_folder)
    plot_binned_bar_chart(csv_file, output_folder)
    plot_stacked_binned_bar_chart(csv_file, output_folder)

csv_file = 'colected_info.csv'
output_folder = 'histogram_images'

plot_histograms_from_csv(csv_file, output_folder)