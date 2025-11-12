from nicegui import ui
from pages.layout import base_layout

@ui.page('/')
def index_page():
    base_layout('Smart Classroom', lambda: ui.label('Welcome to Smart Classroom IoT System!'))