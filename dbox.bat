@echo off
title Constructor de Desktop Box
echo ===========================================
echo   HORNEANDO Y LIMPIANDO (Version 3.13)
echo ===========================================

:: 1. Configuramos rutas corregidas para Python 3.13
set PATH=%PATH%;%APPDATA%\Python\Python313\Scripts;%USERPROFILE%\AppData\Local\Programs\Python\Python313\Scripts

:: 2. Limpieza inicial
if exist build rd /s /q build
if exist dist rd /s /q dist

:: 3. Conversión
echo [1/3] Convirtiendo MOTOR (engine.py)...
python -m PyInstaller --noconsole --onefile engine.py

echo [2/3] Convirtiendo GESTOR (gestor.pyw)...
python -m PyInstaller --noconsole --onefile --name dbox gestor.pyw

:: 4. Limpieza FINAL (Aquí borramos los .spec)
echo [3/3] Limpiando archivos temporales...
if exist build rd /s /q build
if exist engine.spec del /q engine.spec
if exist dbox.spec del /q dbox.spec

echo.
echo ===========================================
echo   ¡LISTO! Todo limpio con Python 3.13. 
echo   Tus archivos finales estan en 'dist'
echo ===========================================
pause
