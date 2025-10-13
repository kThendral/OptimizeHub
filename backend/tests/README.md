# OptimizeHub Test Suite

This directory contains the comprehensive test suite for the OptimizeHub evolutionary algorithm SaaS platform.

## Directory Structure

```
tests/
├── README.md (this file)
│
├── test_algorithms/          # Algorithm-specific unit tests
│   ├── test_pso.py                    # PSO basic tests
│   ├── test_pso_algorithmic_correctness.py  # PSO correctness verification
│   ├── test_pso_edge_cases.py         # PSO edge case handling
│   ├── test_ga.py                     # GA basic tests
│   ├── test_ga_simple.py              # GA simple functionality
│   ├── test_ga_knapsack.py            # GA knapsack problem test
│   ├── test_de.py                     # DE basic tests
│   └── test_aco_validation.py         # ⭐ ACOR comprehensive validation
│
├── test_integration/         # Integration and performance tests
│   ├── test_complete_verification.py  # ⭐ Complete end-to-end verification
│   └── test_api_performance_comparison.py  # ⭐ Algorithm performance comparison
│
├── test_api.py               # Basic API tests
└── test_executor.py          # Executor service tests
```

---

## Key Test Files

### 🔥 Most Important Tests

#### 1. `test_integration/test_complete_verification.py`
**Purpose**: Complete end-to-end verification of all features

**What it tests**:
- ✅ All algorithms have characteristics metadata
- ✅ ACOR optimization through API
- ✅ Algorithm performance comparison (2D Sphere)
- ✅ Validates speed/accuracy ratings match actual performance

**How to run**:
```bash
cd backend
python3 tests/test_integration/test_complete_verification.py
```

**Expected output**:
- All 4 available algorithms should have characteristics
- ACOR should achieve machine precision (< 1e-6)
- Performance rankings for speed and accuracy

---

#### 2. `test_integration/test_api_performance_comparison.py`
**Purpose**: Comprehensive performance comparison of all algorithms

**What it tests**:
- 2D Sphere function (simple optimization)
- 5D Sphere function (medium complexity)
- 3D Rastrigin function (multi-modal challenge)

**How to run**:
```bash
cd backend
python3 tests/test_integration/test_api_performance_comparison.py
```

**Expected output**:
- Performance metrics for each algorithm on each test
- Speed and accuracy rankings
- Algorithm characteristics recommendations

---

#### 3. `test_algorithms/test_aco_validation.py`
**Purpose**: Comprehensive ACOR validation against platform requirements

**What it tests**:
- **Test 1**: Sphere 5D - Convergence to ~0, time < 1s
- **Test 2**: Rastrigin 5D - Solution < 10, time < 1s
- **Test 3**: Large-scale 50D - Time < 30s, 2.5x improvement
- **Test 4**: Tight bounds - Respects constraints
- **Test 5**: Maximization - Correct objective handling

**How to run**:
```bash
cd backend
python3 tests/test_algorithms/test_aco_validation.py
```

**Expected output**: All 5 tests should pass with ✅

---

## Test Categories

### Algorithm-Specific Tests (`test_algorithms/`)

These tests validate individual algorithm implementations:

- **PSO Tests**:
  - `test_pso.py` - Basic functionality
  - `test_pso_algorithmic_correctness.py` - Verifies PSO behavior matches algorithm specifications
  - `test_pso_edge_cases.py` - Edge cases and error handling

- **GA Tests**:
  - `test_ga.py` - Basic functionality
  - `test_ga_simple.py` - Simple optimization problems
  - `test_ga_knapsack.py` - Discrete optimization (knapsack problem)

- **DE Tests**:
  - `test_de.py` - Basic functionality

- **ACOR Tests**:
  - `test_aco_validation.py` - Comprehensive 5-benchmark validation suite

### Integration Tests (`test_integration/`)

These tests validate end-to-end functionality:

- **Complete Verification**: Tests all features together
- **Performance Comparison**: Benchmarks all algorithms against each other

---

## Running Tests

