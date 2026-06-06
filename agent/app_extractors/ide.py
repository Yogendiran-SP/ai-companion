from datetime import datetime

def ide_extractor(context, parts):
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
    
    record = {
        "timestamp": datetime.now().isoformat(),
        "category": context["title_category"],
        "app": context["current_app"],
        "context_type": context["app_category"],
        "context": {
            "file": context["current_file"],
            "project": context["current_project"]
        }
    }

    return record