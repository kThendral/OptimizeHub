from abc import ABC, abstractmethod
from typing import Any, Dict, List


class OptimizationAlgorithm(ABC):
    """
    Base class for all optimization algorithms.
    Each algorithm must inherit and implement the abstract methods.
    """

    def __init__(self, problem: Dict[str, Any], params: Dict[str, Any]):
        """
        problem: Dict with problem definition (variables, constraints, fitness function, etc.)
        params: Dict with algorithm-specific parameters (population size, iterations, etc.)
        """
        self.problem = problem
        self.params = params
        self.best_solution = None
        self.convergence_curve: List[float] = []

    @abstractmethod
    def initialize(self):
        """Setup initial population/particles/solutions."""
        pass

    @abstractmethod
    def optimize(self):
        """
        Core optimization loop.
        Should update self.best_solution and self.convergence_curve.
        """
        pass

    def get_results(self) -> Dict[str, Any]:
        """
        Return a standard result format so all algorithms are comparable.
        """
        return {
            "algorithm": self.__class__.__name__,
            "best_solution": self.best_solution,
            "convergence_curve": self.convergence_curve,
            "params": self.params
        }
