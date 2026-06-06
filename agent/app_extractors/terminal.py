from datetime import datetime

def terminal_extractor(context, parts):
    context["current_app"] = parts[-1].strip()
    context["current_file"] = parts[0].strip()
    context["current_project"] = ""

    record  = {
        "timestamp": datetime.now().isoformat(),
        "category": context["title_category"],
        "app": context["current_app"], # Get the last part as app name
        "context_type": context["app_category"],
        "context": {
            "directory": context["current_file"] # Get the first part as directory name
        }
    }

    return record