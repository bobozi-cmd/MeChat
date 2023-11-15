from rich.console import RenderableType
from textual import events, binding, containers, widgets 
from textual.app import App, ComposeResult
from textual.reactive import reactive

class MeTitle(widgets.Label):
    """Title of MeChat Room"""
    DEFAULT_CSS = """
    MeTitle {
        content-align: center middle;
        text-opacity: 60%;
        width: 100%
    }
    """

class MeMessage(widgets.Label):
    """Signle message"""

    def on_mount(self) -> None:
        if type(self.parent) is MeMessageDisplay:
            self.parent.scroll_end()

class MeMessageDisplay(containers.ScrollableContainer):
    """Message Area of MeChat Room"""
    DEFAULT_CSS = """
    MeMessageDisplay {
        background: blue;
        padding: 1;
        margin: 1;
    }
    """


    def on_mount(self) -> None:
        self.scroll_end()

    def compose(self) -> ComposeResult:
        yield MeMessage("2023-11-15 bobo>\nHello World")
        yield MeMessage("2023-11-15 bobo>\nHello World2")
        yield MeMessage("2023-11-15 bobo>\nHello World3")
        yield MeMessage("2023-11-15 bobo>\nHello World4")
        yield MeMessage("2023-11-15 bobo>\nHello World5")

class MeInput(widgets.Static):
    DEFAULT_CSS = """
    MeInput {
        layout: horizontal;
    }

    #input {
        dock: left;
        width: 75%;
        height: 1;
    }

    #enter {
        dock: right;
        width: 20%;
        margin: 0 1 0 0;
    }
    """

    def compose(self) -> ComposeResult:
        self.me_inp = widgets.Input(placeholder="Please input your message here", id="input")
        self.me_inp.action_submit = self.action_submit
        self.me_btn = widgets.Button("Enter", id="enter", variant="success")
        
        yield self.me_inp
        yield self.me_btn

    def action_submit(self) -> None:
        if type(self.parent.parent) is MeChatRoom:
            self.parent.parent.on_button_pressed(widgets.Button.Pressed(self.me_btn))

class MeChatRoom(App):
    DEFAULT_CSS = """
    MeChatRoom {
        padding: 1;
    }

    #me_msg {
        height: 60%;
    }

    #me_inp {
        height: 20%;
    }
    """
    BINDINGS = [
        binding.Binding("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        self.me_inp = MeInput(id="me_inp")
        self.me_msg_display = MeMessageDisplay(id="me_msg")

        yield MeTitle("MeChat Room")
        yield self.me_msg_display
        yield self.me_inp
        yield widgets.Footer()

    def action_toggle_dark(self) -> None:
        """Actions are methods beginning with `action_`"""
        self.dark = not self.dark

    def on_button_pressed(self, event: widgets.Button.Pressed) -> None:
        content = self.me_inp.me_inp.value
        if content:
            self.me_msg_display.mount(MeMessage(content))
        self.me_inp.me_inp.clear()



if __name__ == "__main__":
    app = MeChatRoom()
    app.run()