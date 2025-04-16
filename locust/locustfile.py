from locust import HttpUser, task, between
import uuid
import random

class ReaderAPI(HttpUser):
    wait_time = between(1, 5)  # Время ожидания между запросами (в секундах)

    # Получение списка всех читателей
    @task(3)  # Этот запрос будет выполняться чаще (вес = 3)
    def get_readers(self):
        self.client.get("/")

    # Получение читателя по UUID
    @task(2)
    def get_reader(self):
        reader_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"  # Замените на реальный UUID существующего читателя
        self.client.get(f"/{reader_id}", name="/[reader_id]")

    # Создание нового читателя
    @task(1)
    def create_reader(self):
        new_reader = {
            "name": f"Test Reader {random.randint(1, 1000)}",
            "has_books": random.choice([True, False])
        }
        self.client.post("/", json=new_reader)

    # Обновление данных читателя
    @task(1)
    def update_reader(self):
        reader_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"  # Замените на реальный UUID существующего читателя
        updated_data = {
            "name": f"Updated Reader {random.randint(1, 1000)}",
            "has_books": random.choice([True, False])
        }
        self.client.put(f"/{reader_id}", json=updated_data, name="/[reader_id]")

    # Формирование отчета
    @task(2)
    def get_report(self):
        self.client.get("/reports/report", name="/reports/report")

    # Получение файла отчета
    @task(1)
    def get_report_file(self):
        report_id = "report_9c90257e-e482-4574-a892-4de7bb122473.json"  # Замените на реальный ID отчета
        self.client.get(f"/reports/report_file/{report_id}", name="/reports/report_file/[report_id]")