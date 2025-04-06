from rich.layout import Layout

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")
    layout.split_row(
        Layout(name="side", size=40),
        Layout(name="main"),
    )
    layout["main"].split_column(
        Layout(name="body", ratio=2),
        Layout(name="chatbox"),
    )
    return layout
