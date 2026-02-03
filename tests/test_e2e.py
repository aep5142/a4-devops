from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

# App URL
BASE_URL = "http://127.0.0.1:5000"

# Start Flask / Uvicorn app
flask_process = subprocess.Popen(
    ["python", "app/main.py", "--host", "127.0.0.1", "--port", "5000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Wait a few seconds for the app to be ready
time.sleep(5)  # increase if needed

# Initialize Chrome browser
driver = webdriver.Chrome()

def test_e2e():
    try:
        # 1️⃣ Open app
        driver.get(BASE_URL)
        time.sleep(1)  # wait a bit for server

        # 2️⃣ Add a todo
        driver.get(f"{BASE_URL}/add?to_add_item=TestItem")
        time.sleep(0.5)
        assert "Added TestItem successfully" in driver.page_source

        # 3️⃣ View todos
        driver.get(f"{BASE_URL}/view")
        time.sleep(0.5)
        assert "TestItem" in driver.page_source

        # 4️⃣ Delete the todo
        driver.get(f"{BASE_URL}/delete?to_delete_item=TestItem")
        time.sleep(0.5)
        assert "Deleted TestItem successfully" in driver.page_source

        # 5️⃣ Verify deletion
        driver.get(f"{BASE_URL}/view")
        time.sleep(0.5)
        assert "TestItem" not in driver.page_source

        print("End-to-end test passed ✅")

    finally:
        driver.quit()
