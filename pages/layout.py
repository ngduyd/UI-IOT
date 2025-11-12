from nicegui import ui

def base_layout(title: str, content_func):
    # Header
    with ui.header().classes(
        'bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 '
        'shadow-lg flex justify-between items-center fixed top-0 left-0 right-0 z-50'
    ):
        ui.label(title).classes('text-xl font-semibold tracking-wide')
        with ui.row().classes('items-center gap-4'):
            ui.icon('notifications').classes('cursor-pointer hover:text-yellow-300')
            ui.avatar('https://cdn-icons-png.flaticon.com/512/3135/3135715.png').classes('w-8 h-8')

    # Main layout
    with ui.row().classes('w-full h-screen'):  # chừa khoảng cho header
        # Sidebar
        with ui.column().classes(
            'w-1/6 min-w-[220px] bg-gray-50 border-r border-gray-200 '
            'p-4 h-full shadow-inner'
        ):
            ui.label('📘 Smart Classroom').classes('text-gray-700 text-lg font-semibold mb-4')
            menu_items = [
                ('🏠 Trang chủ', '/'),
                ('⚙️ Cấu hình', '/config'),
                ('🔗 Thiết bị', '/devices'),
                ('📊 Dashboard', '/dashboard'),
            ]
            for icon, link in menu_items:
                with ui.link(target=link).classes(
                    'block py-2.5 px-3 rounded-lg text-gray-700 font-medium '
                    'hover:bg-blue-100 hover:text-blue-700 transition-colors duration-150'
                ):
                    ui.label(icon)

            # ui.separator()
            # ui.label('Hệ thống').classes('text-gray-500 text-sm mt-2 mb-1')
            # ui.link('🧠 Giám sát', '/monitor').classes(
            #     'block py-2.5 px-3 rounded-lg text-gray-700 hover:bg-blue-100 hover:text-blue-700'
            # )

        # Main content area
        with ui.column().classes('flex-1 p-6 overflow-y-auto bg-white'):
            # with ui.card().classes('shadow-md rounded-xl p-6 border border-gray-200'):
            content_func()

    # Footer
    with ui.footer().classes(
        'bg-gray-100 text-center text-gray-600 py-2 fixed bottom-0 left-0 right-0 '
        'border-t border-gray-200 z-40 text-sm'
    ):
        ui.label('© 2025 Smart Classroom Project · Designed by DuyN')
