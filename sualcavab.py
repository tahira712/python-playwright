import csv
import time
from playwright.sync_api import Playwright, sync_playwright
import sys
import io

# Terminalın çıxışını UTF-8 formatına məcbur edirik
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Giriş hissəsi
    page.goto("https://sualcavab.com/admin/login.php")
    page.get_by_role("checkbox", name="Məni xatırla").check()
    page.get_by_role("textbox", name=" İstifadəçi adı").fill("Tahirə Hüseynova")
    page.get_by_role("textbox", name=" Parol").fill("0555229455")
    page.get_by_role("button", name=" Daxil ol").click()
    
    print("Giriş edildi. Panel yüklənir...")
    time.sleep(5)
    
    # Suallar səhifəsinə keçid
    page.goto("https://sualcavab.com/admin/questions.php")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    with open("suallar.csv", mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        
        for row in reader:
            current_id = row['ID'].strip()
            try:
                print(f"ID {current_id} axtarılır...")
                
                # Axtarış qutusunu tapırıq
                search_input = page.locator("input[type='search']")
                if not search_input.count():
                    search_input = page.get_by_placeholder("Axtar")
                if not search_input.count():
                    search_input = page.get_by_role("textbox").first
                
                search_input.clear()
                search_input.fill(current_id)
                search_input.press("Enter")
                time.sleep(2)
                
                # ID-yə klikləyirik
                target_cell = page.get_by_role("cell", name=current_id, exact=False)
                if not target_cell.count():
                    target_cell = page.get_by_text(current_id).first
                    
                target_cell.click(timeout=5000)
                
                # Modalı açırıq
                page.get_by_role("button", name=" Dəyişiklik təklif et").click(timeout=5000)
                time.sleep(1.5)
                
                # Formu doldururuq (Mətn sahələri)
                page.get_by_role("textbox", name="Sual Mətni *").fill(row['Sual'])
                page.get_by_role("textbox", name="A Variantı *").fill(row['A'])
                page.get_by_role("textbox", name="B Variantı *").fill(row['B'])
                page.get_by_role("textbox", name="C Variantı").fill(row['C'])
                page.get_by_role("textbox", name="D Variantı").fill(row['D'])
                page.get_by_role("textbox", name="E Variantı").fill(row['E'])
                
                # -------------------------------------------------------------
                # 🛠️ 1. SUAL TİPİNİN SEÇİLMƏSİ (Value ilə: 1, 2, 3, 4, 5, 6)
                try:
                    type_val = "1"  # Default: Çox seçimli
                    csv_type = row['Sual Tipi'].strip().lower()
                    
                    if "çox" in csv_type or "cox" in csv_type:
                        type_val = "1"
                    elif "açıq" in csv_type or "aciq" in csv_type:
                        type_val = "2"
                    elif "doğru" in csv_type or "dogru" in csv_type or "səhv" in csv_type:
                        type_val = "3"
                    elif "səbəb" in csv_type or "sebeb" in csv_type or "nəticə" in csv_type:
                        type_val = "4"
                    elif "boşluq" in csv_type or "bosluq" in csv_type:
                        type_val = "5"
                    elif "kombinasiya" in csv_type:
                        type_val = "6"
                        
                    page.locator("#propQuestionType").select_option(value=type_val)
                except Exception as type_err:
                    print(f"ID {current_id} - Sual tipi seçilə bilmədi.")

                # 🛠️ 2. ÇƏTİNLİK SƏVİYYƏSİNİN SEÇİLMƏSİ (Value ilə: 0, 1, 2)
                try:
                    difficulty_val = "0"  # Default: Asan
                    csv_diff = row['Çətinlik Səviyyəsi'].strip().lower()
                    
                    if "ort" in csv_diff:
                        difficulty_val = "1"
                    elif "çət" in csv_diff or "cet" in csv_diff:
                        difficulty_val = "2"
                        
                    page.locator("#propDifficulty").select_option(value=difficulty_val)
                except Exception as diff_err:
                    print(f"ID {current_id} - Çətinlik seçilə bilmədi.")

                # 🛠️ 3. DOĞRU CAVABIN SEÇİLMƏSİ (A, B, C, D, E)
                try:
                    correct_ans = row['Doğru Cavab'].strip().upper()
                    page.locator("#propCorrectAnswerSelect").select_option(value=correct_ans)
                except Exception as ans_err:
                    print(f"ID {current_id} - Doğru cavab seçilə bilmədi.")
                # -------------------------------------------------------------
                
                # 🚀 4. TEKLİFİ GÖNDƏR (SUBMIT)
                submit_button = page.locator("#propSubmitBtn")
                if submit_button.count() > 0:
                    submit_button.click()
                    print(f"ID {current_id} - FORM SUBMIT OLUNDU")
                else:
                    print(f"ID {current_id} - Diqqət: Təsdiq düyməsi tapılmadı!")
                
                time.sleep(2.5)  # Məlumatın qeyd olunub modalın bağlanması üçün gözləmə
                
            except Exception as e:
                print(f"ID {current_id} - ERROR baş verdi.")
                try:
                    page.get_by_role("button", name="Ləğv et").click(timeout=1000)
                except:
                    pass

    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)

    print("Script tamamlandı.")