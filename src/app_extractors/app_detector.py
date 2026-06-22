import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from win32gui import GetWindowText, GetForegroundWindow
from pywinauto import Desktop
from src.app_extractors.ide import ide_extractor
from src.app_extractors.browser import browser_extractor
from src.app_extractors.terminal import terminal_extractor
from src.app_extractors.meeting import meeting_extractor
from src.app_extractors.settings import settings_extractor
from src.app_extractors.file_explorer import explorer_extractor
from datetime import datetime

context = {
    "current_app": "",
    "current_file": "",
    "current_project": "",
    "app_category": "",
    "previous_app": "",
    "previous_file": "",
    "previous_project": "",
    # Title category is not sent to LLM
    "context_category": "" # This is for categorizing the title into SYSTEM_CONTEXT, SYSTEM_NOISE, or USER_CONTEXT
}

def get_active_window_title():
    import time
    time = time.ctime()

    # Defining the category based on the title of the active window
    SYSTEM_NOISE = [
        "",
        "Task Switching",
        "Program Manager",
        "Windows Input Experience",
        "DesktopWindowXamlSource",
        "Shell Experience Host"
    ]
    SYSTEM_CONTEXT = [
        "Search",
        "Settings",
        "Control Panel",
        "Run",
        "Task Manager",
        "Device Manager",
        "Windows Security"
    ]

    # Swapping current and previous app/file before updating current app/file
    context["previous_app"] = context["current_app"]
    context["previous_file"] = context["current_file"]
    context["previous_project"] = context["current_project"]

    # Get the title of the currently active window
    handle = GetForegroundWindow()
    title = GetWindowText(handle)

    print(f"Raw window title: {title}") # For Debugging Title
    ide = ["Visual Studio Code", "PyCharm", "IntelliJ IDEA", "Eclipse", "NetBeans", "Sublime Text", "Atom", "Vim", "Emacs"]
    browsers = ["Google Chrome", "Mozilla Firefox", "Microsoft Edge", "Safari", "Opera", "Brave", "Picture in picture"]
    meetings = ["Zoom Meeting", "Microsoft Teams", "Google Meet", "Webex Meeting", "Skype Meeting"]
    terminals = ["Command Prompt", "Windows PowerShell", "Terminal"]

    # Basic parsing logic to extract app name and file name based on common patterns
    if not title:
        context["current_app"] = "Unknown Application"
        context["current_file"] = ""
    
    # Categorize the title
    if " - " in title:
        if title.split(" - ")[-1].strip() in SYSTEM_CONTEXT:
            context["context_category"] = "SYSTEM_CONTEXT"
        elif title.split(" - ")[-1].strip() in SYSTEM_NOISE:
            context["context_category"] = "SYSTEM_NOISE"
        else:
            context["context_category"] = "USER_CONTEXT"
    else:
        if title in SYSTEM_CONTEXT:
            context["context_category"] = "SYSTEM_CONTEXT"
        elif title in SYSTEM_NOISE:
            context["context_category"] = "SYSTEM_NOISE"
        else:
            context["context_category"] = "USER_CONTEXT"


    if " - " in title:
        parts = title.split(" - ")
        print(f"Parts:\n{parts}")
        app_name = parts[-1].strip()  # Get the last part as app name

        # IDE
        if app_name in ide:
            context["app_category"] = "IDE"
            record = ide_extractor(context, parts)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["file"]
            context["current_project"] = record["context"]["project"]

        # BROWSER
        elif app_name in browsers:
            context["app_category"] = "BROWSER"
            record = browser_extractor(context, parts, handle)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["tab_title"]
            context["current_project"] = record["context"]["web_app"]

        # MEETING
        elif app_name in meetings:
            context["app_category"] = "MEETING"
            record = meeting_extractor(context, parts)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["meeting"]
            context["current_project"] = ""

        # FILE EXPLORER
        elif app_name == "File Explorer":
            context["app_category"] = "FILE EXPLORER"
            record = explorer_extractor(context, parts)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["directory"]
            context["current_project"] = record["context"]["tab_title"]
        
        else:
            context["app_category"] = "UNKNOWN"
            context["current_app"] = app_name
            context["current_file"] = title
            context["current_project"] = ""

            try:
                window = Desktop(backend="uia").window(handle=handle)
                url=""
                for control in window.descendants():
                    if (control.element_info.control_type == "Text"):
                        url = control.window_text().strip()
                        print(f"URL:{url}")
                        app = url.split(".")[-2].capitalize()
                        context["app_category"] = "BROWSER"
                        context["current_app"] = "Picture in Picture"
                        context["current_file"] = handle

                        record  = {
                            "timestamp": datetime.now().isoformat(),
                            "context_type": context["context_category"],
                            "app": context["current_app"], # Get the last part as app name
                            "category": context["app_category"],
                            "context": {
                                "url": url,
                                "web_app": app,
                                "tab_title": context["current_file"] # Get the first part as tab name
                            }
                        }
                        break
                return (context, record)
            
            except Exception:
                pass

            record = {
                "timestamp": datetime.now().isoformat(),
                "context_type": context["context_category"],
                "app": context["current_app"],
                "category": context["app_category"],
                "context": {
                    "title": title
                }
            }

    else:

        # SETTING
        if title == "Settings":
            context["app_category"] = "SETTINGS"
            record = settings_extractor(context)
            context ["current_app"] = record["app"]
            context["current_file"] = record["context"]["section_path"]
            context["current_project"] = ""

        # TERMINAL
        elif title in terminals:
            context["app_category"] = "TERMINAL"
            record = terminal_extractor(context)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["directory"]
            context["current_project"] = ""
        
        else:
            try:
                window = Desktop(backend="uia").window(handle=handle)
                url=""
                for control in window.descendants():
                    if (control.element_info.control_type == "Text"):
                        url = control.window_text().strip()
                        print(f"URL:{url}") # Debug printing
                        app = url.split(".")[-2].capitalize()
                        context["app_category"] = "BROWSER"
                        context["current_app"] = "Picture in Picture"
                        context["current_file"] = handle

                        record  = {
                            "timestamp": datetime.now().isoformat(),
                            "context_type": context["context_category"],
                            "app": context["current_app"], # Get the last part as app name
                            "category": context["app_category"],
                            "context": {
                                "url": url,
                                "web_app": app,
                                "tab_title": context["current_file"] # Get the first part as tab name
                            }
                        }
            
            except Exception:
                context["current_app"] = title.strip()  # Use the entire title as app name
                context["current_file"] = ""

                record  = {
                    "timestamp": datetime.now().isoformat(),
                    "context_type": context["context_category"],
                    "app": context["current_app"], # Get the last part as app name
                    "category": "Unknown",
                    "context": {
                        "tab": context["current_file"] # Get the first part as tab name
                    }
                }

    return (context, record)
