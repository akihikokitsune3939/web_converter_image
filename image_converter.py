"""
КОНВЕРТЕР ИЗОБРАЖЕНИЙ - ИСПРАВЛЕННАЯ ВЕРСИЯ
С поддержкой WebP и всех форматов
"""

print("=" * 50)
print("НАЧАЛО ЗАГРУЗКИ ПРОГРАММЫ")
print("=" * 50)

# Шаг 1: Проверяем импорты
try:
    import tkinter as tk
    print("✓ tkinter загружен")
    
    # Тестируем tkinter
    test_root = tk.Tk()
    test_root.withdraw()  # Скрываем тестовое окно
    print("✓ tkinter работает")
    test_root.destroy()
    
except Exception as e:
    print(f"✗ Ошибка tkinter: {e}")
    input("Нажмите Enter для выхода...")
    exit()

try:
    from tkinter import filedialog, messagebox
    print("✓ tkinter модули загружены")
except Exception as e:
    print(f"✗ Ошибка модулей tkinter: {e}")

try:
    from PIL import Image
    print("✓ Pillow загружен")
    
    # Проверяем поддержку WebP
    try:
        Image.open("test.webp")
        print("✓ WebP поддерживается")
    except:
        print("⚠ WebP может требовать обновления Pillow")
        
except ImportError as e:
    print(f"✗ Pillow не установлен! Установите: pip install pillow")
    input("Нажмите Enter для выхода...")
    exit()

import os
import time

print("=" * 50)
print("БИБЛИОТЕКИ ЗАГРУЖЕНЫ УСПЕШНО")
print("=" * 50)

