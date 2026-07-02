"""
Production scraper template.
NOTE: Fill in selectors if Clutch changes them.
"""
import csv, json, logging, random, time
from logging.handlers import RotatingFileHandler
from pathlib import Path
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TOTAL_PAGES=2522
START_PAGE=1
CHECKPOINT="state.json"
OUT="output/clutch_reviews.csv"

def setup_logger():
    Path("logs").mkdir(exist_ok=True)
    log=logging.getLogger("scraper")
    log.setLevel(logging.INFO)
    fh=RotatingFileHandler("logs/scraper.log",maxBytes=5_000_000,backupCount=5)
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(fh)
    log.addHandler(logging.StreamHandler())
    return log

log=setup_logger()

def load_state():
    if Path(CHECKPOINT).exists():
        return json.loads(Path(CHECKPOINT).read_text())
    return {"page":START_PAGE}

def save_state(page):
    Path(CHECKPOINT).write_text(json.dumps({"page":page}))

def driver():
    opt=uc.ChromeOptions()
    d=uc.Chrome(version_main=149,options=opt,headless=False)
    d.set_page_load_timeout(60)
    return d

def sleep():
    time.sleep(random.uniform(2,5))

def append(rows):
    Path("output").mkdir(exist_ok=True)
    exists=Path(OUT).exists()
    with open(OUT,"a",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=["Profile URL","Reviewer Name","Reviewer Company"])
        if not exists: w.writeheader()
        w.writerows(rows)

def profile_links(d,w,page):
    d.get(f"https://clutch.co/agencies/digital-marketing?page={page}")
    w.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a.provider__title-link.directory_profile")))
    links=[]
    for e in d.find_elements(By.CSS_SELECTOR,"a.provider__title-link.directory_profile"):
        if e.is_displayed():
            u=e.get_attribute("href")
            if u and u not in links: links.append(u)
    return links

def scrape_profile(d,w,url):
    d.get(url)
    w.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.reviewer_card--name")))
    names=d.find_elements(By.CSS_SELECTOR,"div.reviewer_card--name")
    comps=d.find_elements(By.CSS_SELECTOR,"div.reviewer_position")
    out=[]
    for n,c in zip(names,comps):
        out.append({"Profile URL":url,"Reviewer Name":n.text,"Reviewer Company":c.text})
    return out

def main():
    st=load_state()
    d=driver()
    w=WebDriverWait(d,20)
    try:
        for page in range(st["page"],TOTAL_PAGES+1):
            log.info(f"Page {page}")
            rows=[]
            try:
                urls=profile_links(d,w,page)
                for u in urls:
                    ok=False
                    for _ in range(3):
                        try:
                            rows.extend(scrape_profile(d,w,u))
                            ok=True
                            break
                        except Exception as e:
                            log.exception(e)
                            sleep()
                    if not ok:
                        with open("output/failed_profiles.csv","a") as f:
                            f.write(u+"\n")
                    sleep()
                append(rows)
                save_state(page+1)
            except Exception as e:
                log.exception(e)
                save_state(page)
                raise
            if page%75==0:
                d.quit()
                d=driver()
                w=WebDriverWait(d,20)
    finally:
        d.quit()

if __name__=="__main__":
    main()
