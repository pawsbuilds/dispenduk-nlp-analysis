import pandas as pd
import time
import os
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def chain_extract_comments(max_posts=300):
    options = uc.ChromeOptions()
    profile_path = os.path.join(os.getcwd(), 'ig_profile')
    options.add_argument(f"--user-data-dir={profile_path}")
    driver = uc.Chrome(options=options, version_main=144)
    
    all_results = []

    try:
        driver.get("https://www.instagram.com/dispendukcapil.sby/")
        print("\n[!] INSTRUKSI:")
        print("1. Pastikan Anda sudah login.")
        print("2. KLIK POSTINGAN PERTAMA di grid profil sampai muncul Pop-up (Modal).")
        input(">>> Jika Pop-up sudah muncul, tekan ENTER di sini untuk mulai...")

        for p in range(max_posts):
            print(f"\n[{p+1}/{max_posts}] Mengambil data postingan...")
            time.sleep(3) # Tunggu render modal

            # 1. Ambil URL Postingan saat ini (untuk referensi data)
            current_url = driver.current_url
            
            # 2. Ekstraksi Komentar di dalam Modal
            # Menggunakan class _a9zr yang Anda berikan
            comment_blocks = driver.find_elements(By.CSS_SELECTOR, "div._a9zr")
            
            post_comments_count = 0
            for i, block in enumerate(comment_blocks):
                try:
                    # Skip index 0 jika itu Caption (biasanya akun dispendukcapil.sby)
                    user_name = block.find_element(By.TAG_NAME, "h3").text.strip()
                    if i == 0 and "dispendukcapil" in user_name.lower():
                        continue

                    # Ambil teks komentar (class _ap3a yang Anda berikan)
                    comment_text = block.find_element(By.CSS_SELECTOR, "span._ap3a").text.strip()
                    
                    if comment_text:
                        all_results.append({
                            "timestamp": datetime.now().strftime("%Y-%m-%d"),
                            "user": user_name,
                            "comments": comment_text,
                            "post_url": current_url,
                            "source": "Instagram"
                        })
                        post_comments_count += 1
                except:
                    continue
            
            print(f"   -> Berhasil mengambil {post_comments_count} komentar.")

            # 3. Klik Tombol NEXT (Panah Kanan) dengan Pencarian Lebih Luas
            print("   -> Mencari tombol Next...")
            try:
                # Strategi: Cari tombol yang mengandung SVG dengan label 'Next' atau 'Berikutnya'
                # Menggunakan beberapa kemungkinan XPath agar tidak meleset
                next_xpaths = [
                    "//button[.//svg[@aria-label='Next']]",
                    "//button[.//svg[@aria-label='Berikutnya']]",
                    "//div[@role='button'][.//svg[@aria-label='Next']]",
                    "/html/body/div[contains(@class, 'x1n2onr6')]//button[.//svg]" # Target langsung ke modal
                ]
                
                next_button = None
                for xpath in next_xpaths:
                    found = driver.find_elements(By.XPATH, xpath)
                    if found:
                        # Cari yang benar-benar bisa diklik (biasanya yang di sisi kanan)
                        for btn in found:
                            if btn.is_displayed():
                                next_button = btn
                                break
                    if next_button: break

                if next_button:
                    # Gunakan JavaScript click agar lebih paksa (bypass jika tertutup elemen lain)
                    driver.execute_script("arguments[0].click();", next_button)
                    print("   -> Berhasil pindah ke postingan berikutnya.")
                    time.sleep(4) # Beri waktu loading post baru
                else:
                    # Jika tidak ketemu, coba tekan tombol panah kanan di keyboard
                    print("   -> Tombol tidak ditemukan via XPath, mencoba simulasi Keyboard...")
                    from selenium.webdriver.common.keys import Keys
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_RIGHT)
                    time.sleep(4)
                    
            except Exception as e:
                print(f"   -> Gagal navigasi: {str(e)}")
                break

            # Simpan berkala tiap 5 post
            if (p + 1) % 5 == 0:
                pd.DataFrame(all_results).to_excel("data/raw/instagram_comments_partial.xlsx", index=False)

    finally:
        if all_results:
            output_path = os.path.join("data", "raw", "instagram_comments_final.xlsx")
            pd.DataFrame(all_results).to_excel(output_path, index=False)
            print(f"\nSUKSES! {len(all_results)} komentar disimpan di {output_path}")
        driver.quit()

if __name__ == "__main__":
    chain_extract_comments()