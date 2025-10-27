from nicegui import ui

def base_layout(title: str, content_func):
    with ui.header().classes('bg-blue-600 text-white p-3 shadow-md fixed top-0 left-0 right-0 z-50'):
        ui.label(title).classes('text-lg font-bold')

    with ui.row().classes('w-full h-screen flex flex-col'):
        with ui.column().classes('w-1/6 bg-gray-100 p-4 overflow-y-auto h-full'):
            ui.link('🏠 Trang chủ', '/')
            ui.link('⚙️ Cấu hình', '/config')
            ui.link('🔗 Thiết bị', '/devices')
            ui.link('📊 Dashboard', '/dashboard')

        with ui.column().classes('w-5/6 p-6 overflow-y-auto h-full'):
            content_func()

    with ui.footer().classes('bg-gray-200 text-center text-gray-600 p-2 fixed bottom-0 left-0 right-0 z-40'):
        ui.label('© 2025 Smart Classroom Project')
