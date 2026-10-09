@echo off
chcp 65001 >nul
echo === 1. Битый XML ===
python -m src.shell_emulator.main --config examples/configs/config_broken.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. Неверный корневой тег ===
python -m src.shell_emulator.main --config examples/configs/config_wrong_root.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 3. Конфиг не существует ===
python -m src.shell_emulator.main --config examples/configs/nope.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 4. Скрипт не существует ===
python -m src.shell_emulator.main --script examples/startup/nope.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 5. Ошибка внутри стартового скрипта ===
python -m src.shell_emulator.main --script examples/startup/with_error.txt
echo Код завершения: %ERRORLEVEL%