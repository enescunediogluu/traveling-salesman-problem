"""
Quick Test Script for TSP Project
This script runs a faster test with reduced parameters to verify the implementation.
"""

import sys
import os

from tsp_solver import TSPSolver, load_city_data, load_distance_matrix
from visualize_results import plot_tour, print_results_table

def quick_test():
    """
    Quick test with reduced parameters
    """
    print("=" * 60)
    print(" " * 10 + "TSP QUICK TEST")
    print("=" * 60)
    
    # Reduced parameters for quick testing
    POP_SIZE = 50       # Smaller population
    N_GEN = 100         # Fewer generations
    STARTING_CITIES = [0, 19]  # Test with just 2 cities
    
    print(f"\nQuick Test Configuration:")
    print(f"  - Population Size: {POP_SIZE}")
    print(f"  - Number of Generations: {N_GEN}")
    print(f"  - Starting Cities (IDs): {[sc+1 for sc in STARTING_CITIES]}")
    
    # Load data
    print(f"\nLoading data...")
    city_coords = load_city_data('cityData.txt')
    distance_matrix = load_distance_matrix('intercityDistance.txt')
    print(f"✓ Loaded {len(city_coords)} cities")
    
    # Create solver
    solver = TSPSolver(city_coords, distance_matrix)
    
    # Run optimization
    print(f"\nRunning optimization...")
    results = solver.compare_algorithms(
        start_cities=STARTING_CITIES,
        pop_size=POP_SIZE,
        n_gen=N_GEN
    )
    
    # Display results
    print_results_table(results)
    
    # Plot one example
    print(f"\nGenerating sample visualization...")
    start_city = STARTING_CITIES[0]
    ga_result = results[start_city]['GA']
    
    title = f"GA - Starting from City {start_city+1}\nDistance: {ga_result['distance']:.2f}"
    plot_tour(city_coords, ga_result['tour'], title=title, save_path='test_tour.png')
    
    print(f"\n✓ Quick test completed successfully!")
    print(f"  Sample visualization saved to 'test_tour.png'")
    print(f"  Both algorithms (GA and GA-2) tested successfully")

if __name__ == "__main__":
    quick_test()
