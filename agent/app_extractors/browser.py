from datetime import datetime

def browser_extractor(context, parts):
    if len(parts) >= 3:
        context["current_app"] = parts[-1].strip() # Get the last part as app name
        context["current_file"] = parts[0].strip()  # Get the first part as file name
        context["current_project"] = parts[1].strip()  # Get the second part as project name
    elif len(parts) == 2:
        context["current_app"] = parts[-1].strip() # Get the last part as app name
        context["current_file"] = parts[0].strip()  # Get the first part as file name
        context["current_project"] = ""  # No project information available
    else:
        context["current_app"] = parts[-1].strip() # Get the last part as app name
        context["current_file"] = ""  # No file information available
        context["current_project"] = ""  # No project information available

    record  = {
        "timestamp": datetime.now().isoformat(),
        "category": context["title_category"],
        "app": context["current_app"], # Get the last part as app name
        "context_type": context["app_category"],
        "context": {
            "Web App": context["current_project"], # Get the first part as tab name
            "Tab Title": context["current_file"]
        }
    }

    return record