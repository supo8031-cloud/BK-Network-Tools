from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from threading import Thread
import socket
import urllib.request
import time

Window.clearcolor = (0.025, 0.035, 0.07, 1)

CYAN = (0.0, 0.85, 1.0, 1)
GREEN = (0.2, 1.0, 0.55, 1)
DARK = (0.05, 0.09, 0.15, 1)

class NetworkApp(App):
def build(self):
self.title = "BK Network Tools"
root = BoxLayout(
orientation="vertical",
padding=18,
spacing=12
)

    root.add_widget(Label(
        text="[b]BK NETWORK TOOLS[/b]",
        markup=True,
        font_size="25sp",
        color=CYAN,
        size_hint_y=None,
        height=65
    ))

    root.add_widget(Label(
        text="NETWORK DIAGNOSTICS",
        color=GREEN,
        font_size="13sp",
        size_hint_y=None,
        height=30
    ))

    self.host = TextInput(
        hint_text="Enter domain e.g. google.com",
        multiline=False,
        size_hint_y=None,
        height=52,
        background_color=DARK,
        foreground_color=(1, 1, 1, 1),
        cursor_color=CYAN
    )
    root.add_widget(self.host)

    for label, action in [
        ("01  •  DNS LOOKUP", self.dns_check),
        ("02  •  WEBSITE CHECK", self.web_check),
        ("03  •  PUBLIC IP", self.public_ip),
    ]:
        btn = Button(
            text=label,
            size_hint_y=None,
            height=55,
            background_normal="",
            background_color=(0.03, 0.20, 0.30, 1),
            color=CYAN,
            font_size="16sp"
        )
        btn.bind(on_press=action)
        root.add_widget(btn)

    self.output = Label(
        text="READY\nChoose a network test above.",
        color=GREEN,
        halign="left",
        valign="top"
    )
    self.output.bind(size=self.output.setter("text_size"))
    root.add_widget(self.output)

    root.add_widget(Label(
        text="BK • ANDROID NETWORK UTILITY",
        color=CYAN,
        font_size="11sp",
        size_hint_y=None,
        height=28
    ))
    return root

def show_result(self, text):
    self.output.text = text

def dns_check(self, instance):
    host = self.host.text.strip()
    if not host:
        self.show_result("Enter a domain first.")
        return
    self.show_result("Checking DNS...")
    def work():
        try:
            result = socket.getaddrinfo(host, None)
            addresses = sorted(set(x[4][0] for x in result))
            self.show_result("DNS LOOKUP: OK\n\n" + "\n".join(addresses[:8]))
        except Exception as e:
            self.show_result("DNS ERROR\n" + str(e))
    Thread(target=work, daemon=True).start()

def web_check(self, instance):
    host = self.host.text.strip()
    if not host:
        self.show_result("Enter a domain first.")
        return
    if not host.startswith(("http://", "https://")):
        host = "https://" + host
    self.show_result("Checking website...")
    def work():
        start = time.time()
        try:
            req = urllib.request.Request(
                host, headers={"User-Agent": "BKNetworkTools/1.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
            ms = int((time.time() - start) * 1000)
            self.show_result(
                "WEBSITE CHECK: OK\n\nHTTP Status: "
                + str(status) + "\nResponse: " + str(ms) + " ms"
            )
        except Exception as e:
            self.show_result("WEBSITE ERROR\n" + str(e))
    Thread(target=work, daemon=True).start()

def public_ip(self, instance):
    self.show_result("Checking public IP...")
    def work():
        try:
            with urllib.request.urlopen(
                "https://api.ipify.org", timeout=10
            ) as response:
                ip = response.read().decode().strip()
            self.show_result("PUBLIC IP\n\n" + ip)
        except Exception as e:
            self.show_result("IP ERROR\n" + str(e))
    Thread(target=work, daemon=True).start()

NetworkApp().run()
