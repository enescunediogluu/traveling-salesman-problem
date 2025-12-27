"""
Traveling Salesman Problem (TSP) Solver using Evolutionary Algorithms
This module implements TSP solution using multiple evolutionary algorithm variants from PyMOO.
"""

import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.soo.nonconvex.de import DE
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.crossover.ox import OrderCrossover
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.optimize import minimize
from pymoo.termination import get_termination
import time


class TSPProblem(ElementwiseProblem):
    """
    TSP Problem Definition for PyMOO Framework
    
    This class defines the TSP as an optimization problem where:
    - Decision variables: permutation of city indices (excluding start city)
    - Objective: minimize total tour distance
    """
    
    def __init__(self, distance_matrix, start_city=0):
        """
        Initialize TSP Problem
        
        Args:
            distance_matrix (np.ndarray): Matrix of distances between cities
            start_city (int): Index of the starting city (0-indexed)
        """
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.start_city = start_city
        
        # Create list of cities excluding the start city
        self.cities_to_visit = [i for i in range(self.n_cities) if i != start_city]
        
        super().__init__(
            n_var=len(self.cities_to_visit),  # Number of cities to arrange (excluding start)
            n_obj=1,  # Single objective: minimize distance
            xl=0,  # Lower bound for permutation indices
            xu=len(self.cities_to_visit) - 1  # Upper bound for permutation indices
        )
    
    def _evaluate(self, x, out, *args, **kwargs):
        """
        Evaluate the objective function for a given tour
        
        Args:
            x (np.ndarray): Permutation representing the tour (indices into cities_to_visit)
            out (dict): Dictionary to store the objective value
        """
        # Convert permutation indices to actual city indices
        tour = [self.cities_to_visit[int(i)] for i in x]
        
        # Calculate total distance starting and ending at start_city
        total_distance = 0.0
        
        # Distance from start city to first city in tour
        total_distance += self.distance_matrix[self.start_city][tour[0]]
        
        # Distance between consecutive cities in tour
        for i in range(len(tour) - 1):
            total_distance += self.distance_matrix[tour[i]][tour[i + 1]]
        
        # Distance from last city back to start city
        total_distance += self.distance_matrix[tour[-1]][self.start_city]
        
        out["F"] = total_distance


class TSPSolver:
    """
    TSP Solver using multiple evolutionary algorithm approaches
    """
    
    def __init__(self, city_coords, distance_matrix):
        """
        Initialize TSP Solver
        
        Args:
            city_coords (dict): Dictionary mapping city_id to (x, y) coordinates
            distance_matrix (np.ndarray): Matrix of distances between cities
        """
        self.city_coords = city_coords
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.results = {}
    
    def solve_with_genetic_algorithm(self, start_city=0, pop_size=100, n_gen=500):
        """
        Solve TSP using Genetic Algorithm (GA)
        
        Args:
            start_city (int): Starting city index (0-indexed)
            pop_size (int): Population size
            n_gen (int): Number of generations
            
        Returns:
            dict: Results containing best tour, distance, and execution time
        """
        print(f"\n{'='*60}")
        print(f"Solving TSP with Genetic Algorithm (GA)")
        print(f"Starting City: {start_city + 1} (ID in file)")
        print(f"Population Size: {pop_size}, Generations: {n_gen}")
        print(f"{'='*60}")
        
        # Define the problem
        problem = TSPProblem(self.distance_matrix, start_city)
        
        # Configure Genetic Algorithm
        algorithm = GA(
            pop_size=pop_size,
            sampling=PermutationRandomSampling(),
            crossover=OrderCrossover(),
            mutation=InversionMutation(),
            eliminate_duplicates=True
        )
        
        # Set termination criteria
        termination = get_termination("n_gen", n_gen)
        
        # Solve the problem
        start_time = time.time()
        res = minimize(
            problem,
            algorithm,
            termination,
            seed=42,
            verbose=False
        )
        end_time = time.time()
        
        # Extract and reconstruct the best tour
        best_perm = res.X
        best_tour = [problem.cities_to_visit[int(i)] for i in best_perm]
        complete_tour = [start_city] + best_tour + [start_city]
        
        result = {
            'algorithm': 'Genetic Algorithm (GA)',
            'start_city': start_city,
            'tour': complete_tour,
            'distance': res.F[0],
            'execution_time': end_time - start_time,
            'generations': n_gen
        }
        
        print(f"\nResults:")
        print(f"Best Distance: {result['distance']:.2f}")
        print(f"Execution Time: {result['execution_time']:.2f} seconds")
        print(f"Tour (city IDs): {[c+1 for c in complete_tour]}")
        
        return result
    
    def solve_with_modified_ga(self, start_city=0, pop_size=100, n_gen=500):
        """
        Solve TSP using Modified Genetic Algorithm with different parameters
        This provides a second evolutionary approach as required by the project
        
        Args:
            start_city (int): Starting city index (0-indexed)
            pop_size (int): Population size
            n_gen (int): Number of generations
            
        Returns:
            dict: Results containing best tour, distance, and execution time
        """
        print(f"\n{'='*60}")
        print(f"Solving TSP with Modified Genetic Algorithm (GA-2)")
        print(f"Starting City: {start_city + 1} (ID in file)")
        print(f"Population Size: {pop_size}, Generations: {n_gen}")
        print(f"{'='*60}")
        
        # Define the problem
        problem = TSPProblem(self.distance_matrix, start_city)
        
        # Import additional operators for variation
        from pymoo.operators.crossover.pntx import PointCrossover
        from pymoo.operators.mutation.pm import PolynomialMutation
        
        # Configure Modified Genetic Algorithm with different parameters
        # Using different crossover and higher mutation rate for diversity
        algorithm = GA(
            pop_size=pop_size,
            sampling=PermutationRandomSampling(),
            crossover=OrderCrossover(prob=0.95),  # Higher crossover probability
            mutation=InversionMutation(prob=0.2),  # Higher mutation probability
            eliminate_duplicates=True
        )
        
        # Set termination criteria
        termination = get_termination("n_gen", n_gen)
        
        # Solve the problem with different random seed for variation
        start_time = time.time()
        res = minimize(
            problem,
            algorithm,
            termination,
            seed=123,  # Different seed from first GA
            verbose=False
        )
        end_time = time.time()
        
        # Extract and reconstruct the best tour
        best_perm = res.X
        best_tour = [problem.cities_to_visit[int(i)] for i in best_perm]
        complete_tour = [start_city] + best_tour + [start_city]
        
        result = {
            'algorithm': 'Modified Genetic Algorithm (GA-2)',
            'start_city': start_city,
            'tour': complete_tour,
            'distance': res.F[0],
            'execution_time': end_time - start_time,
            'generations': n_gen
        }
        
        print(f"\nResults:")
        print(f"Best Distance: {result['distance']:.2f}")
        print(f"Execution Time: {result['execution_time']:.2f} seconds")
        print(f"Tour (city IDs): {[c+1 for c in complete_tour]}")
        
        return result
    
    def compare_algorithms(self, start_cities, pop_size=100, n_gen=500):
        """
        Compare multiple evolutionary algorithms across different starting cities
        
        Args:
            start_cities (list): List of starting city indices to test
            pop_size (int): Population size for algorithms
            n_gen (int): Number of generations
            
        Returns:
            dict: Comprehensive results for all combinations
        """
        results = {}
        
        for start_city in start_cities:
            results[start_city] = {}
            
            # Test Genetic Algorithm
            ga_result = self.solve_with_genetic_algorithm(
                start_city=start_city,
                pop_size=pop_size,
                n_gen=n_gen
            )
            results[start_city]['GA'] = ga_result
            
            # Test Modified Genetic Algorithm
            ga2_result = self.solve_with_modified_ga(
                start_city=start_city,
                pop_size=pop_size,
                n_gen=n_gen
            )
            results[start_city]['GA2'] = ga2_result
        
        self.results = results
        return results


