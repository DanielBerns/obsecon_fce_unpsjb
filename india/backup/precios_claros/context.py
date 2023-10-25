from pathlib import Path
import sys

p = Path('./').absolute()
q = str(p.parents[1])
sys.path.insert(0, q)

import components
