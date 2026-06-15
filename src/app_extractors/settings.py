from pywinauto import Desktop
from datetime import datetime

def settings_extractor(context):
    try:
        settings = Desktop(backend="uia").window(title="Settings")

        breadcrumb = settings.child_window(
            auto_id = "PermanentNavigationViewBreadcrumbBar"
        )
    
        path = []
        for child in breadcrumb.children():
            text = child.window_text().strip()
            if text:
                path.append(text)

        # Context
        context["current_app"] = "Settings"
        context["current_file"] = path
        context["current_project"] = ""

        # Record creation
        record = {
            "timestamp": datetime.now().isoformat(),
            "context_type": context["context_category"],
            "app": context["current_app"],
            "category": context["app_category"],
            "context": {
                "section_path": context["current_file"]
            }
        }

        return record
    
    except Exception:

        context["current_app"] = "Settings"
        context["current_file"] = "Unknown"
        context["current_project"] = ""

        # Record creation
        record = {
            "timestamp": datetime.now().isoformat(),
            "category": context["title_category"],
            "app": context["current_app"],
            "context_type": context["app_category"],
            "context": {
                "section_path": context["current_file"]
            }
        }

        return record