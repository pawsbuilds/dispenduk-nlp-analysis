import pandas as pd
import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def collect_ig_links(profile_url, scroll_count=30):
    options = uc.ChromeOptions()
    profile_path = os.path.join(os.getcwd(), 'ig_profile')
    options.add_argument(f"--user-data-dir={profile_path}")
    
    driver = uc.Chrome(options=options , version_main=144)
    post_links = set()

    try:
        driver.get("https://www.instagram.com/")
        print("\n[!] Silakan LOGIN manual di browser jika belum.")
        input(">>> Buka profil target, lalu tekan ENTER di sini...")
        
        driver.get(profile_url)
        time.sleep(5)

        print("Sedang mengumpulkan link (mengabaikan class yang panjang)...")
        for i in range(1, scroll_count + 1):
            elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/'], a[href*='/reel/']")
            
            for el in elements:
                href = el.get_attribute('href')
                if href not in post_links:
                    post_links.add(href)
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            print(f"Scroll {i}/{scroll_count} | Total link unik: {len(post_links)}")

        df = pd.DataFrame(list(post_links), columns=['post_url'])
        output_path = os.path.join("data", "raw", "ig_post_links.xlsx")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False)
        print(f"\nSUKSES! {len(df)} link disimpan di {output_path}")

    finally:
        driver.quit()

if __name__ == "__main__":
    target = "https://www.instagram.com/dispendukcapil.sby/"
    collect_ig_links(target, scroll_count=100)