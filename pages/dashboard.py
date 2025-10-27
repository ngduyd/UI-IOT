from nicegui import ui
from pages.layout import base_layout

@ui.page('/dashboard')
def dashboard_page():
    base_layout('Dashboard', lambda: ui.label('📊 Dashboard đang phát triển...'))