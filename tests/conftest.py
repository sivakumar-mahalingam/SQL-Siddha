import sys
from pathlib import Path

# Ensure the project root is on the path for imports
root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
