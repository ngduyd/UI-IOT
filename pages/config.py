import json, os
from nicegui import ui
from pages.layout import base_layout

CONFIG_PATH = 'config.json'

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"mode": "Wi-Fi", "ssid": "", "password": "", "isConfigured": False}

def save_config(data: dict):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_empty(*fields):
    return any(not f.value.strip() for f in fields)

@ui.page('/config')
def config_page():
    @ui.refreshable
    def content():
        ui.label('Cấu hình hệ thống').classes('text-h5 mb-4')

        step = {'value': 1}
        selected = {'value': 'Wi-Fi'}

        modes = [
            {'label': 'Wi-Fi', 'icon': 'wifi'},
            {'label': 'Access Point', 'icon': 'cell_tower'},
        ]

        ui.add_head_html('''
        <style>
        .radio-card {
            width: 200px;
            height: 220px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 2px solid #ccc;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            background: #fff;
        }
        .radio-card.selected {
            border-color: #2196F3;
            background: #E3F2FD;
            box-shadow: 0 0 10px rgba(33, 150, 243, 0.3);
        }
        .radio-card:hover {
            transform: scale(1.05);
        }
        .radio-icon {
            font-size: 100px;
            color: #2196F3;
        }
        .radio-label {
            font-weight: 600;
            margin-top: 10px;
            font-size: 1.1rem;
        }
        </style>
        ''')

        dialog_props = 'persistent' if not load_config().get('isConfigured', False) else ''
        with ui.dialog().props(dialog_props) as dialog, ui.card().classes('p-4 w-[600px]'):
            
            @ui.refreshable
            def dialog_content():
                if step['value'] == 1:
                    ui.label('⚙️ Chọn chế độ hoạt động').classes('text-h5 mb-4')

                    with ui.row().classes('q-gutter-xl justify-center'):
                        cards = []
                        def select_mode(mode):
                            selected['value'] = mode
                            update_highlight()
                        for m in modes:
                            with ui.card().classes('radio-card') as c:
                                ui.icon(m['icon']).classes('radio-icon')
                                ui.label(m['label']).classes('radio-label')
                                c.on('click', lambda e, mode=m['label']: select_mode(mode))
                                cards.append(c)

                        def update_highlight():
                            for card, m in zip(cards, modes):
                                if selected['value'] == m['label']:
                                    card.classes(add='selected')
                                else:
                                    card.classes(remove='selected')
                        update_highlight()

                    ui.button(
                        'Tiếp tục',
                        on_click=lambda: (
                            step.update({'value': 2}),
                            dialog_content.refresh()
                        )
                    ).classes('mt-6')

                elif step['value'] == 2:
                    if selected['value'] == 'Wi-Fi':
                        ui.label('📶 Cấu hình Wi-Fi').classes('text-h5 mb-3')
                        ssid = ui.input('Tên Wi-Fi (SSID)').props('outlined').classes('w-full mb-2')
                        password = ui.input('Mật khẩu').props('type=password outlined').classes('w-full mb-2')
                        ui.button('Thử kết nối', on_click=lambda: ui.notify('🔄 Đang thử kết nối... (chức năng mô phỏng)', color='info')).classes('mb-4')
                    else:
                        ui.label('🚩 Cấu hình Access Point').classes('text-h5 mb-3')
                        ssid = ui.input('Tên AP (SSID)').props('outlined').classes('w-full mb-2')
                        password = ui.input('Mật khẩu').props('type=password outlined').classes('w-full mb-2')

                    def on_save():
                        if is_empty(ssid, password):
                            ui.notify('⚠️ Vui lòng điền đầy đủ thông tin', color='negative')
                            return
                        save_config({
                            'mode': selected['value'],
                            'ssid': ssid.value,
                            'password': password.value,
                            'isConfigured': True
                        })
                        ui.notify('✅ Đã lưu cấu hình thành công')
                        dialog.close()
                        content.refresh()

                    ui.button(
                        'Quay lại',
                        on_click=lambda: (
                            step.update({'value': 1}),
                            dialog_content.refresh()
                        )
                    ).classes('mt-4')

                    ui.button('💾 Lưu cấu hình', on_click=on_save).classes('mt-4')

            dialog_content()

        if not load_config().get('isConfigured', False):
            ui.timer(0.3, dialog.open, once=True)
        else:
            ui.label(f"Chế độ: {load_config().get('mode', '')}").classes('mb-2')
            ui.label(f"SSID: {load_config().get('ssid', '')}").classes('mb-2')
            pwd = load_config().get('password', '')
            masked = f"{'*'*(len(pwd)-2)}{pwd[-2:]}" if len(pwd) > 2 else '*'*len(pwd)
            ui.label(f"Mật khẩu: {masked}").classes('mb-2')

            ui.button('⚙️ Cấu hình lại hệ thống', on_click=dialog.open).classes('mt-4')

    base_layout('Configuration', content)
