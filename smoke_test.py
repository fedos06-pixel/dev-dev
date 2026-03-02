import sys
import os

def main():
    print(">>> Smoke Test Started")
    
    # 1. Проверка импортов
    try:
        import fastapi
        import uvicorn
        print("[OK] Dependencies imported successfully")
    except ImportError as e:
        print(f"[FAIL] Missing dependency: {e}")
        sys.exit(1)

    # 2. Проверка наличия demo_project
    demo_path = os.path.join(os.path.dirname(__file__), "demo_project")
    if not os.path.exists(demo_path):
        print(f"[FAIL] demo_project folder not found at {demo_path}")
        sys.exit(1)
    print("[OK] demo_project folder exists")

    # 3. Проверка наличия данных
    sample_file = os.path.join(demo_path, "sample_data.json")
    if not os.path.exists(sample_file):
        print(f"[FAIL] sample_data.json not found")
        sys.exit(1)
    print("[OK] Test data exists")

    # 4. Проверка логики приложения (импорт main)
    try:
        from main import app
        if not hasattr(app, 'router'):
            raise Exception("App structure invalid")
        print("[OK] Application logic loads correctly")
    except Exception as e:
        print(f"[FAIL] Application error: {e}")
        sys.exit(1)

    print(">>> Smoke Test Passed Successfully")
    sys.exit(0)

if __name__ == "__main__":
    main()
