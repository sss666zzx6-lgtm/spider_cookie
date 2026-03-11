import os
import sys

# 添加项目根目录到 Python 路径，方便子模块导入 util
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
