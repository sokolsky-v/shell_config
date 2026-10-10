@echo off
chcp 65001 >nul
set PYTHONUTF8=1
echo === 1. XML-файл VFS не существует ===
python -m src.shell_emulator.main --vfs examples/vfs/nope.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. Битый XML ===
python -m src.shell_emulator.main --vfs examples/vfs/broken.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 3. Неверный корневой тег ===
python -m src.shell_emulator.main --vfs examples/vfs/wrong_root.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 4. Некорректный base64 ===
python -m src.shell_emulator.main --vfs examples/vfs/bad_base64.xml
echo Код завершения: %ERRORLEVEL%
echo.
echo === 5. Повторяющиеся имена ===
python -m src.shell_emulator.main --vfs examples/vfs/duplicate.xml
echo Код завершения: %ERRORLEVEL%