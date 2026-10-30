import os
import shutil

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Storage folders
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    PROJECTS_FOLDER = os.path.join(BASE_DIR, 'projects')
    EXPORTS_FOLDER = os.path.join(BASE_DIR, 'exports')
    
    # 100 MB max upload limit
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    
    # Allowed extensions
    ALLOWED_EXTENSIONS = {'pdf', 'pptx', 'ppt'}
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'free-corat-coret-ppt-secret-2026')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1')
    
    @classmethod
    def get_libreoffice_path(cls):
        """Auto-detect LibreOffice / soffice binary across OS platforms."""
        # Check custom environment variable
        custom_path = os.environ.get('LIBREOFFICE_PATH')
        if custom_path and os.path.isfile(custom_path):
            return custom_path
            
        # Check system PATH
        for cmd in ['libreoffice', 'soffice']:
            found = shutil.which(cmd)
            if found:
                return found
                
        # Common Windows paths
        win_candidates = [
            r'C:\Program Files\LibreOffice\program\soffice.exe',
            r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
            os.path.expandvars(r'%LOCALAPPDATA%\Programs\LibreOffice\program\soffice.exe'),
        ]
        for path in win_candidates:
            if os.path.isfile(path):
                return path
                
        # Common Linux / macOS paths
        nix_candidates = [
            '/usr/bin/libreoffice',
            '/usr/bin/soffice',
            '/usr/local/bin/soffice',
            '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        ]
        for path in nix_candidates:
            if os.path.isfile(path):
                return path
                
        return None

    @classmethod
    def init_folders(cls):
        """Ensure all required storage directories exist."""
        for folder in [cls.UPLOAD_FOLDER, cls.PROJECTS_FOLDER, cls.EXPORTS_FOLDER]:
            os.makedirs(folder, exist_ok=True)

