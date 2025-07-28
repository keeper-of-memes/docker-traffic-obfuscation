import asyncio
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

# Default websites if file is missing
DEFAULT_WEBSITES = [
    "https://en.wikipedia.org/wiki/Random",
    "https://www.bbc.co.uk/news",
    "https://www.reddit.com/r/random",
    "https://www.theguardian.com",
    "https://www.youtube.com",
]

# Load websites from file
def load_websites(file_path="/home/appuser/websites.txt"):
    try:
        with open(file_path, 'r') as f:
            websites = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        if not websites:
            print(f"Warning: {file_path} is empty, using default websites")
            return DEFAULT_WEBSITES
        print(f"Loaded {len(websites)} websites from {file_path}")
        return websites
    except FileNotFoundError:
        print(f"Warning: Websites file {file_path} not found, using default websites")
        return DEFAULT_WEBSITES
    except Exception as e:
        print(f"Error reading websites file: {e}, using default websites")
        return DEFAULT_WEBSITES

WEBSITES = load_websites()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

async def random_browsing(task_id: int):
    """Simulate random browsing with Selenium."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
    options.add_argument(f"--window-size={random.randint(800, 1920)},{random.randint(600, 1080)}")

    try:
        driver = webdriver.Chrome(options=options)
        for i in range(100):  # Reduce for multiple tasks
            site = random.choice(WEBSITES)
            try:
                driver.get(site)
                print(f"[Task {task_id}] Visited: {site}")
                await asyncio.sleep(random.uniform(1, 10))

                links = driver.find_elements(By.TAG_NAME, "a")
                if links:
                    random.choice(links).click()
                    print(f"[Task {task_id}] Clicked random link")

                await asyncio.sleep(random.uniform(2, 15))
            except WebDriverException as e:
                print(f"[Task {task_id}] Browsing error: {e}")
            await asyncio.sleep(0.1)
    finally:
        driver.quit()
        print(f"[Task {task_id}] Browser closed")

async def main(concurrency=3):
    """Launch multiple browsing tasks concurrently."""
    tasks = [asyncio.create_task(random_browsing(i)) for i in range(concurrency)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main(concurrency=3))  # Adjust concurrency here
