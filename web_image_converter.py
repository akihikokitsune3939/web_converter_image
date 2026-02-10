import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

# Создаем окно
root = tk.Tk()
root.title("Web Image Converter")
root.geometry("500x600")

# Переменные
image_path = None
original_image = None
quality_value = tk.IntVar(value=85)
format_value = tk.StringVar(value="JPEG")
optimize_value = tk.BooleanVar(value=True)

# Функция загрузки изображения
def load_image():
    global image_path, original_image
    
    file_path = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[
            ("Изображения", "*.png *.jpg *.jpeg *.webp *.bmp *.gif"),
            ("Все файлы", "*.*")
        ]
    )
    
    if file_path:
        try:
            image_path = file_path
            original_image = Image.open(file_path)
            
            # Обновляем информацию
            filename = os.path.basename(file_path)
            upload_label.config(text=filename[:30] + "..." if len(filename) > 30 else filename)
            
            # Показываем информацию
            info_text = f"Файл: {filename}\n"
            info_text += f"Размер: {original_image.size[0]}x{original_image.size[1]}\n"
            info_text += f"Вес: {os.path.getsize(file_path)/1024:.1f} KB"
            info_label.config(text=info_text)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

# Функция конвертации
def convert_image():
    global image_path, original_image
    
    if not image_path or not original_image:
        messagebox.showwarning("Ошибка", "Сначала загрузите изображение!")
        return
    
    try:
        # Получаем настройки
        output_format = format_value.get().lower()
        quality = quality_value.get()
        optimize = optimize_value.get()
        
        # Конвертируем для JPEG если нужно
        if output_format == "jpeg" and original_image.mode in ('RGBA', 'LA', 'P'):
            # Создаем белый фон
            background = Image.new('RGB', original_image.size, (255, 255, 255))
            if original_image.mode == 'P':
                original_image = original_image.convert('RGBA')
            background.paste(original_image, mask=original_image.split()[-1])
            image_to_convert = background
        else:
            image_to_convert = original_image
        
        # Предлагаем имя файла
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        default_name = f"{base_name}_optimized.{output_format}"
        
        # Сохраняем
        save_path = filedialog.asksaveasfilename(
            title="Сохранить как",
            initialfile=default_name,
            defaultextension=f".{output_format}",
            filetypes=[
                (f"{output_format.upper()} файлы", f"*.{output_format}"),
                ("Все файлы", "*.*")
            ]
        )
        
        if save_path:
            # Параметры сохранения
            save_kwargs = {'quality': quality, 'optimize': optimize}
            if output_format == 'webp':
                save_kwargs['method'] = 6
            
            image_to_convert.save(save_path, **save_kwargs)
            
            # Показываем результат
            original_size = os.path.getsize(image_path) / 1024
            new_size = os.path.getsize(save_path) / 1024
            
            if original_size > 0:
                compression = ((original_size - new_size) / original_size) * 100
                compression_text = f"{compression:.1f}%"
            else:
                compression_text = "N/A"
            
            messagebox.showinfo("Готово!", 
                f"Сохранено: {save_path}\n\n"
                f"Исходный: {original_size:.1f} KB\n"
                f"Новый: {new_size:.1f} KB\n"
                f"Сжатие: {compression_text}")
    
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось конвертировать: {e}")
        # Функция сброса
def reset_all():
    global image_path, original_image
    
    image_path = None
    original_image = None
    upload_label.config(text="Файл не выбран")
    info_label.config(text="")
    quality_value.set(85)
    format_value.set("JPEG")
    optimize_value.set(True)

# Создаем интерфейс
# Заголовок
title_label = tk.Label(root, text="Web Image Converter", 
                      font=("Arial", 16, "bold"))
title_label.pack(pady=20)

# Блок загрузки
load_frame = tk.LabelFrame(root, text="1. Загрузите изображение", padx=15, pady=15)
load_frame.pack(fill="x", padx=20, pady=10)

upload_label = tk.Label(load_frame, text="Файл не выбран", width=40, anchor="w")
upload_label.pack(side="left", fill="x", expand=True, padx=(0, 10))

load_btn = tk.Button(load_frame, text="Выбрать файл", command=load_image)
load_btn.pack(side="right")

# Информация
info_label = tk.Label(root, text="", justify="left")
info_label.pack(pady=10)

# Настройки
settings_frame = tk.LabelFrame(root, text="2. Настройки конвертации", padx=15, pady=15)
settings_frame.pack(fill="x", padx=20, pady=10)

# Формат
format_label = tk.Label(settings_frame, text="Формат вывода:")
format_label.grid(row=0, column=0, sticky="w", pady=5)

format_menu = tk.OptionMenu(settings_frame, format_value, "JPEG", "WebP")
format_menu.grid(row=0, column=1, sticky="w", pady=5, padx=(10, 0))

# Качество
quality_label = tk.Label(settings_frame, text="Качество (1-100):")
quality_label.grid(row=1, column=0, sticky="w", pady=5)

quality_scale = tk.Scale(settings_frame, from_=1, to=100, 
                        variable=quality_value, orient="horizontal", length=200)
quality_scale.grid(row=1, column=1, sticky="w", pady=5, padx=(10, 0))

# Оптимизация
optimize_check = tk.Checkbutton(settings_frame, text="Оптимизировать для Web",
                               variable=optimize_value)
optimize_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=10)

# Кнопки
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

convert_btn = tk.Button(button_frame, text="Конвертировать", 
                       command=convert_image, bg="blue", fg="white",
                       padx=20, pady=10)
convert_btn.pack(side="left", padx=(0, 10))

reset_btn = tk.Button(button_frame, text="Сброс", 
                     command=reset_all, bg="red", fg="white",
                     padx=20, pady=10)
reset_btn.pack(side="left")

# Подсказка
tip_label = tk.Label(root, 
                    text="Поддерживаемые форматы: PNG, JPEG, WebP, BMP, GIF",
                    font=("Arial", 9), fg="gray")
tip_label.pack(pady=10)

# Запускаем
root.mainloop()