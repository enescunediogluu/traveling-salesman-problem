"""
Main Execution Script for TSP Project
This script runs the complete TSP analysis with multiple algorithms and starting cities,
and generates comprehensive visualizations and reports.
"""

import sys
import os

# Import our custom modules
from tsp_solver import TSPSolver, load_city_data, load_distance_matrix
from visualize_results import (
    plot_tour, 
    plot_comparison, 
    plot_performance_comparison,
    create_comprehensive_report,
    print_results_table
)


def main():
    """
    Main execution function for TSP project
    """
    print("=" * 80)
    print(" " * 20 + "TRAVELING SALESMAN PROBLEM SOLVER")
    print(" " * 15 + "Using Evolutionary Algorithms with PyMOO")
    print("=" * 80)
    
    # Configuration parameters
    POP_SIZE = 200      # Population size for evolutionary algorithms
    N_GEN = 1000        # Number of generations
    
    # Starting cities to test (as specified in requirements: 5 different starting cities)
    # Using city IDs: 1, 10, 20, 30, 40 (which are indices 0, 9, 19, 29, 39)
    STARTING_CITIES = [0, 9, 19, 29, 39]
    
    print(f"\nConfiguration:")
    print(f"  - Population Size: {POP_SIZE}")
    print(f"  - Number of Generations: {N_GEN}")
    print(f"  - Starting Cities (IDs): {[sc+1 for sc in STARTING_CITIES]}")
    print(f"  - Algorithms: Genetic Algorithm (GA), Modified Genetic Algorithm (GA-2)")
    
    # Step 1: Load data
    print(f"\n{'='*80}")
    print("STEP 1: Loading Data")
    print(f"{'='*80}")
    
    try:
        city_coords = load_city_data('cityData.txt')
        distance_matrix = load_distance_matrix('intercityDistance.txt')
        print(f"✓ Successfully loaded {len(city_coords)} cities")
        print(f"✓ Distance matrix shape: {distance_matrix.shape}")
    except FileNotFoundError as e:
        print(f"✗ Error: Could not find data files. Please ensure cityData.txt and")
        print(f"  intercityDistance.txt are in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        sys.exit(1)
    
    # Step 2: Create solver and run optimization
    print(f"\n{'='*80}")
    print("STEP 2: Running TSP Optimization")
    print(f"{'='*80}")
    
    solver = TSPSolver(city_coords, distance_matrix)
    
    try:
        results = solver.compare_algorithms(
            start_cities=STARTING_CITIES,
            pop_size=POP_SIZE,
            n_gen=N_GEN
        )
        print(f"\n✓ Successfully completed all optimization runs")
    except Exception as e:
        print(f"✗ Error during optimization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 3: Display results
    print(f"\n{'='*80}")
    print("STEP 3: Results Summary")
    print(f"{'='*80}")
    
    print_results_table(results)
    
    # Step 4: Generate visualizations
    print(f"\n{'='*80}")
    print("STEP 4: Generating Visualizations")
    print(f"{'='*80}")
    
    try:
        # Create results directory
        output_dir = 'results'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✓ Created '{output_dir}' directory")
        
        # Generate all visualizations
        create_comprehensive_report(results, city_coords, output_dir=output_dir)
        
        print(f"\n✓ All visualizations generated successfully!")
        print(f"  Check the '{output_dir}' directory for output images.")
    except Exception as e:
        print(f"✗ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 5: Generate text report
    print(f"\n{'='*80}")
    print("STEP 5: Generating Text Report")
    print(f"{'='*80}")
    
    try:
        report_file = f"{output_dir}/results_report.txt"
        with open(report_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("TRAVELING SALESMAN PROBLEM - RESULTS REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write("CONFIGURATION:\n")
            f.write(f"  Population Size: {POP_SIZE}\n")
            f.write(f"  Number of Generations: {N_GEN}\n")
            f.write(f"  Starting Cities: {[sc+1 for sc in STARTING_CITIES]}\n")
            f.write(f"  Algorithms: GA (Genetic Algorithm), GA2 (Modified Genetic Algorithm)\n\n")
            
            f.write("="*80 + "\n")
            f.write("DETAILED RESULTS\n")
            f.write("="*80 + "\n\n")
            
            for start_city in sorted(results.keys()):
                f.write(f"\n{'='*60}\n")
                f.write(f"Starting City: {start_city+1}\n")
                f.write(f"{'='*60}\n\n")
                
                for algo in ['GA', 'GA2']:
                    result = results[start_city][algo]
                    f.write(f"{result['algorithm']}:\n")
                    f.write(f"  Total Distance: {result['distance']:.2f} units\n")
                    f.write(f"  Execution Time: {result['execution_time']:.2f} seconds\n")
                    f.write(f"  Number of Generations: {result['generations']}\n")
                    f.write(f"  Tour (City IDs): {' -> '.join([str(c+1) for c in result['tour']])}\n")
                    f.write("\n")
            
            # Find and report best solution
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
                f.write("\n" + "="*80 + "\n")
                f.write("BEST OVERALL SOLUTION\n")
                f.write("="*80 + "\n\n")
                f.write(f"Algorithm: {algo}\n")
                f.write(f"Starting City: {start+1}\n")
                f.write(f"Total Distance: {result['distance']:.2f} units\n")
                f.write(f"Execution Time: {result['execution_time']:.2f} seconds\n")
                f.write(f"Complete Tour: {' -> '.join([str(c+1) for c in result['tour']])}\n")
        
        print(f"✓ Text report saved to '{report_file}'")
    except Exception as e:
        print(f"✗ Error generating text report: {e}")
    
    # Final summary
    print(f"\n{'='*80}")
    print("PROJECT EXECUTION COMPLETED SUCCESSFULLY!")
    print(f"{'='*80}")
    print(f"\nAll results have been saved to the '{output_dir}' directory:")
    print(f"  - Individual tour visualizations for each algorithm and starting city")
    print(f"  - Comparison grid showing all results")
    print(f"  - Performance comparison charts")
    print(f"  - Detailed text report")
    print(f"\nYou can now use these results for your project report and video demonstration.")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
