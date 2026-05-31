import os
import subprocess
import sys

def run_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scripts = [
        "gemma2/gemma2_eval.py",
        "phi3/phi3_eval.py",
        "tinyllama/tinyllama_eval.py"
    ]
    
    python_exe = sys.executable
    print(f"Starting Assignment-2 Evaluations...")
    print(f"Using Python: {python_exe}\n")
    
    for script_name in scripts:
        script_path = os.path.join(script_dir, script_name)
        print("="*60)
        print(f"Executing: {script_name}")
        print("="*60)
        
        if not os.path.exists(script_path):
            print(f"Error: Script {script_name} does not exist at {script_path}")
            continue
            
        result = subprocess.run([python_exe, script_path], capture_output=True, text=True)
        
        print("STDOUT Output:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR Errors:")
            print(result.stderr)
            
    print("\nAll Assignment-2 evaluations have finished executing.")

if __name__ == "__main__":
    run_all()
