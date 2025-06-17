@echo off
SETLOCAL

:: ========================
:: Конфигурация
:: ========================
set "VENV_DIR=venv"               :: Папка с виртуальным окружением
set "PYTHON_APP=main.py"          :: Главный файл приложения
set "PYTHON_PATH=python"          :: Команда python (или полный путь)

:: ========================
:: Проверка Python
:: ========================
%PYTHON_PATH% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не установлен или не добавлен в PATH
    pause
    exit /b 1
)

:: ========================
:: Активация окружения
:: ========================
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo [ОШИБКА] Виртуальное окружение не найдено в %VENV_DIR%
    echo Создайте его командой: %PYTHON_PATH% -m venv %VENV_DIR%
    pause
    exit /b 1
)

:: ========================
:: Запуск приложения
:: ========================
echo Запуск бота...
%PYTHON_PATH% %PYTHON_APP%

if %errorlevel% neq 0 (
    echo [ОШИБКА] Приложение завершилось с ошибкой (код: %errorlevel%)
)

:: ========================
:: Завершение
:: ========================
deactivate
pause
