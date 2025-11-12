from nicegui import ui
from pages.layout import base_layout
from core.database import get_all_sensors, get_sensor_data
import asyncio

@ui.page('/dashboard')
def dashboard_page():
    def content():
        ui.label('Xem dữ liệu cảm biến').classes('text-h5')

        async def load_data():
            """Fetches and displays sensor data based on user selection."""
            if not sensor_select.value or not limit_select.value:
                ui.notify('Vui lòng chọn sensor và số lượng dữ liệu!', color='negative')
                return

            sensor_id = sensor_select.value
            limit = limit_select.value
            
            notification = ui.notification(timeout=None)
            notification.message = f'Đang tải {limit} điểm dữ liệu...'
            notification.spinner = True
            
            loop = asyncio.get_running_loop()
            data = await loop.run_in_executor(None, get_sensor_data, sensor_id, limit)

            table_container.clear()
            with table_container:
                if not data:
                    notification.message = 'Không có dữ liệu cho sensor này.'
                    notification.spinner = False
                    notification.timeout = 5
                    return

                all_keys = set().union(*(d.keys() for d in data))
                sorted_keys = sorted(list(all_keys))
                if 'timestamp' in sorted_keys:
                    sorted_keys.remove('timestamp')
                    sorted_keys.append('timestamp')

                column_defs = [
                    {
                        'headerName': key.capitalize().replace('_', ' '),
                        'field': key,
                        'sortable': True,
                        'filter': True,
                        'resizable': True,
                    }
                    for key in sorted_keys
                ]

                ui.aggrid({
                    'columnDefs': column_defs,
                    'rowData': data,
                    'defaultColDef': {
                        'sortable': True,
                        'filter': True,
                        'resizable': True,
                    },
                    # 'pagination': True,
                    # 'paginationAutoPageSize': True,
                }).classes('w-full h-96')

            notification.message = 'Tải dữ liệu thành công!'
            notification.spinner = False
            notification.timeout = 5

        # --- UI Elements for selection ---
        sensors = get_all_sensors()
        if not sensors:
            ui.label("Không có sensor nào trong hệ thống. Vui lòng thêm sensor ở trang 'Devices'.").classes('text-warning')
            return
            
        sensor_map = {s['sensor_id']: s['name'] for s in sensors}
        limit_options = [360, 500, 1000, 5000, 8640]

        with ui.row().classes('w-full items-center gap-4 pt-4'):
            sensor_select = ui.select(sensor_map, label='Chọn Sensor').classes('grow').props('outlined dense')
            limit_select = ui.select(limit_options, label='Số lượng dữ liệu', value=360).classes('grow').props('outlined dense')
            ui.button('Xem dữ liệu', on_click=load_data).props('color=primary')

        # Container for the table, defined after the controls
        table_container = ui.column().classes('w-full')

    base_layout('Dashboard', content)