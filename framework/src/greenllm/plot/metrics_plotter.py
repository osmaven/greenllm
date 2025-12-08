import json
import numpy as np
import matplotlib.pyplot as plt



def plot_metrics(metrics: dict, metric_key: str, agg:str = 'avg') -> dict:
    """
    A partir de las métricas generadas, dibuja una gráfica agrupada por fichero de prompts y modelo.
    """

    info = {}

    if agg == 'avg':
        agg_label = 'Average'
        agg_function = np.average
    elif agg == 'sum':
        agg_label = 'Sum'
        agg_function = np.sum
    else raise Exception ('Aggregate method not supported')

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

    # Create bar plot
    bars = ax.bar(range(len(labels)), values, color=['#3498db', '#e74c3c', '#3498db', '#e74c3c'])

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



