import flet as ft
import json

# Funções de persistência
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main(page: ft.Page):
    # Configura a página
    page.title = "Gerenciador de Tarefas"
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Inicializa o tema e tarefas
    dark_theme = False
    tasks = load_tasks()
    completed_tasks = set()  # Usando um conjunto para armazenar tarefas concluídas

    def add_task(e):
        task_name = task_input.value
        if task_name:
            tasks.append(task_name)
            save_tasks(tasks)  # Salva a tarefa no arquivo JSON
            update_task_list()  # Atualiza a lista de tarefas na interface
            task_input.value = ""
            page.update()

    def toggle_theme(e):
        nonlocal dark_theme
        dark_theme = not dark_theme
        page.theme_mode = ft.ThemeMode.DARK if dark_theme else ft.ThemeMode.LIGHT
        theme_icon.icon = ft.icons.NIGHTLIGHT if dark_theme else ft.icons.WB_SUNNY
        page.update()

    def remove_completed_tasks(e):
        nonlocal tasks
        # Filtra tarefas não concluídas
        tasks = [task for task in tasks if task not in completed_tasks]
        completed_tasks.clear()  # Limpa as tarefas concluídas
        save_tasks(tasks)  # Salva as tarefas restantes
        update_task_list()  # Atualiza a lista de tarefas na interface

    def mark_completed(e):
        checkbox = e.control
        if checkbox.value:
            completed_tasks.add(checkbox.label)  # Adiciona a tarefa ao conjunto de concluídas
        else:
            completed_tasks.discard(checkbox.label)  # Remove do conjunto se desmarcada

    def update_task_list():
        tasks_list.controls.clear()  # Limpa a lista atual
        for task in tasks:
            checkbox = ft.Checkbox(label=task, on_change=mark_completed)
            tasks_list.controls.append(checkbox)
        page.update()  # Atualiza a interface

    # Cabeçalho
    theme_icon = ft.IconButton(ft.icons.WB_SUNNY, on_click=toggle_theme)
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.MENU, size=32),
                    ft.Text("Gerenciador de Tarefas", size=24, weight="bold", expand=True),
                    ft.IconButton(ft.icons.NOTIFICATIONS),
                    theme_icon
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.all(20)
        )
    )
    
    # Barra de Pesquisa
    search_bar = ft.TextField(label="Pesquisar Tarefa", width=500)
    task_input = ft.TextField(label="Nova Tarefa", width=400, on_submit=add_task)  # Adiciona atalho de adicionar tarefa ao dar enter
    
    page.add(
        ft.Container(
            content=ft.Row(
                [search_bar],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.only(bottom=20)
        )
    )
    
    # Adicionar Tarefa
    task_input = ft.TextField(label="Nova Tarefa", width=400)
    add_task_button = ft.IconButton(ft.icons.ADD, on_click=add_task)
    
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    task_input,
                    add_task_button
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=ft.padding.only(bottom=20)
        )
    )
    
    # Lista de Tarefas
    tasks_list = ft.Column()
    update_task_list()  # Inicializa a lista de tarefas

    # Controles de Remoção
    remove_completed_button = ft.IconButton(ft.icons.DELETE, on_click=remove_completed_tasks)
    
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    tasks_list,
                    remove_completed_button
                ]
            ),
            padding=ft.padding.all(20)
        )
    )

# Executa o aplicativo
ft.app(target=main)
