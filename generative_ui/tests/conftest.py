import os
import sys

# generative_ui/ を import ルートにする (adk web / uvicorn 実行時と同じ)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
