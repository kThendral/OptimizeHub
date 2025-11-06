"""
Example: Malicious Function
This function attempts dangerous operations to test Docker sandbox security.
Should be BLOCKED by security measures.
"""
import os
import subprocess

def fitness(x):
    """
    Malicious function that tries to:
    1. Access system files
    2. Execute shell commands
    3. Write to filesystem
    
    All operations should FAIL in a secure sandbox.
    """
    # Try to read sensitive system file
    try:
        with open('/etc/passwd', 'r') as f:
            data = f.read()
    except:
        pass
    
    # Try to execute system command
    try:
        subprocess.run(['ls', '/'], capture_output=True)
    except:
        pass
    
    # Try to write file
    try:
        with open('/tmp/breach.txt', 'w') as f:
            f.write('Security compromised!')
    except:
        pass
    
    # Return fitness (should never reach here in secure sandbox)
    return sum(x**2)