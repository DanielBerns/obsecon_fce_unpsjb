from pathlib import Path
import sys

p = Path('./').absolute()
q = Path(p.parents[0], 'india')
sys.path.insert(0, str(q))

import components
