from datetime import datetime
from pywinauto import Desktop

def url_extractor(handles, app):
    window = Desktop(backend="uia").window(handle=handles)
    url=""

    if app == "Picture in picture":
            for control in window.descendants():
                if (control.element_info.control_type == "Text"):
                    url = control.window_text().strip()
                    print(f"URL: {url}")
                    domain = url.split(".")[:-1]

    for control in window.descendants():
        if (control.element_info.control_type == "Edit"):
            url = control.window_text().strip()
            print(f"URL: {url}")
            app_name = url.split("/")[0].split(".")[-2].capitalize()
            return (url, app_name)

def browser_extractor(context, parts, handles):
    # if context["app_category"] == "Unknown":
    #     try:
    #         window = Desktop(backend="uia").window(handle=handles)
    #         url=""
    #         for control in window.descendants():
    #                 if (control.element_info.control_type == "Text"):
    #                     url = control.window_text().strip()
    #                     print(f"URL: {url}")
    #                     domain = url.split(".")[:-1]
    #     except Exception:
             
    (url, app) = url_extractor(handles, parts[-1].strip())
    if len(parts) >= 3:
        context["current_app"] = parts[-1].strip() # Get the last part as app name
        context["current_file"] = ' - '.join(parts[0:-2]).strip()  # Get the first part as file name
        context["current_project"] = parts[-2].strip()  # Get the second part as project name
    elif len(parts) == 2:
        context["current_app"] = parts[-1].strip() # Get the last part as app name
        context["current_file"] = parts[0].strip()  # Get the first part as file name
        context["current_project"] = app
    
    record  = {
        "timestamp": datetime.now().isoformat(),
        "context_type": context["context_category"],
        "app": context["current_app"], # Get the last part as app name
        "category": context["app_category"],
        "context": {
            "url": url,
            "web app": context["current_project"], # Get the first part as tab name
            "tab title": context["current_file"]
        }
    }

    return record