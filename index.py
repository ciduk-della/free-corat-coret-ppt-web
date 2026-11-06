import os
from flask import Flask

base_dir = os.path.abspath(os.path.dirname(app.py))
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, 'templates'),
            static_folder=os.path.join(base_dir, 'static'))
