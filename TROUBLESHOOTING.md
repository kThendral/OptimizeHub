# Troubleshooting "Failed to Fetch" Error

## Current Status
- ✅ Backend running on port 8000 (confirmed via curl)
- ✅ Frontend running on port 5173
- ✅ CORS configured for localhost:5173
- ❌ Frontend can't fetch from backend
- ❌ YAML parser had bug (FIXED)

## Quick Checks

### 1. Open Browser Console (F12)
Look for the actual error message. It will show one of these:

**CORS Error:**
```
Access to fetch at 'http://localhost:8000/api/algorithms' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**Network Error:**
```
Failed to fetch
TypeError: Failed to fetch
```

**Connection Refused:**
```
net::ERR_CONNECTION_REFUSED
```

### 2. Check What URL You're Using

Are you accessing frontend via:
- ✅ `http://localhost:5173` - Should work
- ❌ `http://127.0.0.1:5173` - Might cause CORS issue (different origin)
- ❌ `http://192.168.x.x:5173` - Definitely won't work (not in CORS list)

### 3. Verify Backend is Actually Running

In PowerShell:
```powershell
curl http://localhost:8000/api/algorithms
```

Expected response:
```json
{
  "algorithms": [
    {"name": "particle_swarm", "status": "available", ...},
    {"name": "genetic_algorithm", "status": "available", ...}
  ]
}
```

## Solutions

### Solution 1: Access Frontend via Correct URL
**USE:** `http://localhost:5173`  
**NOT:** `http://127.0.0.1:5173` or your IP address

### Solution 2: Add Your Current Origin to CORS

If you're using `127.0.0.1:5173`, we already have it in CORS config (check backend/app/main.py lines 67-68).

If you're using a different URL, add it to backend CORS:

```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # Add your URL here if different
    ],
    # ...
)
```

### Solution 3: Restart Backend After Changes
If you modified main.py, restart the backend:
```powershell
# In backend terminal
# Press Ctrl+C to stop
# Then run again:
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Solution 4: Check Browser Console Logs
I added detailed logging to the API client. Open browser console (F12) and look for:
```
Fetching algorithms from: http://localhost:8000/api/algorithms
Response status: ...
```

This will tell us exactly what's happening.

## YAML Parser Fix

✅ **FIXED** - The parser now correctly handles:
- Root-level fields (like `algorithm: genetic_algorithm`)
- Nested sections (`problem:`, `params:`)
- Comments (lines starting with `#`)
- Numbers, booleans, and strings

## Testing Steps

### 1. Manual Input Test
1. Open `http://localhost:5173` (NOT 127.0.0.1)
2. Open browser console (F12)
3. Look for console logs showing fetch attempt
4. Select PSO algorithm
5. Click Run Algorithm

### 2. YAML Upload Test
1. Click "YAML Upload" tab
2. Copy this YAML:
```yaml
algorithm: genetic_algorithm
problem:
  dimensions: 2
  fitness_function: sphere
  lower_bound: -5
  upper_bound: 5
  objective: minimize
params:
  population_size: 50
  max_iterations: 50
  crossover_rate: 0.8
  mutation_rate: 0.1
  tournament_size: 3
```
3. Paste into textarea
4. Click "Run from YAML"

## Expected Console Output

When everything works, you should see:
```
Fetching algorithms from: http://localhost:8000/api/algorithms
Response status: 200 OK
Algorithms data: {algorithms: Array(2)}
Sending payload: {algorithm: "particle_swarm", problem: {...}, params: {...}}
```

## Common Issues & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to fetch` | Backend not running | Start backend |
| `CORS policy` | Wrong URL or CORS not configured | Use localhost:5173 |
| `net::ERR_CONNECTION_REFUSED` | Backend crashed or wrong port | Restart backend on port 8000 |
| `YAML must contain "algorithm" field` | Parser bug | FIXED - reload frontend |
| `404 Not Found` | Wrong endpoint URL | Check API_BASE in api/index.js |

## Next Steps

1. **Check browser console** - Tell me what errors you see
2. **Verify URL** - Are you using `localhost:5173` or `127.0.0.1:5173`?
3. **Test backend directly** - Run the curl command above
4. **Share console logs** - Copy the console output

Once we see the actual error message, we can fix it immediately!