### Run Individual Test
```bash
cd backend
python3 tests/test_algorithms/test_aco_validation.py
```

### Run All Tests in a Directory
```bash
cd backend
python3 -m pytest tests/test_algorithms/
```

### Run Complete Verification
```bash
cd backend
python3 tests/test_integration/test_complete_verification.py
```

---

## Test Results Interpretation

### ACOR Validation Tests

**Sphere 5D Test**:
- ✅ Pass: Best fitness < 1e-4
- ✅ Pass: Average time < 1s
- Expected: ~0.07s with fitness near 0

**Rastrigin 5D Test**:
- ✅ Pass: Best fitness < 10
- ✅ Pass: Time < 1s
- Expected: ~0.07s with fitness < 5

**Large-scale 50D Test**:
- ✅ Pass: Time < 30s
- ✅ Pass: 2.5x improvement from initial to final
- Expected: ~0.7s with significant convergence

**Tight Bounds Test**:
- ✅ Pass: All dimensions respect bounds [0.0, 0.5]
- Expected: Solution within bounds

**Maximization Test**:
- ✅ Pass: Negative sphere converges to value > -1.0
- Expected: Correct handling of maximization objective

### Performance Comparison

**Expected Rankings**:

**Accuracy (2D Sphere)**:
1. ACOR: ~0.0 (machine precision) ⭐
2. PSO: ~0.00001-0.0001
3. GA: ~0.0001-0.001

**Speed (2D Sphere)**:
1. PSO: ~0.010s ⚡
2. GA: ~0.012s
3. ACOR: ~0.018s

---

## Algorithm Characteristics

All algorithms now have metadata exposed through the API:

| Algorithm | Speed | Accuracy | Speed Rank | Accuracy Rank |
|-----------|-------|----------|------------|---------------|
| **ACOR** | fast | excellent | 5/5 ★ | 5/5 ★ |
| **PSO** | fast | excellent | 4/5 ★ | 4/5 ★ |
| **GA** | fastest | good | 5/5 ★ | 3/5 ★ |
| **DE** | fast | very good | 4/5 ★ | 4/5 ★ |

---

## Adding New Tests

### For New Algorithms

1. Create `test_algorithms/test_{algorithm_name}.py`
2. Include basic functionality tests
3. Add comprehensive validation if needed (like `test_aco_validation.py`)
4. Update the performance comparison test to include the new algorithm

### For New Features

1. Add tests to appropriate directory
2. Update this README
3. Ensure tests are standalone (can be run individually)

---

## Test Maintenance

### Cleaned Up Tests

The following redundant/incomplete tests were removed during cleanup:

- ❌ `test_aco_simple.py` - Superseded by `test_aco_validation.py`
- ❌ `test_api_integration.py` - Superseded by `test_complete_verification.py`
- ❌ `test_characteristics_direct.py` - Debugging test, no longer needed
- ❌ `verify_api_characteristics.py` - Superseded by `test_complete_verification.py`
- ❌ `test_final_integration.py` - Superseded by `test_complete_verification.py`

---

## Troubleshooting

### Import Errors

Make sure you're running tests from the `backend/` directory:
```bash
cd backend
python3 tests/test_integration/test_complete_verification.py
```

### Path Issues

Tests use relative path resolution. Always run from the backend root directory.

### Missing Dependencies

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## Test Coverage

### Current Coverage:
- ✅ PSO: Comprehensive (basic, correctness, edge cases)
- ✅ GA: Good (basic, simple, knapsack)
- ✅ DE: Basic
- ✅ ACOR: Comprehensive (5-benchmark validation)
- ✅ API Integration: Complete end-to-end verification
- ✅ Performance Comparison: All algorithms benchmarked
- ✅ Characteristics: All algorithms have metadata

---

## Contributing

When adding new tests:
1. Follow existing test patterns
2. Use descriptive test names
3. Include docstrings explaining what's being tested
4. Add print statements for clear output
5. Update this README

---

**Last Updated**: 2025-10-13
**Test Suite Status**: ✅ All tests passing
