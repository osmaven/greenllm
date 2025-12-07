import json
import numpy as np
import matplotlib.pyplot as plt



def plot_metrics(metrics: dict) -> dict:
    """
    A partir de las métricas generadas, dibuja una gráfica agrupada por fichero de prompts y modelo.
    """

    info = {}

    for prompt_set, models in metrics.items():
        prompt_name = prompt_set.split('/')[-1].replace('.txt', '')
        
        for model_name, model_data in models.items():
            model_short = model_name.split('/')[-1]
            
            # Flatten all w_per_token values and calculate average
            w_per_token_values = model_data['metrics']['w_per_token']
            all_values = [val for sublist in w_per_token_values for val in sublist]
            avg_w_per_token = np.average(all_values)
            
            key = f"{prompt_name}_{model_short}"
            info[key] = avg_w_per_token


    labels = list(info.keys())
    values = list(info.values())

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create bar plot
    bars = ax.bar(range(len(labels)), values, color=['#3498db', '#e74c3c', '#3498db', '#e74c3c'])

    # Customize the plot
    ax.set_xlabel('Model - Prompt Set', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Watts per Token', fontsize=12, fontweight='bold')
    ax.set_title('Average Energy Consumption (w_per_token) by Model and Prompt Set', 
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