# ============================================================================
# ГЛАВНОЕ ПРИЛОЖЕНИЕ
# ============================================================================
def main():
    print("\nСоздаем главное окно...")
    
    # Создаем главное окно
    root = tk.Tk()
    root.title("Image Converter 2.0")
    root.geometry("500x450")  # Немного увеличил окно
    
    # Центрируем окно на экране
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Делаем окно поверх всех
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)
    
    print("✓ Окно создано и позиционировано")
    
    # Переменные
    image_path = None
    current_image = None
    
    # ============================================================================
    # СОЗДАНИЕ ИНТЕРФЕЙСА
    # ============================================================================
    print("Создаем интерфейс...")
    
    # Заголовок
    title_frame = tk.Frame(root)
    title_frame.pack(pady=15)
    
    title_label = tk.Label(
        title_frame,
        text="🖼️ IMAGE CONVERTER PRO",
        font=("Arial", 18, "bold"),
        fg="darkblue"
    )
    title_label.pack()
    
    subtitle_label = tk.Label(
        title_frame,
        text="Convert images between formats with WebP support",
        font=("Arial", 10),
        fg="gray"
    )
    subtitle_label.pack()
    
    # Разделитель
    separator = tk.Frame(root, height=2, bg="lightgray")
    separator.pack(fill=tk.X, padx=30, pady=10)
    
    # Статус загрузки
    status_label = tk.Label(
        root,
        text="Ready to convert",
        font=("Arial", 9),
        fg="green"
    )
    status_label.pack(pady=5)
    
    # Кнопка выбора файла
    select_btn = tk.Button(
        root,
        text="📂 SELECT IMAGE",
        command=lambda: select_image(),
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#45a049",
        padx=30,
        pady=10,
        cursor="hand2"
    )
    select_btn.pack(pady=10)
    
    # Метка выбранного файла
    file_label = tk.Label(
        root,
        text="No image selected",
        font=("Arial", 10),
        fg="#666",
        bg="#f5f5f5",
        relief=tk.SUNKEN,
        width=45,
        height=2
    )
    file_label.pack(pady=10)
    
    # Фрейм форматов
    format_frame = tk.LabelFrame(root, text="Output Format", padx=15, pady=10)
    format_frame.pack(pady=10, padx=20, fill=tk.X)
    
    format_var = tk.StringVar(value="PNG")
    
    # Все поддерживаемые форматы
    formats = [
        ("PNG (Best for graphics, transparent)", "PNG"),
        ("JPEG (Best for photos)", "JPEG"),
        ("WebP (Modern format, small size)", "WebP"),
        ("BMP (Windows bitmap)", "BMP"),
        ("GIF (Animated images)", "GIF"),
        ("TIFF (High quality)", "TIFF")
    ]
    
    for text, value in formats:
        rb = tk.Radiobutton(
            format_frame,
            text=text,
            variable=format_var,
            value=value,
            font=("Arial", 9),
            anchor="w"
        )
        rb.pack(anchor="w", pady=1)
    
    # Фрейм кнопок
    button_frame = tk.Frame(root)
    button_frame.pack(pady=15)
    
    # Кнопка конвертации (изначально отключена)
    convert_btn = tk.Button(
        button_frame,
        text="🔄 CONVERT NOW",
        command=lambda: convert_image(),
        font=("Arial", 11, "bold"),
        bg="#2196F3",
        fg="white",
        padx=25,
        pady=8,
        state=tk.DISABLED
    )
    convert_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    # Кнопка выхода
    exit_btn = tk.Button(
        button_frame,
        text="🚪 EXIT",
        command=root.quit,
        font=("Arial", 11),
        bg="#f44336",
        fg="white",
        padx=20,
        pady=8
    )
    exit_btn.pack(side=tk.LEFT)
    
    # Информация
    info_label = tk.Label(
        root,
        text="Supports: PNG, JPG, JPEG, WebP, BMP, GIF, TIFF",
        font=("Arial", 8),
        fg="#888"
    )
    info_label.pack(pady=5)
    
    print("✓ Интерфейс создан")
    
    # ============================================================================
    # ФУНКЦИИ
    # ============================================================================
    def select_image():
        nonlocal image_path, current_image
        
        print("Открываем диалог выбора файла...")
        
        try:
            # Открываем диалог выбора файла с поддержкой ВСЕХ форматов
            filetypes_list = [
                ("All image files", "*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tiff *.tif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("WebP files", "*.webp"),
                ("BMP files", "*.bmp"),
                ("GIF files", "*.gif"),
                ("TIFF files", "*.tiff *.tif"),
                ("All files", "*.*")
            ]
            
            path = filedialog.askopenfilename(
                title="Select an image file",
                filetypes=filetypes_list
            )
            
            if path:
                print(f"Выбран файл: {path}")
                
                try:
                    # Пробуем открыть изображение
                    current_image = Image.open(path)
                    image_path = path
                    
                    # Обновляем интерфейс
                    filename = os.path.basename(path)
                    file_ext = os.path.splitext(filename)[1].upper()
                    short_name = filename[:25] + "..." if len(filename) > 25 else filename
                    file_label.config(
                        text=f"{short_name} [{file_ext}]",
                        fg="darkblue",
                        font=("Arial", 10, "bold")
                    )
                    
                    # Активируем кнопку конвертации
                    convert_btn.config(state=tk.NORMAL, bg="#2196F3")
                    
                    # Обновляем статус
                    status_label.config(
                        text=f"✓ Loaded: {current_image.format} image",
                        fg="green"
                    )
                    
                    # Показываем информацию
                    img_info = f"Size: {current_image.width}×{current_image.height} | Format: {current_image.format}"
                    print(f"✓ Изображение загружено: {img_info}")
                    
                    # Небольшое информационное сообщение
                    messagebox.showinfo("Image Loaded", 
                        f"✓ Image loaded successfully!\n\n"
                        f"File: {filename}\n"
                        f"Format: {current_image.format}\n"
                        f"Size: {current_image.width}×{current_image.height} px\n\n"
                        f"Ready to convert!"
                    )
                    
                except Exception as e:
                    print(f"✗ Ошибка загрузки изображения: {e}")
                    messagebox.showerror("Error", f"Cannot open image file:\n{str(e)}")
                    
        except Exception as e:
            print(f"✗ Ошибка в диалоге выбора: {e}")
            messagebox.showerror("Error", f"Cannot open file dialog:\n{str(e)}")
    
    def convert_image():
        if not image_path or not current_image:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
        
        print(f"Начинаем конвертацию {image_path}...")
        
        try:
            output_format = format_var.get()
            print(f"Целевой формат: {output_format}")
            
            # Запрашиваем место сохранения
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            default_name = f"{base_name}_converted.{output_format.lower()}"
            
            # Создаем фильтры для разных форматов
            filetypes_map = {
                "JPEG": [("JPEG files", "*.jpg;*.jpeg")],
                "PNG": [("PNG files", "*.png")],
                "WebP": [("WebP files", "*.webp")],
                "BMP": [("BMP files", "*.bmp")],
                "GIF": [("GIF files", "*.gif")],
                "TIFF": [("TIFF files", "*.tiff;*.tif")]
            }
            
            save_path = filedialog.asksaveasfilename(
                title=f"Save as {output_format}",
                initialfile=default_name,
                defaultextension=f".{output_format.lower()}",
                filetypes=filetypes_map.get(output_format, [("All files", "*.*")])
            )
            
            if save_path:
                print(f"Сохраняем в: {save_path}")
                
                try:
                    # Подготавливаем параметры для разных форматов
                    save_kwargs = {}
                    img_to_save = current_image.copy()
                    
                    if output_format == "JPEG":
                        # Для JPEG нужно убрать прозрачность
                        if img_to_save.mode in ('RGBA', 'LA', 'P'):
                            # Создаем белый фон
                            background = Image.new('RGB', img_to_save.size, (255, 255, 255))
                            if img_to_save.mode == 'P':
                                img_to_save = img_to_save.convert('RGBA')
                            background.paste(img_to_save, mask=img_to_save.split()[-1])
                            img_to_save = background
                        
                        if img_to_save.mode != 'RGB':
                            img_to_save = img_to_save.convert('RGB')
                        
                        save_kwargs = {'quality': 95, 'optimize': True}
                    
                    elif output_format == "PNG":
                        save_kwargs = {'compress_level': 6}
                    
                    elif output_format == "WebP":
                        # WebP поддерживает прозрачность
                        save_kwargs = {'quality': 90, 'method': 6}
                    
                    elif output_format == "BMP":
                        # BMP обычно без сжатия
                        if img_to_save.mode in ('RGBA', 'LA', 'P'):
                            img_to_save = img_to_save.convert('RGB')
                    
                    elif output_format == "GIF":
                        # Для GIF может потребоваться конвертация
                        if img_to_save.mode not in ('P', 'L', 'RGB', 'RGBA'):
                            img_to_save = img_to_save.convert('P', palette=Image.ADAPTIVE)
                    
                    elif output_format == "TIFF":
                        save_kwargs = {'compression': 'tiff_lzw'}
                    
                    # Сохраняем изображение
                    img_to_save.save(save_path, **save_kwargs)
                    
                    # Проверяем, что файл сохранен
                    if os.path.exists(save_path):
                        # Сравниваем размеры
                        original_size = os.path.getsize(image_path) / 1024
                        new_size = os.path.getsize(save_path) / 1024
                        
                        reduction = original_size - new_size
                        percent = (reduction / original_size) * 100 if original_size > 0 else 0
                        
                        # Формируем сообщение
                        if percent > 0:
                            size_info = f"Reduced by: {reduction:.1f} KB ({percent:.1f}%)"
                        elif percent < 0:
                            size_info = f"Increased by: {-reduction:.1f} KB ({-percent:.1f}%)"
                        else:
                            size_info = "Size unchanged"
                        
                        result_message = (
                            f"✅ CONVERSION SUCCESSFUL!\n\n"
                            f"Original: {original_size:.1f} KB ({os.path.basename(image_path)})\n"
                            f"New: {new_size:.1f} KB ({os.path.basename(save_path)})\n"
                            f"{size_info}\n\n"
                            f"Format: {output_format}\n"
                            f"Saved to:\n{os.path.dirname(save_path)}"
                        )
                        
                        messagebox.showinfo("Success", result_message)
                        
                        # Обновляем статус
                        status_label.config(
                            text=f"✓ Converted to {output_format} ({new_size:.1f} KB)",
                            fg="blue"
                        )
                        
                        print(f"✓ Конвертация успешна! Сохранено: {save_path}")
                        print(f"  Размер: {new_size:.1f} KB, Формат: {output_format}")
                    else:
                        messagebox.showerror("Error", "Failed to save file!")
                        
                except Exception as e:
                    print(f"✗ Ошибка при сохранении: {e}")
                    messagebox.showerror("Save Error", 
                        f"Failed to save image as {output_format}:\n\n{str(e)}")
                    
        except Exception as e:
            print(f"✗ Ошибка конвертации: {e}")
            messagebox.showerror("Conversion Error", 
                f"Failed to convert image:\n\n{str(e)}")
    
    # ============================================================================
    # ЗАПУСК ГЛАВНОГО ЦИКЛА
    # ============================================================================
    print("\n" + "=" * 50)
    print("ЗАПУСКАЕМ ГЛАВНЫЙ ЦИКЛ ОКНА")
    print("=" * 50)
    
    # Форсируем отображение окна
    root.deiconify()
    root.lift()
    root.focus_force()
    
    # Обновляем окно
    root.update()
    
    print("✓ Окно отображено")
    print("✓ Программа готова к работе")
    print("\nОжидание действий пользователя...")
    
    # Запускаем главный цикл
    try:
        root.mainloop()
        print("\n✓ Главный цикл завершен")
    except Exception as e:
        print(f"\n✗ Ошибка в главном цикле: {e}")
    
    print("=" * 50)
    print("ПРОГРАММА ЗАВЕРШЕНА")
    print("=" * 50)

# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================
if __name__ == "__main__":
    try:
        print("\nВызываем функцию main()...")
        main()
    except KeyboardInterrupt:
        print("\n✗ Программа прервана пользователем")
    except Exception as e:
        print(f"\n✗ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")
    
    # Задержка перед выходом
    time.sleep(0.5)
    print("\nЗавершение работы...")