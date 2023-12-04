from pathlib import Path
import sys

TEST_ROOT = Path('~', 'Tests').expanduser()

p = Path('./').absolute()
q = Path(p.parents[0], 'juliet')
sys.path.insert(0, str(q))

import components
