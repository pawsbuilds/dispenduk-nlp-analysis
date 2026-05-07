import pandas as pd
import time
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_google_maps(url, num_scrolls=700): 
    options = uc.ChromeOptions()
    options.add_argument("--lang=id")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'id,id-ID'})
    
    profile_path = os.path.join(os.getcwd(), 'chrome_profile')
    options.add_argument(f"--user-data-dir={profile_path}")
    
    driver = uc.Chrome(options=options, version_main=144)
    results = []

    try:
        print("\n=== LOGIN MANUAL ===")
        driver.get("https://accounts.google.com/")
        input("Setelah sukses login dan masuk ke tampilan Maps, tekan ENTER di sini...")

        target_url = f"{url}&hl=id" if "?" in url else f"{url}?hl=id"
        print(f"Mengakses URL: {target_url}")
        driver.get(target_url)
        
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jftiEf")))
        time.sleep(5)

        scrollable_div = driver.execute_script(
            "return document.querySelector('div[role=\"main\"] div[tabindex=\"-1\"]') || "
            "document.querySelector('div.m679nn.ecceSd');"
        )

        print("Memulai Intelligent Deep Scroll...")
        
        last_count = len(driver.find_elements(By.CLASS_NAME, "jftiEf"))
        no_progress_count = 0

        for i in range(1, num_scrolls + 1):
            if i % 15 == 0:
                driver.execute_script("arguments[0].click();", scrollable_div)
                time.sleep(1)

            if i % 25 == 0:
                print(f"\n[Deep Mode] Memberikan jeda 30 detik agar RAM/CPU stabil...")
                time.sleep(30)

            if last_count > 1000 and i % 5 == 0:
                driver.execute_script("arguments[0].scrollBy(0, -800);", scrollable_div)
                time.sleep(2)

            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)
            
            start_time = time.time()
            if last_count > 2000:
                timeout = 100  
            elif last_count > 1000:
                timeout = 50  
            else:
                timeout = 20
                
            loading_success = False
            
            while time.time() - start_time < timeout:
                current_count = len(driver.find_elements(By.CLASS_NAME, "jftiEf"))
                
                if current_count > last_count:
                    actual_wait = round(time.time() - start_time, 2)
                    print(f"Scroll {i}: Dimuat dalam {actual_wait}s. Total: {current_count}")
                    last_count = current_count
                    loading_success = True
                    no_progress_count = 0
                    break
                
                time.sleep(0.7)

            if not loading_success:
                no_progress_count += 1
                print(f"Scroll {i}: Gagal memuat ulasan baru (Timeout {timeout}s).")

                driver.execute_script("arguments[0].scrollTop -= 1000;", scrollable_div)
                time.sleep(2)
                driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)
                
                if no_progress_count >= 6:
                    print("Sudah mencapai batas maksimal respons Google Maps. Memulai ekstraksi...")
                    break

        print("\nMengekstrak ulasan...")
        final_items = driver.find_elements(By.CLASS_NAME, "jftiEf")
        
        for item in final_items:
            try:
                user = item.find_element(By.CSS_SELECTOR, "div.d4r55").text
                try:
                    more_btns = item.find_elements(By.CSS_SELECTOR, "button.w8Bnu")
                    if more_btns:
                        driver.execute_script("arguments[0].click();", more_btns[0])
                except: pass

                comment_element = item.find_element(By.CSS_SELECTOR, "span.wiI7pd")
                comment_text = comment_element.text

                if "(Diterjemahkan oleh Google)" in comment_text or "(Translated by Google)" in comment_text:
                    try:
                        original_text_element = item.find_element(By.CSS_SELECTOR, "div.MyEned span")
                        comment_text = original_text_element.text
                    except: pass

                results.append({
                    "timestamp": item.find_element(By.CLASS_NAME, "rsqa6b").text if item.find_elements(By.CLASS_NAME, "rsqa6b") else "N/A",
                    "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": user,
                    "comments": comment_text
                })
            except: continue

    except Exception as e:
        print(f"Terjadi Kesalahan: {e}")

    finally:
        if results:
            df = pd.DataFrame(results)
            df = df.drop_duplicates(subset=['user', 'comments'])
            output_path = os.path.join("data", "raw", "google_maps_reviews_deep.xlsx")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_excel(output_path, index=False)
            print(f"SUKSES! {len(df)} ulasan unik disimpan di {output_path}")
        driver.quit()

if __name__ == "__main__":
    url_target = "https://www.google.com/maps/place/Dinas+Kependudukan+dan+Pencatatan+Sipil+Kota+Surabaya/@-7.2489954,112.7355612,14.6z/data=!4m18!1m9!3m8!1s0x2dd7f942b8b351bf:0x32f07c5175c50974!2sDinas+Kependudukan+dan+Pencatatan+Sipil+Kota+Surabaya!8m2!3d-7.2563161!4d112.7374704!9m1!1b1!16s%2Fg%2F11cly85ds7!3m7!1s0x2dd7f942b8b351bf:0x32f07c5175c50974!8m2!3d-7.2563161!4d112.7374704!9m1!1b1!16s%2Fg%2F11cly85ds7?entry=ttu&g_ep=EgoyMDI2MDEyOC4wIKXMDSoASAFQAw%3D%3D" 
    scrape_google_maps(url_target, num_scrolls=700)