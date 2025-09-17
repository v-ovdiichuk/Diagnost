# Імпортуємо необхідні бібліотеки
import customtkinter as ctk  # Для сучасного GUI.
from tkinter import messagebox  # Для спливаючих повідомлень.

# Встановлюємо тему для GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Проста "база даних" — словник з хворобами
diseases = {
    "Грип": {
        "symptoms": ["висока температура", "кашель", "біль у горлі", "втома", "головний біль"],
        "recommendations": "Відпочивайте, пийте багато рідини, зверніться до лікаря якщо симптоми тривають >3 днів."
    },
    "Застуда": {
        "symptoms": ["нежить", "кашель", "біль у горлі", "невелика температура"],
        "recommendations": "Пийте теплі напої, використовуйте спреї для носа, відпочивайте."
    },
    "Мігрень": {
        "symptoms": ["головний біль", "нудота", "чутливість до світла", "втома"],
        "recommendations": "Уникайте тригерів (стрес, шоколад), прийміть знеболювальне, лягайте в темну кімнату."
    }
}

# Функція для розрахунку ймовірності
def calculate_probability(selected_symptoms):
    results = {}  # Словник для результатів: хвороба -> відсоток
    for disease, data in diseases.items():  # Змінено 'diseases' на 'disease' у циклі
        total_symptoms = len(data["symptoms"])
        if total_symptoms == 0:
            continue
        matching = sum(1 for sym in selected_symptoms if sym in data["symptoms"])
        probability = (matching / total_symptoms) * 100
        results[disease] = probability
    return results

# Функція для показу результатів
def show_results(selected_symptoms):
    probabilities = calculate_probability(selected_symptoms)
    if not probabilities:
        messagebox.showinfo("Результат", "Немає співпадінь з хворобами.")
        return
    
    sorted_results = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    
    message = "Можливі хвороби:\n"
    for disease, prob in sorted_results:
        if prob > 0:
            rec = diseases[disease]["recommendations"]
            message += f"{disease}: {prob:.2f}% ймовірності.\nРекомендації: {rec}\n\n"
    
    if message == "Можливі хвороби:\n":
        message = "Немає значущих співпадінь."
    
    messagebox.showinfo("Результат", message)

# Головний клас для GUI
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Перевірка симптомів")
        self.geometry("400x500")
        
        # Список усіх можливих симптомів
        all_symptoms = set()
        for data in diseases.values():
            all_symptoms.update(data["symptoms"])
        self.symptoms_list = sorted(list(all_symptoms))
        
        # Лейбл
        label = ctk.CTkLabel(self, text="Виберіть симптоми:", font=("Arial", 16))
        label.pack(pady=10)
        
        # Фрейм для чекбоксів
        frame = ctk.CTkScrollableFrame(self, width=350, height=300)
        frame.pack(pady=10)
        
        self.checkboxes = {}
        for sym in self.symptoms_list:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(frame, text=sym, variable=var)
            chk.pack(anchor="w", pady=5)
            self.checkboxes[sym] = var
        
        # Кнопка для розрахунку
        button = ctk.CTkButton(self, text="Розрахувати", command=self.on_calculate)
        button.pack(pady=20)
    
    def on_calculate(self):
        selected = [sym for sym, var in self.checkboxes.items() if var.get()]
        if not selected:
            messagebox.showwarning("Попередження", "Виберіть хоча б один симптом!")
            return
        show_results(selected)

# Запуск програми
if __name__ == "__main__":
    app = App()
    app.mainloop()