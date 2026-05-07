import pandas as pd
import time
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_playstore(url, num_scrolls=20):
    options = uc.ChromeOptions()
    options.add_argument("--lang=id")
    profile_path = os.path.join(os.getcwd(), 'playstore_profile')
    options.add_argument(f"--user-data-dir={profile_path}")
    
    driver = uc.Chrome(options=options, version_main=144)
    results = []

    try:
        print(f"\nMengakses Google Play Store: {url}")
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        try:
            all_reviews_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Lihat semua ulasan')]")))
            driver.execute_script("arguments[0].click();", all_reviews_btn)
            time.sleep(3)
        except:
            print("Peringatan: Modal ulasan mungkin sudah terbuka atau tombol tidak ditemukan.")

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "RHo1pe")))
        scrollable_div = driver.find_element(By.CLASS_NAME, "fysCi")

        print("Memulai proses scroll...")
        last_count = 0
        for i in range(1, num_scrolls + 1):
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)
            time.sleep(2)
            current_count = len(driver.find_elements(By.CLASS_NAME, "RHo1pe"))
            if i % 5 == 0: print(f"Scroll {i} | Terdeteksi: {current_count} elemen")
            if current_count == last_count and i > 5: break
            last_count = current_count

        print("\nScrolling selesai. Mengekstrak ulasan yang memiliki komentar...")
        reviews = driver.find_elements(By.CLASS_NAME, "RHo1pe")
        
        for r in reviews:
            try:
                comment_text = r.find_element(By.CSS_SELECTOR, "div.h3YV2d").text
                
                if comment_text.strip(): 
                    user_name = r.find_element(By.CSS_SELECTOR, "div.X5PpBb").text
                    date_text = r.find_element(By.CSS_SELECTOR, "span.bp9Aid").text

                    results.append({
                        "timestamp": date_text,
                        "user": user_name,
                        "comments": comment_text,
                        "source": "Play Store"
                    })
            except:
                continue

    finally:
        if results:
            df = pd.DataFrame(results)
            output_path = os.path.join("data", "raw", "klampid_playstore_reviews.xlsx")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_excel(output_path, index=False)
            print(f"\nSUKSES! Berhasil menyimpan {len(df)} ulasan yang berisi teks.")
            print(f"File tersimpan di: {output_path}")
        else:
            print("\nGAGAL: Tidak ada ulasan dengan teks komentar yang ditemukan.")
        driver.quit()

if __name__ == "__main__":
    url_klampid = "https://play.google.com/store/apps/details?id=id.disdukcapilsurabaya.kng&hl=id"
    scrape_playstore(url_klampid)