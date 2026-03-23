import flet as ft
import datetime
import hashlib
# --- ИМИТАЦИЯ БАЗЫ ДАННЫХ ---
# В реальном приложении данные заменяются на запросы к серверу (Firebase/SQL)
users = {}  # {user_id: {"name": str, "class": str, "is_admin": bool}}
admin_reports = []  # Список жалоб и фото
posts =}
]
ADMIN_HASH = "8227653c031c51859846c434f59c8a9d" 

def check_pass(e):
    # Кодируем введенный пароль и сравниваем хеши
    user_hash = hashlib.md5(pass_input.value.encode()).hexdigest()
    if user_hash == ADMIN_HASH:
        user_data["is_admin"] = True
        show_admin_panel() # Пароль, чтобы стать админом (скрытая функция)

def main(page: ft.Page):
    page.title = "подслушка"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # Состояние текущего пользователя
    user_data = {"name": "", "class": "", "is_admin": False}

    # --- ФУНКЦИИ ПЕРЕКЛЮЧЕНИЯ СТРАНИЦ ---
    def show_registration():
        page.clean()
        name_input = ft.TextField(label="Ваше имя", border_radius=15)
        class_input = ft.TextField(label="Ваш класс", border_radius=15)
        
        def register_click(e):
            if name_input.value and class_input.value:
                user_data["name"] = name_input.value
                user_data["class"] = class_input.value
                show_posts_page()
            else:
                page.snack_bar = ft.SnackBar(ft.Text("Заполните все поля!"))
                page.snack_bar.open = True
                page.update()

        page.add(
            ft.Column(, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

    def show_posts_page():
        page.clean()
        posts_list = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

        for post in posts:
            comments_col = ft.Column(])
            
            def add_comment(e, p=post):
                if e.control.value:
                    p["comments"].append(f"{user_data['name']}: {e.control.value}")
                    show_posts_page()

            posts_list.controls.append(
                ft.Container(
                    content=ft.Column(, weight="bold", size=16),
                        ft.Text(post, size=14),
                        ft.Divider(),
                        comments_col,
                        ft.TextField(label="Написать комментарий...", on_submit=add_comment, text_size=12, height=40)
                    ]),
                    padding=15, bgcolor="#f0f2f5", border_radius=15
                )
            )

        page.add(
            ft.Text("Лента постов", size=24, weight="bold"),
            posts_list,
            nav_bar()
        )

    def show_report_page():
        page.clean()
        msg_input = ft.TextField(label="Сообщение админу", multiline=True, min_lines=3)
        
        def send_report(e):
            # В Android-приложении IP обычно эмулируется или берется из сетевого интерфейса
            report = {
                "user": f"{user_data['name']} ({user_data['class']})",
                "text": msg_input.value,
                "ip": "192.168.0.1", # Имитация IP
                "time": datetime.datetime.now().strftime("%H:%M")
            }
            admin_reports.append(report)
            msg_input.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("Отправлено!"))
            page.snack_bar.open = True
            page.update()

        page.add(
            ft.Text("Связь с админом", size=24, weight="bold"),
            msg_input,
            ft.ElevatedButton("Отправить с фото и данными", icon=ft.icons.SEND, on_click=send_report),
            nav_bar()
        )

    def show_admin_panel():
        page.clean()
        if not user_data["is_admin"]:
            pass_input = ft.TextField(label="Введите секретный код", password=True)
            
            def check_pass(e):
                if pass_input.value == ADMIN_PASSWORD:
                    user_data["is_admin"] = True
                    show_admin_panel()
            
            page.add(
                ft.Text("Доступ ограничен", size=20),
                pass_input,
                ft.ElevatedButton("Войти как админ", on_click=check_pass),
                nav_bar()
            )
            return

        reports_view = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
        for r in admin_reports:
            reports_view.controls.append(
                ft.ListTile(
                    title=ft.Text(f"От: {r['user']}"),
                    subtitle=ft.Text(f"IP: {r['ip']} | {r['time']}\nТекст: {r}"),
                    is_three_line=True,
                    bgcolor="#fff4f4",
                    border_radius=10
                )
            )

        page.add(
            ft.Text("Панель администратора", size=24, weight="bold", color="red"),
            ft.Text("Другие админы скрыты", size=12, italic=True),
            reports_view,
            nav_bar()
        )

    # --- НИЖНЕЕ МЕНЮ ---
    def nav_bar():
        def on_nav_change(e):
            if e.control.selected_index == 0: show_posts_page()
            elif e.control.selected_index == 1: show_report_page()
            elif e.control.selected_index == 2: show_admin_panel()

        return ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(icon=ft.icons.HOME, label="Посты"),
                ft.NavigationDestination(icon=ft.icons.REPORT_PROBLEM, label="Жалоба"),
                ft.NavigationDestination(icon=ft.icons.ADMIN_PANEL_SETTINGS, label="Админ"),
            ],
            on_change=on_nav_change
        )

    show_registration()

ft.app(target=main)
