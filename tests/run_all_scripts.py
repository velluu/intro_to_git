import os
import subprocess

base = os.path.join(os.path.dirname(__file__), "..", "scripts")

for folder in sorted(os.listdir(base)):
    path = os.path.join(base, folder, "main.py")
    if os.path.isfile(path):
        print(f"Running {path}...")

        try:
            result = subprocess.run(
                ["python3", path],
                capture_output=True,
                text=True,
                timeout=10,  # <= limit execution to 10 seconds
            )

            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            # Detect input requirement (common case)
            if "EOFError" in stderr:
                print("⚠️  INPUT REQUIRED (script waits for input)\n")
                continue

            if result.returncode == 0:
                print("✅ PASS")
                if stdout:
                    print("Output:", stdout)
                print()
            else:
                print("❌ FAIL")
                if stderr:
                    print(stderr)
                print()

        except subprocess.TimeoutExpired:
            print("⏱️  TIMEOUT (took > 10s, possible infinite loop)\n")
