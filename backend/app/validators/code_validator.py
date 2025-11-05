"""
Security validator for user-uploaded Python code.
Uses AST (Abstract Syntax Tree) analysis to detect forbidden operations.
"""

import ast
from typing import Tuple, List, Set


class SecurityValidator:
    """Validates Python code for security violations"""

    # Forbidden built-in functions
    FORBIDDEN_BUILTINS = {
        'eval', 'exec', 'compile', '__import__',
        'open', 'input', 'raw_input',
        'file', 'execfile', 'reload',
        'breakpoint', 'memoryview', 'bytearray'
    }

    # Allowed imports only
    ALLOWED_IMPORTS = {'math', 'numpy', 'np'}

    # Forbidden modules (even if imported)
    FORBIDDEN_MODULES = {
        'os', 'sys', 'subprocess', 'socket', 'urllib', 'urllib2', 'urllib3',
        'http', 'httplib', 'ftplib', 'telnetlib', 'smtplib',
        'pickle', 'shelve', 'marshal', 'imp', 'importlib',
        'ctypes', 'cffi', 'pty', 'tty', 'termios',
        'multiprocessing', 'threading', 'asyncio',
        'requests', 'flask', 'django', 'tornado',
        '__builtin__', '__builtins__', 'builtins'
    }

    # Forbidden attribute access patterns
    FORBIDDEN_ATTRIBUTES = {
        '__code__', '__globals__', '__dict__', '__class__',
        '__bases__', '__subclasses__', '__mro__', '__loader__',
        '__spec__', '__path__', '__file__', '__name__',
        '__builtins__', '__import__'
    }

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, code: str) -> Tuple[bool, str]:
        """
        Validate Python code for security violations.

        Args:
            code: Python source code as string

        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if code is safe, False otherwise
            - error_message: Detailed error message if invalid, empty string if valid
        """
        self.errors = []
        self.warnings = []

        # Check if code is empty
        if not code.strip():
            return False, "Code cannot be empty"

        # Try to parse the code
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e.msg} at line {e.lineno}"
        except Exception as e:
            return False, f"Failed to parse code: {str(e)}"

        # Run security checks
        self._check_imports(tree)
        self._check_function_calls(tree)
        self._check_attribute_access(tree)
        self._check_forbidden_operations(tree)
        self._check_fitness_function(tree)

        # Return results
        if self.errors:
            return False, " | ".join(self.errors)

        return True, ""

    def _check_imports(self, tree: ast.AST):
        """Check for forbidden imports"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    if module_name in self.FORBIDDEN_MODULES:
                        self.errors.append(
                            f"Forbidden import: '{alias.name}'. Only 'math' and 'numpy' are allowed."
                        )
                    elif module_name not in self.ALLOWED_IMPORTS:
                        self.errors.append(
                            f"Import '{alias.name}' not allowed. Only 'math' and 'numpy' are permitted."
                        )

            elif isinstance(node, ast.ImportFrom):
                module_name = node.module.split('.')[0] if node.module else ''
                if module_name in self.FORBIDDEN_MODULES:
                    self.errors.append(
                        f"Forbidden import from '{node.module}'. Only 'math' and 'numpy' are allowed."
                    )
                elif module_name and module_name not in self.ALLOWED_IMPORTS:
                    self.errors.append(
                        f"Import from '{node.module}' not allowed. Only 'math' and 'numpy' are permitted."
                    )

    def _check_function_calls(self, tree: ast.AST):
        """Check for forbidden function calls"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = None

                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name in self.FORBIDDEN_BUILTINS:
                    self.errors.append(
                        f"Forbidden function call: '{func_name}()'. "
                        f"This function is not allowed for security reasons."
                    )

    def _check_attribute_access(self, tree: ast.AST):
        """Check for forbidden attribute access (dunder methods)"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                attr_name = node.attr
                if attr_name in self.FORBIDDEN_ATTRIBUTES:
                    self.errors.append(
                        f"Forbidden attribute access: '{attr_name}'. "
                        f"Special attributes are not allowed."
                    )

    def _check_forbidden_operations(self, tree: ast.AST):
        """Check for other forbidden operations"""
        for node in ast.walk(tree):
            # Check for file operations (with statement often used for files)
            if isinstance(node, ast.With):
                self.errors.append(
                    "File operations (with statement) are not allowed."
                )

            # Check for try/except importing (often used to detect environment)
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if handler.type and isinstance(handler.type, ast.Name):
                        if handler.type.id == 'ImportError':
                            self.warnings.append(
                                "Import error handling detected - may be attempting environment detection"
                            )

            # Check for lambda (can be used for obfuscation)
            if isinstance(node, ast.Lambda):
                self.warnings.append(
                    "Lambda functions detected - ensure they don't contain malicious code"
                )

            # Check for list/dict comprehensions with suspicious patterns
            if isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                for generator in node.generators:
                    if isinstance(generator.iter, ast.Call):
                        if isinstance(generator.iter.func, ast.Name):
                            if generator.iter.func.id in self.FORBIDDEN_BUILTINS:
                                self.errors.append(
                                    f"Forbidden function in comprehension: {generator.iter.func.id}"
                                )

    def _check_fitness_function(self, tree: ast.AST):
        """Verify that a 'fitness' function exists and has correct signature"""
        fitness_found = False
        fitness_params_correct = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name == 'fitness':
                    fitness_found = True

                    # Check function signature
                    if len(node.args.args) == 1:
                        fitness_params_correct = True
                    else:
                        self.errors.append(
                            "Fitness function must accept exactly one parameter (e.g., 'def fitness(x):')."
                        )

        if not fitness_found:
            self.errors.append(
                "No 'fitness' function found. Your code must define a function named 'fitness'."
            )
        elif not fitness_params_correct:
            # Error already added above
            pass


def validate_fitness_code(code: str) -> Tuple[bool, str]:
    """
    Convenience function to validate fitness function code.

    Args:
        code: Python source code as string

    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = SecurityValidator()
    return validator.validate(code)


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_cases = [
        # Valid code
        ("""
import numpy as np

def fitness(x):
    return np.sum(x**2)
""", True),

        # Valid with math
        ("""
import math

def fitness(x):
    return sum(x_i**2 for x_i in x)
""", True),

        # Invalid - file operation
        ("""
def fitness(x):
    with open('file.txt', 'r') as f:
        data = f.read()
    return sum(x)
""", False),

        # Invalid - forbidden import
        ("""
import os

def fitness(x):
    return sum(x)
""", False),

        # Invalid - eval
        ("""
def fitness(x):
    return eval('sum(x)')
""", False),

        # Invalid - no fitness function
        ("""
def my_function(x):
    return sum(x)
""", False),

        # Invalid - wrong signature
        ("""
def fitness(x, y):
    return x + y
""", False),
    ]

    print("Running validation tests...\n")
    for i, (code, expected_valid) in enumerate(test_cases, 1):
        is_valid, error_msg = validate_fitness_code(code)
        status = "PASS" if is_valid == expected_valid else "FAIL"
        print(f"Test {i}: {status}")
        if not is_valid:
            print(f"  Error: {error_msg}")
        print()
