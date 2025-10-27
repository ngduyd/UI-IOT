from nicegui import ui
from core.grpc_client import scan_ble, connect_ble
from pages.layout import base_layout

@ui.page('/devices')
async def devices_page():
    def content():
        ui.label('Quét thiết bị BLE').classes('text-h5')
        result_box = ui.column()

        async def do_scan():
            result_box.clear()
            with result_box:
                ui.label('Đang quét...')
            devices = await scan_ble()
            result_box.clear()

            for dev in devices:
                async def connect_action(dev_mac=dev['mac']):
                    resp = await connect_ble(dev_mac)
                    ui.notify(resp.message)

                with result_box:
                    with ui.row():
                        ui.label(f"{dev['name']} ({dev['mac']}) RSSI={dev['rssi']}")
                        ui.button('Kết nối', on_click=connect_action)

        ui.button('Quét thiết bị BLE', on_click=do_scan)
    
    base_layout('Cấu hình BLE', content)