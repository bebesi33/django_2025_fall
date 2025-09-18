# run_waitress.py

from waitress import serve
import hello  # Importáljuk az előzőleg létrehozott alkalmazást

serve(hello.application, host='0.0.0.0', port=8080)
