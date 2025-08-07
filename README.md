# **Dota 2 Panorama Editor - VPK Creator**  
**Простой инструмент для замены панорамы в Dota 2**  

[![GitHub release](https://img.shields.io/github/v/release/LincolnCox29/Dota2PanoramaEditor?include_prereleases&style=flat-square)](https://github.com/LincolnCox29/Dota2PanoramaEditor/releases)
[![Last Commit](https://img.shields.io/github/last-commit/LincolnCox29/Dota2PanoramaEditor?style=flat-square)](https://github.com/LincolnCox29/Dota2PanoramaEditor/commits/main)
[![Stars](https://img.shields.io/github/stars/LincolnCox29/Dota2PanoramaEditor?style=flat-square)](https://github.com/LincolnCox29/Dota2PanoramaEditor/stargazers)

Этот скрипт автоматизирует процесс замены видеофайлов в Dota 2, упаковывая их в VPK-архив и помещая в нужную папку игры.  

---

## **📋 Требования**  
- **Python 3.6+** ([скачать](https://www.python.org/downloads/))  
- **Steam и Dota 2** (желательно установленные в стандартной папке)  

---

## **⚙️ Установка**  
1. **Скачайте архив** с программой и распакуйте его.   
3. **Убедитесь**, что у вас установлен Python.  

---

## **🚀 Как использовать**  
1. **Запустите скрипт** (двойной клик по `Dota2PanoramaEditor.py` или через командную строку).  
2. **Введите пути**:  
   - Полный путь к вашему `.webm` файлу (например, `C:\Videos\my_video.webm`).  
   - Если скрипт не нашел путь до Steam, введите его (обычно `C:\Program Files (x86)\Steam`).
3. **Дождитесь завершения** – скрипт сам создаст VPK и переместит его в Dota 2.  

---

## **❌ Как отключить панорму**
1. **Запустите скрипт** `RestoreDefaultBackground.py` 
2. **Дождитесь завершения**

---

## **⚠️ Важно!**  
- **Закройте Dota 2 перед запуском** (иначе файлы не заменятся).  
- **Если скрипт просит права администратора** – дайте их).
- **Если вы меняли директорию Steam** - Скачайте скрипт заново, либо просто откройте файл steam_dir в тектовом редакторе и удалите его содержимое. 
- **Если что-то пошло не так** – проверьте, что:  
  - Введены правильные пути.  
  - В папке `vpk_creator` есть `vpk.exe` и `Create vpk-archive from pak01_dir folder.bat-файл`.  

---

## **❓ Частые проблемы**  
### **1. Скрипт не запускается**  
- Убедитесь, что Python установлен и добавлен в `PATH`.  
- Попробуйте запустить через командную строку:  
  ```cmd
  python Dota2PanoramaEditor.py
  ```

### **2. Ошибка "VPK tool not found"**  
- Проверьте, что `vpk.exe` лежит в папке `vpk_creator`.  

### **3. Файл не заменился в игре**  
- Убедитесь, что Dota 2 была закрыта во время работы скрипта.  

---

## **📁 Структура папок**  
```
Dota2PanoramaEditor/  
├── Dota2PanoramaEditor.py      # Скрипт для установки панорамы
├── RestoreDefaultBackground.py # Скрипт для отключения панорамы
├── utils.py                    # Файл с утилитарными функциями
├── steam_dir                   # Файл хранящий путь до Steam
└── vpk_creator/  
    ├── vpk.exe                 # Инструмент для работы с VPK
    └── Create vpk-archive from pak01_dir folder.bat  # Батник для упаковки  
```
