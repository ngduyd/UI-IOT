from nicegui import ui
from core.grpc_client import scan_ble, connect_ble
from pages.layout import base_layout
from core.database import add_sensor, get_all_sensors
from core.mqtt_client import publish_message_cmd
import asyncio

@ui.page('/devices')
async def devices_page():
    def content():
        """Main content for the devices page."""
        
        ui.label('Danh sách cảm biến').classes('text-h5')

        async def update_status_sensor(sensor_id: int, status: str):
            """Updates the status of a sensor in the database."""
            if publish_message_cmd(sensor_id, status):
                ui.notify("Cập nhật trạng thái thành công", color="positive")
            else:
                ui.notify("Cập nhật trạng thái thất bại", color="negative")

            await refresh_devices()
                

        async def refresh_devices():
            """Clears and reloads the grid with sensors from the database."""
            device_grid.clear()
            sensors = get_all_sensors()
            with device_grid:
                if not sensors:
                    ui.label('Không có cảm biến nào trong hệ thống.')
                    return
                
                for sensor in sensors:
                    with ui.card():
                        ui.label(sensor['name']).classes('text-semibold')
                        ui.label(f"Trạng thái: {sensor.get('status', 'N/A')}").classes('text-xs')
                        ui.label(f"Pin: {sensor.get('vbat', 'N/A')}").classes('text-xs')
                        ui.label(f"Cập nhật: {sensor['updated_at'].strftime('%Y-%m-%d %H:%M:%S')}").classes('text-xs')
                        with ui.card_actions():
                            if sensor.get('status') == 'online':
                                ui.button('Ngắt kết nối', on_click=lambda s=sensor: update_status_sensor(s['name'], 'offline')).props('flat dense color=red')
                            else:
                                ui.button('Kết nối', on_click=lambda s=sensor: update_status_sensor(s['name'], 'online')).props('flat dense color=green')
                            ui.button('Xóa', on_click=lambda s=sensor: update_status_sensor(s['name'], 'disconnect')).props('flat dense color=red')

        async def open_add_device_dialog():
            """Opens a dialog to scan and add a new BLE device."""
            scanned_devices_list = []
            
            with ui.dialog() as dialog, ui.card().style('min-width: 500px'):
                ui.label('Thêm cảm biến mới').classes('text-h5')
                
                scan_results_container = ui.column().classes('w-full')
                device_radio = ui.radio([], value=None)
                
                async def do_scan():
                    nonlocal scanned_devices_list
                    scanned_devices_list.clear()
                    device_radio.clear()
                    scan_results_container.clear()
                    
                    with scan_results_container:
                        with ui.row().classes('items-center'):
                            ui.spinner()
                            ui.label('Đang quét các thiết bị BLE...')
                    
                    devices = await scan_ble()
                    scanned_devices_list = devices
                    scan_results_container.clear()
                    
                    if not devices:
                        with scan_results_container:
                            ui.label('Không tìm thấy thiết bị nào.')
                        return

                    device_map = {dev['mac']: f"{dev['name']} ({dev['mac']}) | RSSI: {dev['rssi']}" for dev in devices}
                    device_radio.options = device_map
                    device_radio.update()

                async def connect_and_add():
                    """Connects to the selected device and adds it to the database."""
                    selected_mac = device_radio.value
                    if not selected_mac:
                        ui.notify('Vui lòng chọn một thiết bị.', color='negative')
                        return

                    device_to_add = next((dev for dev in scanned_devices_list if dev['mac'] == selected_mac), None)
                    if not device_to_add:
                        ui.notify('Lỗi: Không tìm thấy thông tin thiết bị.', color='negative')
                        return

                    device_name = device_to_add['name']
                    ui.notify(f'Đang kết nối tới {device_name}...', color='info')

                    try:
                        # We assume connect_ble is for establishing connection.
                        # The user can add more logic based on the response if needed.
                        await connect_ble(selected_mac)
                        
                        if add_sensor(device_name):
                            ui.notify(f'✅ Đã thêm cảm biến "{device_name}" thành công!', color='positive')
                            refresh_devices()
                            dialog.close()
                        else:
                            # This might happen if the sensor already exists or DB error
                            ui.notify(f'⚠️ Không thể thêm cảm biến "{device_name}". Có thể đã tồn tại.', color='warning')
                    
                    except Exception as e:
                        ui.notify(f'❌ Lỗi khi kết nối hoặc thêm thiết bị: {e}', color='negative')

                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Quét', on_click=do_scan, icon='search')
                    ui.button('Kết nối & Thêm', on_click=connect_and_add, icon='add_link')
                    ui.button('Hủy', on_click=dialog.close, color='grey').props('flat')
            
            await dialog

        # Page layout
        with ui.row():
            ui.button('Thêm cảm biến', on_click=open_add_device_dialog).props('icon=add')

        # Container for the grid of sensor cards
        device_grid = ui.grid(columns=3).classes('gap-4 mt-4')

        # Initial load of devices
        asyncio.create_task(refresh_devices())

    base_layout('Quản lý Cảm biến', content)
