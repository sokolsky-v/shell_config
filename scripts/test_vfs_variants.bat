@echo off
chcp 65001 >nul
set PYTHONUTF8=1
echo === 1. Минимальная VFS (пустая) ===
python -m src.shell_emulator.main --vfs examples/vfs/minimal.xml --script examples/startup/info.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 2. Несколько файлов (включая двоичный в base64) ===
python -m src.shell_emulator.main --vfs examples/vfs/files.xml --script examples/startup/info.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 3. Три и более уровня вложенности ===
python -m src.shell_emulator.main --vfs examples/vfs/deep.xml --script examples/startup/info.txt
echo Код завершения: %ERRORLEVEL%
echo.
echo === 4. VFS не задана: пустая VFS по умолчанию ===
python -m src.shell_emulator.main --script examples/startup/info.txt
echo Код завершения: %ERRORLEVEL%