from win32gui import GetWindowText, GetForegroundWindow
from app_extractors.ide import ide_extractor
from app_extractors.browser import browser_extractor
from app_extractors.terminal import terminal_extractor
from app_extractors.meeting import meeting_extractor
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
    "title_category": "" # This is for categorizing the title into SYSTEM_CONTEXT, SYSTEM_NOISE, or USER_CONTEXT
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
        "File Explorer",
        "Run",
        "Task Manager"
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
    browsers = ["Google Chrome", "Mozilla Firefox", "Microsoft Edge", "Safari", "Opera", "Brave"]
    meetings = ["Zoom Meeting", "Microsoft Teams", "Google Meet", "Webex Meeting", "Skype Meeting"]
    terminals = ["Command Prompt", "PowerShell", "Terminal"]

    # Basic parsing logic to extract app name and file name based on common patterns
    if not title:
        context["current_app"] = "Unknown Application"
        context["current_file"] = ""
    
    # Categorize the title
    if " - " in title:
        if title.split(" - ")[-1].strip() in SYSTEM_CONTEXT:
            context["title_category"] = "SYSTEM_CONTEXT"
        elif title.split(" - ")[-1].strip() in SYSTEM_NOISE:
            context["title_category"] = "SYSTEM_NOISE"
        else:
            context["title_category"] = "USER_CONTEXT"
    else:
        if title in SYSTEM_CONTEXT:
            context["title_category"] = "SYSTEM_CONTEXT"
        elif title in SYSTEM_NOISE:
            context["title_category"] = "SYSTEM_NOISE"
        else:
            context["title_category"] = "USER CONTEXT"


    if " - " in title:
        parts = title.split(" - ")
        print(f"Parts:\n{parts}")
        app_name = parts[-1].strip()  # Get the last part as app name

        if app_name in ide:
            context["app_category"] = "IDE"
            record = ide_extractor(context, parts)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["file"]
            context["current_project"] = record["context"]["project"]

        elif app_name in browsers:
            context["app_category"] = "BROWSER"
            record = browser_extractor(context, parts)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["Tab Title"]
            context["current_project"] = record["context"]["Web App"]

        elif app_name in meetings:
            context["app_category"] = "MEETING"
            record = meeting_extractor(context, parts)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["meeting"]
            context["current_project"] = ""

        elif app_name in terminals:
            context["app_category"] = "TERMINAL"
            record = terminal_extractor(context, parts)
            context["current_app"] = record["app"]
            context["current_file"] = record["context"]["directory"]
            context["current_project"] = ""

    else:
        context["current_app"] = title.strip()  # Use the entire title as app name
        context["current_file"] = ""

        record  = {
            "timestamp": datetime.now().isoformat(),
            "category": context["title_category"],
            "app": context["current_app"], # Get the last part as app name
            "context": {
                "tab": context["current_file"] # Get the first part as tab name
            }
        }

    return (context, record)
