import os
import sys
import traceback

# Tambahkan direktori root dan direktori saat ini ke sys.path
current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, '..'))

for p in [root_dir, current_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

class VercelWSGIMiddleware:
    """
    Middleware untuk:
    1. Memulihkan PATH_INFO dari header Vercel ketika rewrite dilakukan.
    2. Menangkap semua runtime error agar tidak menyebabkan '500 FUNCTION_INVOCATION_FAILED'
       dan menampilkan pesan traceback error yang jelas di layar.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        try:
            path_info = environ.get('PATH_INFO', '')
            
            # Cek apakah Vercel mengubah PATH_INFO menjadi /api/index
            if path_info in ('/api/index', '/api/index/'):
                orig = (
                    environ.get('HTTP_X_FORWARDED_URI') or
                    environ.get('HTTP_X_MATCHED_PATH') or
                    environ.get('RAW_URI') or
                    environ.get('REQUEST_URI') or
                    ''
                ).split('?')[0]
                
                if orig and orig not in ('/api/index', '/api/index/'):
                    environ['PATH_INFO'] = orig
                else:
                    environ['PATH_INFO'] = '/'
            elif path_info.startswith('/api/index/'):
                environ['PATH_INFO'] = path_info[len('/api/index'):]

            return self.wsgi_app(environ, start_response)
        except Exception:
            err = traceback.format_exc()
            print("RUNTIME INVOCATION ERROR:\n", err, file=sys.stderr)
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            start_response(status, headers)
            html = f"""
            <!DOCTYPE html>
            <html>
            <head><title>Vercel Runtime Error</title></head>
            <body style="font-family: monospace; padding: 25px; background: #18181b; color: #f87171;">
                <h2>❌ Runtime Error pada Vercel Function</h2>
                <p style="color: #cbd5e1;">Aplikasi mengalami error saat memproses permintaan:</p>
                <pre style="background: #27272a; color: #f1f5f9; padding: 16px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap;">{err}</pre>
            </body>
            </html>
            """
            return [html.encode('utf-8')]

try:
    from app import create_app
    raw_app = create_app()
    # Terapkan middleware
    raw_app.wsgi_app = VercelWSGIMiddleware(raw_app.wsgi_app)
    app = raw_app
except Exception as e:
    # Tangkap error startup dan tampilkan langsung di browser agar mudah didebug
    from flask import Flask
    error_detail = traceback.format_exc()
    print("FATAL STARTUP ERROR:", error_detail, file=sys.stderr)
    
    app = Flask(__name__)
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def debug_error(path):
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Startup Error</title></head>
        <body style="font-family: monospace; padding: 20px; background: #18181b; color: #f87171;">
            <h2>❌ Startup Error pada Vercel</h2>
            <p style="color: #cbd5e1;">Terjadi kesalahan saat inisialisasi aplikasi:</p>
            <pre style="background: #27272a; color: #f1f5f9; padding: 15px; border-radius: 6px; overflow-x: auto; white-space: pre-wrap;">{error_detail}</pre>
        </body>
        </html>
        """, 500
