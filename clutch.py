# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# options = uc.ChromeOptions()

# driver = uc.Chrome(
#     version_main=149,
#     options=options,
#     headless=False
# )

# wait = WebDriverWait(driver, 20)

# driver.get("https://clutch.co/profile/funnel-boost-media")

# # Wait until reviewer names are present
# wait.until(
#     EC.presence_of_element_located(
#         (By.CSS_SELECTOR, "div.reviewer_card--name")
#     )
# )

# names = driver.find_elements(By.CSS_SELECTOR, "div.reviewer_card--name")
# companies = driver.find_elements(By.CSS_SELECTOR, "div.reviewer_position")

# print("Names found:", len(names))
# print("Companies found:", len(companies))

# for i in range(max(len(names), len(companies))):
#     print("-" * 60)

#     name = names[i].text if i < len(names) else ""
#     company = companies[i].text if i < len(companies) else ""

#     print("Name    :", name)
#     print("Company :", company)

# input("\nPress Enter to close...")
# driver.quit()

import time
import pandas as pd
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------
# Start Browser
# ------------------------
options = uc.ChromeOptions()

driver = uc.Chrome(
    version_main=149,
    options=options,
    headless=False
)

wait = WebDriverWait(driver, 20)

# ------------------------
# Open Listing Page
# ------------------------
listing_url = "https://clutch.co/agencies/digital-marketing"

driver.get(listing_url)

wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, 'a[href*="/profile/"]')
    )
)

time.sleep(3)

# ------------------------
# Collect Profile Links
# ------------------------
# Get only the company profile links

profile_urls = []

links = driver.find_elements(
    By.CSS_SELECTOR,
    "a.provider__title-link.directory_profile"
)

for link in links:
    if not link.is_displayed():
        continue

    url = link.get_attribute("href")

    if url and url not in profile_urls:
        profile_urls.append(url)
        print(url)

print(f"\nVisible profiles: {len(profile_urls)}")
# ------------------------
# Visit Every Profile
# ------------------------
all_reviews = []

for index, profile in enumerate(profile_urls, start=1):

    print("=" * 80)
    print(f"[{index}/{len(profile_urls)}] {profile}")

    try:
        driver.get(profile)

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.reviewer_card--name")
            )
        )

        names = driver.find_elements(
            By.CSS_SELECTOR,
            "div.reviewer_card--name"
        )

        companies = driver.find_elements(
            By.CSS_SELECTOR,
            "div.reviewer_position"
        )

        print(f"Reviews found: {len(names)}")

        for name, company in zip(names, companies):

            print(f"{name.text} | {company.text}")

            all_reviews.append({
                "Profile URL": profile,
                "Reviewer Name": name.text,
                "Reviewer Company": company.text
            })
    except Exception as e:
        print("Error:", e)

    time.sleep(2)

driver.quit()

# ------------------------
# Save CSV
# ------------------------
df = pd.DataFrame(all_reviews)

df.to_csv("clutch_reviews.csv", index=False, encoding="utf-8-sig")

print("\nDone!")
print(f"Total Reviews: {len(df)}")
print("Saved as clutch_reviews.csv")