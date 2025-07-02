#!/usr/bin/env python
"""
Test runner script that sets up the Python path correctly.
"""
import sys
import os
import subprocess

# Add src directory to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

if __name__ == "__main__":
    # Set PYTHONPATH environment variable
    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    if current_pythonpath:
        env['PYTHONPATH'] = f"{src_path}:{current_pythonpath}"
    else:
        env['PYTHONPATH'] = src_path
    
    # Run pytest with the correct environment
    cmd = ["pytest", "tests/", "-v"] + sys.argv[1:]
    result = subprocess.run(cmd, env=env)
    sys.exit(result.returncode)