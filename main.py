import webview
import os
import sys
import threading

def get_html_path():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'index.html')

def main():
    html_path = get_html_path()
    window = webview.create_window(
        'CodeCraft',
        url=html_path,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True,
        confirm_close=True,
        text_selectable=True,
    )
    webview.start(debug=False)

if __name__ == '__main__':
    main()
