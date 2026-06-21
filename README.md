# 📌 Sualcavab Admin Automation

This script automates updating questions in the **sualcavab.com** admin panel via Playwright using a CSV file (`suallar.csv`).
⚠️⚠️⚠️Since platform is not mine I can't share my password but here is the video:


https://github.com/user-attachments/assets/145a217b-56c9-4006-a8bd-27cf84f82db1




## 🚀 Features
- Automatic admin login.
- Reads updates from a CSV file.
- Searches questions by ID, opens the edit modal, and updates text, choices (A–E), type, difficulty, and the correct answer.
- Auto-submits changes with basic error handling.

## 🛠️ Tech Stack
- Python 3
- Playwright (Sync API)
- CSV Module

## ⚙️ Quick Start

1. **Install dependencies:**
   ```bash
   pip install playwright
   playwright install
   ```
2. **Configure login** inside `script.py`:
   ```python
   page.get_by_role("textbox", name=" İstifadəçi adı").fill("YOUR_USERNAME")
   page.get_by_role("textbox", name=" Parol").fill("YOUR_PASSWORD")
   ```
3. **Run the script:**
   ```bash
   python script.py
   ```

## 📊 CSV Format (Delimiter: `;`)
`ID;Sual;A;B;C;D;E;Sual Tipi;Çətinlik Səviyyəsi;Doğru Cavab`

*Example:*  
`101;What is 2+2?;3;4;5;6;;Çox seçimli;Asan;B`

## 🧠 System Mappings
- **Type:** çox/cox ➔ 1 | açıq/aciq ➔ 2 | doğru/səhv ➔ 3 | səbəb/nəticə ➔ 4 | boşluq ➔ 5 | kombinasiya ➔ 6
- **Difficulty:** asan ➔ 0 | orta ➔ 1 | çətin ➔ 2

⚠️ **Note:** Runs in UI mode (`headless=False`). Missing IDs are automatically skipped to ensure continuous operation.
