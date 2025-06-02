@echo off
echo ===============================
echo  🧪 Birim Testler Çalıştırılıyor...
echo ===============================
python -m unittest testler\birim_testi.py

echo.
echo ===============================
echo  🧪 Selenium Testi Çalıştırılıyor...
echo ===============================
python testler\selenium_testi.py

pause