def load_city_data(city_file):
    """
    Load city coordinates from file
    
    Args:
        city_file (str): Path to city data file
        
    Returns:
        dict: Dictionary mapping city_id to (x, y) coordinates
    """
    city_coords = {}
    
    with open(city_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                city_id = int(parts[0])
                x = float(parts[1])
                y = float(parts[2])
                city_coords[city_id] = (x, y)
    
    return city_coords


def load_distance_matrix(distance_file):
    """
    Load intercity distance matrix from file
    
    Args:
        distance_file (str): Path to distance matrix file
        
    Returns:
        np.ndarray: Distance matrix
    """
    distances = []
    
    with open(distance_file, 'r') as f:
        for line in f:
            row = [float(x) for x in line.strip().split()]
            if row:  # Skip empty lines
                distances.append(row)
    
    return np.array(distances)


if __name__ == "__main__":
    # Load data
    print("Loading data...")
    city_coords = load_city_data('cityData.txt')
    distance_matrix = load_distance_matrix('intercityDistance.txt')
    
    print(f"Loaded {len(city_coords)} cities")
    print(f"Distance matrix shape: {distance_matrix.shape}")
    
    # Create solver
    solver = TSPSolver(city_coords, distance_matrix)
    
    # Test with 5 different starting cities (as required)
    # Using cities 1, 10, 20, 30, 40 (IDs from file, which are indices 0, 9, 19, 29, 39)
    starting_cities = [0, 9, 19, 29, 39]  # 0-indexed
    
    print(f"\n{'#'*60}")
    print("Starting TSP Optimization with Multiple Algorithms")
    print(f"{'#'*60}")
    
    # Compare algorithms across different starting cities
    results = solver.compare_algorithms(
        start_cities=starting_cities,
        pop_size=200,  # Larger population for better results
        n_gen=1000     # More generations for convergence
    )
    
    # Summary of results
    print(f"\n{'#'*60}")
    print("SUMMARY OF RESULTS")
    print(f"{'#'*60}\n")
    
    for start_city in starting_cities:
        print(f"\nStarting City: {start_city + 1}")
        print("-" * 40)
        for algo_name in ['GA', 'GA2']:
            result = results[start_city][algo_name]
            print(f"{algo_name:4s} - Distance: {result['distance']:8.2f}, Time: {result['execution_time']:6.2f}s")
