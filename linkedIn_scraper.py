from linkedin_scraper import actions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

# === Configuration ===
email = "hanzala0877@gmail.com"
password = "hanzala@123"
search_query = "Machine Learning Engineer"
location = "Pakistan"

# === Initialize Driver ===
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment for headless
driver = webdriver.Chrome(options=options)

try:
    # === Step 1: Login via linkedin_scraper ===
    print("Logging in...")
    actions.login(driver, email, password)
    print("Login successful.")

    # === Step 2: Navigate to job search ===
    url = (
        f"https://www.linkedin.com/jobs/search/?"
        f"keywords={search_query.replace(' ', '%20')}&"
        f"location={location.replace(' ', '%20')}&"
        f"refresh=true"
    )
    driver.get(url)
    time.sleep(5)

    # Wait for job cards to appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-occludable-job-id]"))
    )

    # === Step 3: Scroll to load more jobs ===
    print("Loading job listings...")
    scroll_pause = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # === Step 4: Parse job cards using exact structure from your HTML ===
    job_cards = driver.find_elements(By.CSS_SELECTOR, "li[data-occludable-job-id]")
    print(f"Found {len(job_cards)} job cards.")

    jobs = []

    for card in job_cards:
        try:
            # Extract job ID
            job_id = card.get_attribute("data-occludable-job-id")

            # Title & link
            title_elem = card.find_element(By.CSS_SELECTOR, "a.job-card-container__link[aria-label]")
            title = title_elem.get_attribute("aria-label")
            job_url = title_elem.get_attribute("href")

            # Company name
            company = ""
            try:
                company_elem = card.find_element(By.CSS_SELECTOR, ".artdeco-entity-lockup__subtitle span")
                company = company_elem.text.strip()
            except:
                pass

            # Location
            location_text = ""
            try:
                loc_elem = card.find_element(By.CSS_SELECTOR, ".job-card-container__metadata-wrapper li span")
                location_text = loc_elem.text.strip()
            except:
                pass

            # Posted time
            posted_time = ""
            try:
                time_elem = card.find_element(By.CSS_SELECTOR, "time")
                posted_time = time_elem.text.strip()
            except:
                pass

            # Easy Apply?
            easy_apply = False
            try:
                card.find_element(By.XPATH, ".//span[contains(text(), 'Easy Apply')]")
                easy_apply = True
            except NoSuchElementException:
                pass

            # Actively reviewing?
            actively_reviewing = False
            try:
                card.find_element(By.XPATH, ".//span[contains(text(), 'Actively reviewing applicants')]")
                actively_reviewing = True
            except NoSuchElementException:
                pass

            jobs.append({
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location_text,
                "posted": posted_time,
                "easy_apply": easy_apply,
                "actively_reviewing": actively_reviewing,
                "job_url": job_url
            })

        except Exception as e:
            print(f"Skipping a card due to error: {e}")
            continue

    # === Step 5: Output Results ===
    print(f"\nSuccessfully extracted {len(jobs)} jobs.\n")
    for job in jobs[:3]:  # Preview first 3
        print(json.dumps(job, indent=2))

    # Save full results
    with open("linkedin_ml_jobs_pakistan.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

finally:
    input("\nPress Enter to close browser...")
    driver.quit()