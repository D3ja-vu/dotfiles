import psutil
from ignis.widgets import Widget

# Unicode bolt symbol
BOLT_SYMBOL = ""

def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return battery.percent, battery.power_plugged
    return None, None

def battery_item() -> Widget.Box:
    battery_percent, is_plugged = get_battery_info()

    if battery_percent is None:
        battery_percent = 0  # If no battery info, set to 0%
        is_plugged = False

    battery_label = Widget.Label(
        label=BOLT_SYMBOL if is_plugged else f"{int(battery_percent)}%",
        css_classes=["battery-percent"],
    )

    battery_scale = Widget.Scale(
        min=0,
        max=100,
        value=battery_percent,
        sensitive=False,
        css_classes=["battery-scale"],
    )

    box = Widget.Box(
        css_classes=["battery-item"],
        child=[battery_label, battery_scale]
    )

    def refresh():
        new_battery_percent, new_is_plugged = get_battery_info()
        battery_label.label = BOLT_SYMBOL if new_is_plugged else f"{int(new_battery_percent)}%"
        battery_scale.value = new_battery_percent
        return True

    box.setup = lambda self: GLib.timeout_add_seconds(3, lambda: refresh())  # Refresh every 3 seconds

    return box

def battery_widget() -> Widget.Box:
    return Widget.Box(
        setup=lambda self: self.append(battery_item())
    )
