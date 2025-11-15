from nicegui import ui
import uuid
from utils.jsonConfig import save_config, load_config

# Import trang config BLE
from pages import devices_page, dashboard_page, config_page, index_page

if __name__ in {"__main__", "__mp_main__"}:
    config = load_config()
    if not config.get('deviceID') or config.get('deviceID').strip() == '':
        new_device_id = str(uuid.uuid4())
        config['deviceID'] = new_device_id
        save_config(config)
    
    ui.run(
        title="Smart Classroom Control Panel",
        reload=True,          
        port=8080,             
        host="0.0.0.0",        
        show=False    
    )
