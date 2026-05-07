import pandas as pd
import time
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def extract_comments_from_links():
    input_path = os.path.join("data", "raw", "ig_post_links.xlsx")
    if not os.path.exists(input_path): return
    
    df_links = pd.read_excel(input_path)
    # Filter link milik dispendukcapil saja
    links = df_links[df_links['post_url'].str.contains('dispendukcapil.sby', na=False)]['post_url'].tolist()

    options = uc.ChromeOptions()
    profile_path = os.path.join(os.getcwd(), 'ig_profile')
    options.add_argument(f"--user-data-dir={profile_path}")
    driver = uc.Chrome(options=options, version_main=144)
    
    all_results = []

    try:
        for idx, url in enumerate(links):
            print(f"\n[{idx+1}/{len(links)}] Memproses: {url}")
            driver.get(url)
            time.sleep(10) # Beri waktu ekstra untuk loading IG yang berat

            # STRATEGI: Ambil semua elemen <li> di dalam <ul> manapun yang muncul
            # karena berdasarkan HTML Anda, komentar selalu dibungkus <li>
            items = driver.find_elements(By.TAG_NAME, "li")
            
            valid_comments = 0
            for item in items:
                try:
                    # Ambil teks mentah dari li tersebut
                    raw_text = item.text
                    
                    # Logika Filter:
                    # 1. Komentar biasanya punya teks "Reply" atau "Balas"
                    # 2. Kita cari span dengan class _ap3a yang Anda temukan
                    if "Reply" in raw_text or "Balas" in raw_text:
                        # Cari teks komentar di dalam span _ap3a
                        comment_el = item.find_element(By.CSS_SELECTOR, "span._ap3a")
                        comment_text = comment_el.text.strip()
                        
                        # Cari username (biasanya kata pertama atau di tag a)
                        user_name = item.find_element(By.TAG_NAME, "a").text.strip()

                        if comment_text and user_name:
                            all_results.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d"),
                                "user": user_name,
                                "comments": comment_text,
                                "post_url": url,
                                "source": "Instagram"
                            })
                            valid_comments += 1
                except:
                    continue
            
            print(f"   -> Berhasil mengambil {valid_comments} komentar.")
            
            # Jika tetap 0, mungkin karena perlu scroll
            if valid_comments == 0:
                driver.execute_script("window.scrollTo(0, 500);")
                print("   -> Mencoba scroll karena tidak ada data...")

    finally:
        if all_results:
            output_path = os.path.join("data", "raw", "instagram_comments_final.xlsx")
            pd.DataFrame(all_results).to_excel(output_path, index=False)
            print(f"\nSUKSES! Data tersimpan di {output_path}")
        driver.quit()

if __name__ == "__main__":
    extract_comments_from_links()