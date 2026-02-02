import subprocess
import threading
import time

def run_backend():
    try:
        subprocess.run(["uvicorn", "app.backend.web_rag_api:app", "--host", "localhost", "--port", "9999"], check=True)
    except Exception as e:
        print(e)
    
def run_frontend():
    try:
        subprocess.run(["streamlit", "run", "app/frontend/index.py"], check=True)
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    try:
        threading.Thread(target = run_backend).start()
        time.sleep(2)
        run_frontend()
    except Exception as e:
        print(e)