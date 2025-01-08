import os
import datetime
import requests

class NextTier:
    API_URL = "https://exercisedb.p.rapidapi.com/exercises"
    API_HEADERS = {
        "X-RapidAPI-Key": "SUA_CHAVE_AQUI",
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

    def __init__(self):
        self.tasks = []
        self.date = datetime.date.today()
        self.level = "E"
        self.experience = 0
        self.generate_tasks()

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
        # Retorna a tradução ou o nome original se não tiver tradução
        return translations.get(text, text)

    def show_status(self):
        """Mostra o status atual."""
        print(f"🎮 Nível Atual: {self.level}")
        print(f"💪 Experiência: {self.experience}/{self.LEVELS[self.level] if self.level != 'S' else '∞'}")

    def show_tasks(self):
        """Mostra as tarefas diárias."""
        for i, task in enumerate(self.tasks, start=1):
            status = "✅" if task["completed"] else "❌"
            print(f"{i}. {task['name']} - XP: {task['xp']} - {status}")

    def complete_task(self, task_number):
        """Marca uma tarefa como concluída."""
        if 0 < task_number <= len(self.tasks):
            task = self.tasks[task_number - 1]
            if not task["completed"]:
                task["completed"] = True
                self.experience += task["xp"]
                print(f"Tarefa '{task['name']}' concluída! Ganhou {task['xp']} XP.")
            else:
                print("Essa tarefa já foi concluída.")
        else:
            print("Número da tarefa inválido.")

    def run(self):
        """Executa o sistema."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.show_status()
            self.show_tasks()

            print("\nEscolha uma opção:")
            print("1. Completar tarefa")
            print("2. Sair")
            choice = input("> ")

            if choice == "1":
                try:
                    task_number = int(input("Digite o número da tarefa: "))
                    self.complete_task(task_number)
                except ValueError:
                    print("Entrada inválida! Tente novamente.")
            elif choice == "2":
                print("Saindo...")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    app = NextTier()
    app.run()
