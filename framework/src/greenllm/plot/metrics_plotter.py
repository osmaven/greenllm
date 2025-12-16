import json
import numpy as np
import matplotlib.pyplot as plt

def identity(l):
    return l


def plot_metrics(metrics: dict, metric_key: str, agg:str = 'avg', plot = 'bar') -> dict:
    """
    A partir de las métricas generadas, dibuja una gráfica agrupada por fichero de prompts y modelo.
    """

    info = {}

    if plot == 'bar':
        if agg == 'avg':
            agg_label = 'Average'
            agg_function = np.average
        elif agg == 'sum':
            agg_label = 'Sum'
            agg_function = np.sum
        else:
            raise Exception ('Aggregate method not supported')
    elif plot == 'box':
        agg_label = 'Distribution of '
        agg_function = identity
    else:
        raise Exception ('Plot not supported')

    for prompt_set, models in metrics.items():
        prompt_name = prompt_set.split('/')[-1].replace('.txt', '')
        
        for model_name, model_data in models.items():
            model_short = model_name.split('/')[-1]
            
            # Flatten all metric values and calculate average
            metric_values = model_data['metrics'][metric_key]
            all_values = [val for sublist in metric_values for val in sublist]
            metric_value = agg_function(all_values)
            
            key = f"{prompt_name}_{model_short}"
            info[key] = metric_value


    labels = list(info.keys())
    values = list(info.values())

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    if plot == 'bar':
        # Create bar plot
        bars = ax.bar(range(len(labels)), values, color=['#3498db', '#e74c3c', '#3498db', '#e74c3c'])
    elif plot == 'box':
        positions = range(1, len(values) + 1)
        boxplot = ax.boxplot(values, 
                labels=range(len(labels)),
                patch_artist=True,
                notch=True,
                showmeans=True,
                meanprops=dict(marker='D', markerfacecolor='red', markeredgecolor='red', markersize=6))

    # Customize the plot
    ax.set_xlabel('Model - Prompt Set', fontsize=12, fontweight='bold')
    ax.set_ylabel(f'{agg_label} {metric_key}', fontsize=12, fontweight='bold')
    ax.set_title(f'{agg_label} {metric_key} by Model and Prompt Set', 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')

    # Add value labels on top of bars
    for i, (label, value) in enumerate(zip(labels, values)):
        ax.text(i, value, f'{value:.4f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.show()

def plot_metrics_comparison(metrics: dict, metric_key_x: str = 'w_per_token', metric_key_y: str = 'co2e_g_per_1k_tokens',
metric_key_bubble: str = 'tokens_per_second', agg:str = 'avg') -> dict:

    # Prepare data for scatter plot
    scatter_data = []

    for prompt_set, models in metrics.items():
        prompt_name = prompt_set.split('/')[-1].replace('.txt', '').replace('prompt_set_', '')

        for model_name, model_data in models.items():
            model_short = model_name.split('/')[-1]

            # Flatten metrics
            metrics = model_data['metrics']

            metric_x_values = []
            for sublist in metrics[metric_key_x]:
                if isinstance(sublist, list):
                    metric_x_values.extend(sublist)
                else:
                    metric_x_values.append(sublist)

            metric_y_values = []
            for sublist in metrics[metric_key_y]:
                if isinstance(sublist, list):
                    metric_y_values.extend(sublist)
                else:
                    metric_y_values.append(sublist)

            metric_bubble_values = []
            for sublist in metrics[metric_key_bubble]:
                if isinstance(sublist, list):
                    metric_bubble_values.extend(sublist)
                else:
                    metric_bubble_values.append(sublist)

            # Calculate averages
            avg_metric_x_values = np.mean(metric_x_values)
            avg_metric_y_values = np.mean(metric_y_values)
            avg_metric_bubble_values = np.mean(metric_bubble_values)

            scatter_data.append({
                'model': model_short,
                'prompt': prompt_name,
                'label': f"{model_short}-{prompt_name}",
                'metric_x_values': avg_metric_x_values,
                'metric_y_values': avg_metric_y_values,
                'metric_bubble_values': avg_metric_bubble_values,
                'size': len(metric_x_values)  # Number of data points
            })

    # Create scatter plot
    fig, ax = plt.subplots(figsize=(14, 8))

    # Define colors for different model-prompt combinations
    colors = ['#3498db', '#2980b9', '#e74c3c', '#c0392b']
    label_offsets = [
        (0, 10),   
        (0, -15),  
        (0, 10),  
        (0, -15)  
    ]


    # Plot each point
    for i, item in enumerate(scatter_data):
        color = colors[i % len(colors)]
        offset = label_offsets[i % len(label_offsets)]

        # Size based on number of samples (scaled for visibility)
        size = item['size'] * 100

        ax.scatter(item['metric_x_values'],
                item['metric_y_values'],
                s=size, 
                c=color, 
                alpha=0.6, 
                edgecolors='black',
                linewidth=1.5,
                label=item['label'])

        # Add labels
        ax.annotate(item['label'],
                    xy=(item['metric_x_values'], item['metric_y_values']),
                    xytext=offset,
                    textcoords='offset points',
                    fontsize=8,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='gray', linewidth=0.5),
                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

    # Customize the plot
    ax.set_xlabel(metric_key_x, fontsize=12, fontweight='bold')
    ax.set_ylabel(metric_key_y, fontsize=12, fontweight='bold')
    ax.set_title(f'{metric_key_x} vs {metric_key_y}\nBubble size represents {metric_key_bubble}',
                fontsize=14, fontweight='bold', pad=20)

    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Add legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='best', fontsize=10, framealpha=0.9)

    plt.tight_layout()
    plt.show()