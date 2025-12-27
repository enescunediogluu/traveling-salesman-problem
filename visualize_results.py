"""
Visualization Module for TSP Results
This module provides functions to visualize TSP tours and compare results.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
import matplotlib.patches as mpatches


def plot_tour(city_coords, tour, title="TSP Tour", save_path=None, show_arrows=True):
    """
    Plot a single TSP tour on a 2D map
    
    Args:
        city_coords (dict): Dictionary mapping city_id to (x, y) coordinates
        tour (list): List of city indices representing the tour
        title (str): Plot title
        save_path (str): Path to save the figure (optional)
        show_arrows (bool): Whether to show direction arrows
    """
    plt.figure(figsize=(14, 10))
    
    # Extract coordinates for the tour
    x_coords = []
    y_coords = []
    
    for city_idx in tour:
        city_id = city_idx + 1  # Convert 0-indexed to 1-indexed
        x, y = city_coords[city_id]
        x_coords.append(x)
        y_coords.append(y)
    
    # Plot all cities as points
    all_x = [coords[0] for coords in city_coords.values()]
    all_y = [coords[1] for coords in city_coords.values()]
    plt.scatter(all_x, all_y, c='lightgray', s=100, zorder=1, alpha=0.5, label='All Cities')
    
    # Plot the tour path
    plt.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.6, zorder=2)
    
    # Highlight tour cities
    plt.scatter(x_coords[1:-1], y_coords[1:-1], c='blue', s=150, zorder=3, 
                marker='o', edgecolors='black', linewidths=1, label='Visited Cities')
    
    # Highlight start/end city (they are the same)
    plt.scatter(x_coords[0], y_coords[0], c='red', s=300, zorder=4, 
                marker='*', edgecolors='black', linewidths=2, label=f'Start/End City {tour[0]+1}')
    
    # Add arrows to show direction
    if show_arrows:
        for i in range(len(x_coords) - 1):
            dx = x_coords[i + 1] - x_coords[i]
            dy = y_coords[i + 1] - y_coords[i]
            
            # Place arrow at midpoint
            mid_x = x_coords[i] + 0.4 * dx
            mid_y = y_coords[i] + 0.4 * dy
            
            plt.arrow(mid_x, mid_y, dx * 0.1, dy * 0.1,
                     head_width=2, head_length=2, fc='darkblue', ec='darkblue',
                     alpha=0.7, zorder=3, length_includes_head=True)
    
    # Add city labels
    for i, city_idx in enumerate(tour[:-1]):  # Exclude the last (duplicate start city)
        city_id = city_idx + 1
        x, y = city_coords[city_id]
        plt.annotate(str(city_id), (x, y), xytext=(5, 5), 
                    textcoords='offset points', fontsize=8,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    plt.xlabel('X Coordinate', fontsize=12)
    plt.ylabel('Y Coordinate', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(loc='best', fontsize=10)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")
    
    plt.show()


def plot_comparison(results, city_coords, save_path=None):
    """
    Create a comprehensive comparison plot for all results
    
    Args:
        results (dict): Dictionary containing results for all algorithms and starting cities
        city_coords (dict): Dictionary mapping city_id to (x, y) coordinates
        save_path (str): Path to save the figure (optional)
    """
    start_cities = list(results.keys())
    algorithms = ['GA', 'GA2']
    
    n_starts = len(start_cities)
    n_algos = len(algorithms)
    
    fig, axes = plt.subplots(n_starts, n_algos, figsize=(16, 4 * n_starts))
    
    if n_starts == 1:
        axes = axes.reshape(1, -1)
    
    for i, start_city in enumerate(start_cities):
        for j, algo in enumerate(algorithms):
            ax = axes[i, j]
            
            result = results[start_city][algo]
            tour = result['tour']
            distance = result['distance']
            exec_time = result['execution_time']
            
            # Extract coordinates for the tour
            x_coords = []
            y_coords = []
            
            for city_idx in tour:
                city_id = city_idx + 1
                x, y = city_coords[city_id]
                x_coords.append(x)
                y_coords.append(y)
            
            # Plot tour
            ax.plot(x_coords, y_coords, 'b-', linewidth=1.5, alpha=0.6)
            ax.scatter(x_coords[1:-1], y_coords[1:-1], c='blue', s=50, zorder=3)
            ax.scatter(x_coords[0], y_coords[0], c='red', s=200, marker='*', 
                      zorder=4, edgecolors='black', linewidths=1)
            
            # Set title with results
            ax.set_title(f'{algo} - Start City {start_city+1}\n' + 
                        f'Distance: {distance:.2f}, Time: {exec_time:.2f}s',
                        fontsize=10, fontweight='bold')
            ax.set_xlabel('X Coordinate')
            ax.set_ylabel('Y Coordinate')
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved comparison plot to {save_path}")
    
    plt.show()


def plot_performance_comparison(results, save_path=None):
    """
    Create bar charts comparing algorithm performance
    
    Args:
        results (dict): Dictionary containing results for all algorithms and starting cities
        save_path (str): Path to save the figure (optional)
    """
    start_cities = list(results.keys())
    algorithms = ['GA', 'GA2']
    
    # Extract data for plotting
    distances = {algo: [] for algo in algorithms}
    times = {algo: [] for algo in algorithms}
    
    for start_city in start_cities:
        for algo in algorithms:
            result = results[start_city][algo]
            distances[algo].append(result['distance'])
            times[algo].append(result['execution_time'])
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot distances
    x = np.arange(len(start_cities))
    width = 0.35
    
    for i, algo in enumerate(algorithms):
        offset = width * (i - 0.5)
        ax1.bar(x + offset, distances[algo], width, label=algo, alpha=0.8)
    
    ax1.set_xlabel('Starting City', fontsize=12)
    ax1.set_ylabel('Total Distance', fontsize=12)
    ax1.set_title('Distance Comparison Across Algorithms', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'City {sc+1}' for sc in start_cities])
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Plot execution times
    for i, algo in enumerate(algorithms):
        offset = width * (i - 0.5)
        ax2.bar(x + offset, times[algo], width, label=algo, alpha=0.8)
    
    ax2.set_xlabel('Starting City', fontsize=12)
    ax2.set_ylabel('Execution Time (seconds)', fontsize=12)
    ax2.set_title('Execution Time Comparison', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'City {sc+1}' for sc in start_cities])
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved performance comparison to {save_path}")
    
    plt.show()


def create_comprehensive_report(results, city_coords, output_dir='results'):
    """
    Create a comprehensive visual report with all results
    
    Args:
        results (dict): Dictionary containing results for all algorithms and starting cities
        city_coords (dict): Dictionary mapping city_id to (x, y) coordinates
        output_dir (str): Directory to save result images
    """
    import os
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"\n{'='*60}")
    print("Generating Comprehensive Visual Report")
    print(f"{'='*60}\n")
    
    # 1. Plot individual tours for each combination
    for start_city in results.keys():
        for algo in ['GA', 'GA2']:
            result = results[start_city][algo]
            tour = result['tour']
            distance = result['distance']
            exec_time = result['execution_time']
            
            title = (f"{result['algorithm']} - Starting from City {start_city+1}\n"
                    f"Total Distance: {distance:.2f} units, "
                    f"Execution Time: {exec_time:.2f}s")
            
            filename = f"{output_dir}/tour_{algo}_start{start_city+1}.png"
            plot_tour(city_coords, tour, title=title, save_path=filename, show_arrows=True)
    
    # 2. Create comparison grid
    print("\nGenerating comparison grid...")
    comparison_file = f"{output_dir}/comparison_all.png"
    plot_comparison(results, city_coords, save_path=comparison_file)
    
    # 3. Create performance comparison
    print("\nGenerating performance comparison...")
    performance_file = f"{output_dir}/performance_comparison.png"
    plot_performance_comparison(results, save_path=performance_file)
    
    print(f"\n{'='*60}")
    print(f"All visualizations saved to '{output_dir}/' directory")
    print(f"{'='*60}\n")


def print_results_table(results):
    """
    Print a formatted table of results
    
    Args:
        results (dict): Dictionary containing results for all algorithms and starting cities
    """
    print(f"\n{'='*80}")
    print("DETAILED RESULTS TABLE")
    print(f"{'='*80}\n")
    
    print(f"{'Start City':<12} {'Algorithm':<8} {'Distance':<12} {'Time (s)':<12} {'Best Tour'}")
    print("-" * 80)
    
    for start_city in sorted(results.keys()):
        for algo in ['GA', 'GA2']:
            result = results[start_city][algo]
            tour_str = ' -> '.join([str(c+1) for c in result['tour'][:6]]) + '...'
            
            print(f"{start_city+1:<12} {algo:<8} {result['distance']:<12.2f} "
                  f"{result['execution_time']:<12.2f} {tour_str}")
    
    print("=" * 80)
    
    # Find best overall result
    best_distance = float('inf')
    best_config = None
    
    for start_city in results.keys():
        for algo in ['GA', 'GA2']:
            result = results[start_city][algo]
            if result['distance'] < best_distance:
                best_distance = result['distance']
                best_config = (start_city, algo, result)
    
    if best_config:
        start, algo, result = best_config
        print(f"\n🏆 BEST RESULT:")
        print(f"   Algorithm: {algo}")
        print(f"   Starting City: {start+1}")
        print(f"   Distance: {result['distance']:.2f}")
        print(f"   Execution Time: {result['execution_time']:.2f}s")
        print(f"   Complete Tour: {' -> '.join([str(c+1) for c in result['tour']])}")
        print(f"\n{'='*80}\n")


if __name__ == "__main__":
    # This can be used to test visualization with sample data
    print("Visualization module loaded successfully.")
    print("Import this module in tsp_solver.py to visualize results.")
