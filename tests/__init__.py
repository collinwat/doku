import sys
import os

TESTS = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.dirname(TESTS)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
