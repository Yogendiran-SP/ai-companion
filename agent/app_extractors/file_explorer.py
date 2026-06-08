from pywinauto import Desktop
from datetime import datetime

def explorer_extractor(context, parts):
    try:
        explorer = Desktop(backend="uia").window(title_re=".*File Explorer*.")
        breadcrumb = explorer.child_window(
            auto_id="PART_BreadcrumbBar"
        )

        path=[]
        for child in breadcrumb.children():
            if child.friendly_class_name() == "SplitButton":
                text = child.window_text().strip()

                if text:
                    path.append(text)
        path="\\".join(path)
            
            # For Debugging
        # print(f"Path: {path}")

        # Context
        context["current_app"] = "File Explorer"
        context["current_file"] = path
        context["current_project"] = parts[0].strip()

        # Record creation
        record = {
            "timestamp": datetime.now().isoformat(),
            "context_type": context["context_category"],
            "app": context["current_app"],
            "category": context["app_category"],
            "context": {
                    "tab_title": context["current_project"],
                    "directory": context["current_file"]
            }
        }

        return record

    except Exception:
        # Context
        context["current_app"] = "File Explorer"
        context["current_file"] = "Unknown"
        context["current_project"] = ""

        # Record creation
        record = {
            "timestamp": datetime.now().isoformat(),
            "category": context["title_category"],
            "app": context["current_app"],
            "context_type": context["app_category"],
            "context": {
                "tab_title": context["current_project"],
                "directory": context["current_file"]
            }
        }

        return record