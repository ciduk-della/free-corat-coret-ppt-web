import sys
import os

# Memastikan root folder masuk dalam path import Python
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import instance Flask dari file utama (aplikasi.py)
from aplikasi import app

# Vercel butuh ekspor objek 'app'