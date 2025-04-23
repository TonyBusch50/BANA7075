import multiprocessing
import os
import signal
import sys

import uvicorn


def run_fastapi():
    """Start the FastAPI app"""
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=5000)


def run_streamlit():
    """Start the Streamlit app"""
    os.system("streamlit run streamlit_app.py")


def shutdown_handler(signum, frame):
    """Gracefully terminate child processes"""
    print("\nShutting down FastAPI and Streamlit...")

    p1.terminate()
    p2.terminate()

    p1.join()
    p2.join()

    sys.exit(0)  # Exit the script cleanly


if __name__ == "__main__":
    # Run FastAPI and Streamlit in parallel processes
    multiprocessing.set_start_method("spawn")

    p1 = multiprocessing.Process(target=run_fastapi, daemon=True)  # Set daemon mode
    p2 = multiprocessing.Process(target=run_streamlit, daemon=True)

    p1.start()
    p2.start()

    # Capture termination signals
    signal.signal(signal.SIGINT, shutdown_handler)  # Handle Ctrl+C
    signal.signal(
        signal.SIGTERM, shutdown_handler
    )  # Handle termination (e.g., Docker stop)

    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        shutdown_handler(None, None)  # Gracefully shut down on manual interrupt