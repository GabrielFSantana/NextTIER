import os
import requests
import datetime
import tkinter as tk
from tkinter import messagebox

class NextTier:
    API_URL = "https://exercisedb.p.rapidapi.com/exercises"
    API_HEADERS = {
        "X-RapidAPI-Key": "5face91d51msh8dd0e2cd75f71d4p1a8b67jsnba852f929a59",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    LEVELS = {
        "E": 0,
        "D": 100,
        "C": 300,
        "B": 600,
        "A": 1000,
        "S": 1500
    }

    def __init__(self, root):
        self.root = root
        self.root.title("NextTier - Sistema de Tarefas")
        
        self.tasks = []
        self.date = datetime.date.today()
        self.level = "E"
        self.experience = 0
        self.generate_tasks()

        # Interface Gráfica
        self.level_label = tk.Label(self.root, text=f"🎮 Nível: {self.level}", font=("Arial", 16))
        self.level_label.pack(pady=10)

        self.experience_label = tk.Label(self.root, text=f"💪 XP: {self.experience}/{self.LEVELS.get(self.level, '∞')}", font=("Arial", 12))
        self.experience_label.pack(pady=10)

        self.tasks_listbox = tk.Listbox(self.root, height=10, width=50, font=("Arial", 12))
        self.tasks_listbox.pack(pady=10)

        self.complete_button = tk.Button(self.root, text="Completar Tarefa", font=("Arial", 12), command=self.complete_task_gui)
        self.complete_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Sair", font=("Arial", 12), command=self.root.quit)
        self.quit_button.pack(pady=10)

        self.update_tasks_display()

    def fetch_exercises(self):
        """Busca exercícios da API."""
        response = requests.get(self.API_URL, headers=self.API_HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            print("Erro ao buscar exercícios da API.")
            return []

    def generate_tasks(self):
        """Gera tarefas baseadas no nível atual."""
        exercises = self.fetch_exercises()
        if exercises:
            self.tasks = [
                {"name": f"{self.translate(exercise['name'])} - {exercise['target']}", "xp": 10, "completed": False}
                for exercise in exercises[:3]
            ]
        else:
            self.tasks = [
                {"name": "Complete 10 agachamentos", "xp": 10, "completed": False},
                {"name": "Leia por 30 minutos", "xp": 15, "completed": False},
                {"name": "Beba 1 litro de água", "xp": 5, "completed": False},
            ]

    def translate(self, text):
        """Função simples para traduzir os nomes dos exercícios."""
        translations = {
            "Push-up": "Flexão",
            "Pull-up": "Barra fixa",
            "Squat": "Agachamento",
            "Running": "Corrida",
            "Plank": "Prancha",
            "Jumping Jacks": "Polichinelos",
            "Crunch": "Abdominal",
            "Lunges": "Afundo",
            "Burpee": "Burpee",
            "High Knees": "Joelho alto",
            "Mountain Climber": "Escalador",
            "Leg Raise": "Elevação de pernas",
            "Tricep Dips": "Mergulho para tríceps"
        }
        return translations.get(text, text)

    def level_up(self):
        """Calcula o nível com base na experiência acumulada."""
        for level, xp in reversed(sorted(self.LEVELS.items(), key=lambda x: x[1])):
            if self.experience >= xp:
                self.level = level
                break

    def update_tasks_display(self):
        """Atualiza a lista de tarefas na interface gráfica."""
        self.tasks_listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks, start=1):
            status = "✅" if task["completed"] else "❌"
            self.tasks_listbox.insert(tk.END, f"{i}. {task['name']} - XP: {task['xp']} - {status}")

        self.level_label.config(text=f"🎮 Nível: {self.level}")
        self.experience_label.config(text=f"💪 XP: {self.experience}/{self.LEVELS.get(self.level, '∞')}")

    def complete_task(self, task_number):
        """Marca uma tarefa como concluída e atualiza a experiência e o nível."""
        if 0 < task_number <= len(self.tasks):
            task = self.tasks[task_number - 1]
            if not task["completed"]:
                task["completed"] = True
                self.experience += task["xp"]
                self.level_up()
                messagebox.showinfo("Tarefa Concluída", f"Tarefa '{task['name']}' concluída! Ganhou {task['xp']} XP.")
            else:
                messagebox.showwarning("Tarefa Já Concluída", "Essa tarefa já foi concluída.")
        else:
            messagebox.showerror("Erro", "Número da tarefa inválido.")

    def complete_task_gui(self):
        """Obtém o número da tarefa selecionada na interface gráfica."""
        try:
            task_number = int(self.tasks_listbox.curselection()[0]) + 1
            self.complete_task(task_number)
            self.update_tasks_display()
        except IndexError:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma tarefa.")

# Função principal para rodar o sistema com Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = NextTier(root)
    root.mainloop()
