# main.py
from script import Interface

if __name__ == "__main__":
    # Ensure the history directory exists before starting the app
    # (The Interface class also does this, but doing it here is safe too)
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    history_dir = os.path.join(script_dir, 'history')
    if not os.path.exists(history_dir):
        try:
            os.makedirs(history_dir)
        except OSError as e:
             print(f"Could not create history directory at launch: {e}")

    app = Interface()
    app.run_app()