from nicegui import ui
import asyncio

# Import trang config BLE
from pages import devices_page, dashboard_page, config_page, index_page

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="Smart Classroom Control Panel",
        reload=True,          
        port=8080,             
        host="0.0.0.0",        
        show=False    
    )
