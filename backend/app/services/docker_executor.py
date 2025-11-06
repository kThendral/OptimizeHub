"""
Docker executor service for running user code in isolated containers.
"""

import os
import json
import uuid
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DockerExecutor:
    """Manages execution of user code in Docker containers"""

    def __init__(
        self,
        image_name: str = "optimizehub-sandbox:latest",
        timeout: int = 30,
        memory_limit: str = "512m",
        cpu_limit: str = "2.0"
    ):
        """
        Initialize Docker executor.

        Args:
            image_name: Name of the Docker image to use
            timeout: Execution timeout in seconds
            memory_limit: Memory limit (e.g., "512m", "1g")
            cpu_limit: CPU limit (e.g., "1.0", "2.0")
        """
        self.image_name = image_name
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpu_limit = cpu_limit
        self.temp_dir = Path(tempfile.gettempdir()) / "optimizehub_executions"
        self.temp_dir.mkdir(exist_ok=True)

    def execute_custom_fitness(
        self,
        fitness_code: str,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute custom fitness function in Docker container.

        Args:
            fitness_code: Python code containing the fitness function
            config: Configuration dictionary with algorithm and parameters

        Returns:
            Dictionary with execution results or error information
        """
        execution_id = str(uuid.uuid4())
        exec_dir = self.temp_dir / execution_id

        try:
            # Create execution directory
            exec_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created execution directory: {exec_dir}")

            # Write fitness function to file
            fitness_file = exec_dir / "fitness.py"
            fitness_file.write_text(fitness_code)
            logger.info(f"Wrote fitness function to {fitness_file}")

            # Write config to JSON file
            config_file = exec_dir / "config.json"
            config_file.write_text(json.dumps(config))
            logger.info(f"Wrote config to {config_file}")

            # Check if Docker image exists
            self._ensure_image_exists()

            # Run Docker container
            result = self._run_container(exec_dir, execution_id)

            return result

        except Exception as e:
            logger.error(f"Execution failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'error_type': 'execution_error'
            }

        finally:
            # Cleanup execution directory
            try:
                if exec_dir.exists():
                    shutil.rmtree(exec_dir)
                    logger.info(f"Cleaned up execution directory: {exec_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {exec_dir}: {str(e)}")

    def _ensure_image_exists(self):
        """Check if Docker image exists, build if not"""
        try:
            # Check if image exists
            result = subprocess.run(
                ["docker", "images", "-q", self.image_name],
                capture_output=True,
                text=True,
                check=True
            )

            if not result.stdout.strip():
                logger.info(f"Docker image {self.image_name} not found, building...")
                self._build_image()
            else:
                logger.info(f"Docker image {self.image_name} found")

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to check Docker image: {e.stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "Docker is not installed or not in PATH. "
                "Please install Docker to use custom fitness functions."
            )

    def _build_image(self):
        """Build Docker image from Dockerfile"""
        try:
            # Get path to Dockerfile
            backend_dir = Path(__file__).parent.parent.parent
            dockerfile_path = backend_dir / "docker" / "Dockerfile.sandbox"

            if not dockerfile_path.exists():
                raise RuntimeError(f"Dockerfile not found at {dockerfile_path}")

            logger.info(f"Building Docker image from {dockerfile_path}")

            # Build image
            result = subprocess.run(
                [
                    "docker", "build",
                    "-t", self.image_name,
                    "-f", str(dockerfile_path),
                    str(backend_dir / "docker")
                ],
                capture_output=True,
                text=True,
                check=True
            )

            logger.info(f"Docker image built successfully: {result.stdout}")

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to build Docker image: {e.stderr}")

    def _run_container(self, exec_dir: Path, execution_id: str) -> Dict[str, Any]:
        """
        Run Docker container with user code.

        Args:
            exec_dir: Directory containing fitness.py and config.json
            execution_id: Unique execution ID

        Returns:
            Dictionary with execution results
        """
        try:
            # Build Docker command
            docker_cmd = [
                "docker", "run",
                "--rm",  # Remove container after execution
                "--network", "none",  # No network access
                "--memory", self.memory_limit,  # Memory limit
                "--cpus", self.cpu_limit,  # CPU limit
                "--read-only",  # Read-only filesystem
                "--tmpfs", "/tmp",  # Writable temp directory
                "--user", "1000:1000",  # Non-root user
                "-v", f"{exec_dir}:/workspace:ro",  # Mount execution dir as read-only
                "-w", "/workspace",  # Set working directory
                self.image_name,
                "python", "/runner.py", "fitness.py", "config.json"
            ]

            logger.info(f"Running Docker command: {' '.join(docker_cmd)}")

            # Run container with timeout
            result = subprocess.run(
                docker_cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            # Parse output
            if result.returncode == 0:
                try:
                    output = json.loads(result.stdout)
                    logger.info(f"Execution successful: {output.get('success', False)}")
                    return output
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse output: {result.stdout}")
                    return {
                        'success': False,
                        'error': f"Failed to parse execution output: {str(e)}",
                        'error_type': 'parse_error',
                        'raw_output': result.stdout
                    }
            else:
                # Container exited with error
                logger.error(f"Container failed with return code {result.returncode}")
                logger.error(f"stdout: {result.stdout}")
                logger.error(f"stderr: {result.stderr}")

                # Try to parse error output
                try:
                    error_output = json.loads(result.stdout)
                    return error_output
                except json.JSONDecodeError:
                    return {
                        'success': False,
                        'error': result.stderr or result.stdout or "Container execution failed",
                        'error_type': 'container_error'
                    }

        except subprocess.TimeoutExpired:
            logger.error(f"Execution timed out after {self.timeout} seconds")
            return {
                'success': False,
                'error': f"Execution exceeded {self.timeout} seconds timeout. "
                        f"Try reducing iterations or problem complexity.",
                'error_type': 'timeout'
            }
        except Exception as e:
            logger.error(f"Container execution failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'error_type': 'execution_error'
            }

    def cleanup_all(self):
        """Cleanup all execution directories"""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                self.temp_dir.mkdir(exist_ok=True)
                logger.info("Cleaned up all execution directories")
        except Exception as e:
            logger.warning(f"Failed to cleanup all directories: {str(e)}")


# Singleton instance
_executor_instance: Optional[DockerExecutor] = None


def get_docker_executor() -> DockerExecutor:
    """Get or create singleton DockerExecutor instance"""
    global _executor_instance
    if _executor_instance is None:
        _executor_instance = DockerExecutor()
    return _executor_instance


# Example usage
if __name__ == "__main__":
    # Test the executor
    executor = DockerExecutor()

    # Test fitness function
    test_code = """
import numpy as np

def fitness(x):
    return np.sum(x**2)
"""

    # Test config
    test_config = {
        "algorithm": "PSO",
        "parameters": {
            "num_particles": 20,
            "max_iterations": 50,
            "w": 0.7,
            "c1": 1.5,
            "c2": 1.5
        },
        "problem": {
            "dimensions": 5,
            "lower_bound": -5.0,
            "upper_bound": 5.0
        }
    }

    print("Testing Docker executor...")
    result = executor.execute_custom_fitness(test_code, test_config)
    print(json.dumps(result, indent=2))
