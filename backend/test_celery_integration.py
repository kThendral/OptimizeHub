#!/usr/bin/env python3
"""
Test script to verify Celery integration with Docker sandbox.
This tests the complete flow: API -> Celery -> Docker sandbox.
"""

import requests
import time
import sys

BASE_URL = "http://localhost:8000/api"

def test_celery_basic():
    """Test basic Celery functionality."""
    print("🧪 Testing basic Celery connection...")
    
    try:
        response = requests.post(f"{BASE_URL}/celery/test", timeout=5)
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            print(f"✅ Celery test started - Task ID: {task_id}")
            return task_id
        else:
            print(f"❌ Celery test failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Celery test error: {e}")
        return None

def test_async_optimization():
    """Test async optimization with simple sphere function."""
    print("\n🚀 Testing async optimization...")
    
    request_data = {
        "algorithm": "particle_swarm",
        "problem": {
            "fitness_function": "sphere",
            "dimensions": 2,
            "bounds": [[-5.0, 5.0], [-5.0, 5.0]],
            "objective": "minimize"
        },
        "swarm_size": 10,
        "max_iterations": 30,
        "w": 0.5,
        "c1": 1.5,
        "c2": 1.5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/optimize/async", json=request_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            print(f"✅ Async optimization started - Task ID: {task_id}")
            return task_id
        else:
            print(f"❌ Async optimization failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Async optimization error: {e}")
        return None

def monitor_task(task_id, max_wait=60):
    """Monitor task progress."""
    print(f"\n📊 Monitoring task {task_id}...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(f"{BASE_URL}/optimize/status/{task_id}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                state = data.get('state')
                status = data.get('status', 'Unknown')
                progress = data.get('progress', 0)
                
                print(f"📈 State: {state} | Progress: {progress}% | Status: {status}")
                
                if state == 'SUCCESS':
                    result = data.get('result', {})
                    print(f"✅ Task completed successfully!")
                    print(f"🎯 Best fitness: {result.get('best_fitness', 'N/A')}")
                    return True
                elif state == 'FAILURE':
                    error = data.get('error', 'Unknown error')
                    print(f"❌ Task failed: {error}")
                    return False
                elif state in ['REVOKED', 'CANCELLED']:
                    print(f"⚠️ Task was cancelled/revoked")
                    return False
                    
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error monitoring task: {e}")
            time.sleep(3)
    
    print(f"⏰ Task monitoring timed out after {max_wait}s")
    return False

def test_docker_sandbox():
    """Test Docker sandbox with custom fitness function."""
    print("\n🐳 Testing Docker sandbox with custom fitness...")
    
    # Test with malicious code (should be blocked)
    malicious_code = '''
def fitness(x):
    import os
    try:
        os.system('echo "Security breach!"')
    except:
        pass
    return sum(x**2)
'''
    
    try:
        files = {'file': ('malicious.py', malicious_code)}
        data = {
            'algorithm': 'particle_swarm',
            'dimensions': '2',
            'bounds': '[[-5,5],[-5,5]]',
            'swarm_size': '10',
            'max_iterations': '20'
        }
        
        response = requests.post(f"{BASE_URL}/optimize/custom", files=files, data=data, timeout=30)
        
        if response.status_code == 500:
            print("✅ Docker sandbox blocked malicious code (expected)")
            return True
        elif response.status_code == 200:
            print("⚠️ WARNING: Malicious code was not blocked!")
            return False
        else:
            print(f"❓ Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Docker sandbox test error: {e}")
        return False

def main():
    print("🛡️ OptimizeHub Celery + Docker Sandbox Integration Test")
    print("=" * 60)
    
    # Check if API is running
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code != 200:
            print("❌ API server not running. Start it with:")
            print("   cd backend && python -m uvicorn app.main:app --reload")
            sys.exit(1)
    except:
        print("❌ Cannot connect to API server on localhost:8000")
        sys.exit(1)
    
    print("✅ API server is running")
    
    # Test 1: Basic Celery
    task_id = test_celery_basic()
    if task_id:
        monitor_task(task_id, max_wait=45)
    
    # Test 2: Async optimization 
    task_id = test_async_optimization()
    if task_id:
        monitor_task(task_id, max_wait=60)
    
    # Test 3: Docker sandbox security
    test_docker_sandbox()
    
    print("\n" + "=" * 60)
    print("🎯 Test completed! Check the results above.")
    print("Expected results:")
    print("  ✅ Celery tasks should complete successfully")
    print("  ✅ Async optimization should find good solutions")
    print("  ✅ Docker sandbox should block malicious code")

if __name__ == "__main__":
    main()