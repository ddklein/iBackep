import flet as ft
from ui import App

version = ""

def main(page: ft.Page):

    page.title = "iBackep"
    page.vertical_alignment = "center"
    page.theme_mode = "system"

    #App title and version
    app_name = ft.Row([ft.Text("iBackep", size = 56), ft.Text(version, size = 12)], alignment="center")
    page.add(app_name)
    
    ibackep = App()
    
    page.add(ibackep)
    

ft.app(target=main)