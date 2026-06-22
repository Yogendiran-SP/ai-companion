from datetime import datetime
from pywinauto import Desktop
from urllib.parse import urlparse

def url_extractor(handles, app):
    window = Desktop(backend="uia").window(handle=handles)
    url=""

    for control in window.descendants():
        if (control.element_info.control_type == "Edit") and ('.' in control.window_text().strip()):
            url = control.window_text().strip()
            if ("." in url) and (" " not in url):
                print(f"URL: {url}")
                parsed = urlparse(url)
                path = urlparse(url).path.split("/")
                if path[-1] == "": path = path[:-1]
                fragments = parsed.fragment
                queries=[]
                for q in parsed.query.split("&"):
                    if "=" in q:
                        queries.append(q.split("="))
                    else:
                        queries.append(q.split())
                        queries[-1].append("")
                try:
                    queries = dict(queries)
                    for key, value in queries.items():
                        if "+" in value:
                            queries[key] = " ".join(value.split("+"))
                except:
                    queries = dict()
                # url_segments = url.split("/")[1:]
                # app_name = url.split("/")[0].split(".")[-2].capitalize()
                return (url, path[0], path[1:], queries, fragments)
    else:
        (url, app_name, url_segments, fragments) = ("", "", [], "")
        print(f"url:{url}, app_name:{app_name}, url_segments:{url_segments}")
        return (url, app_name, url_segments, fragments)


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
             
    (url, app, url_segments, query_params, fragments) = url_extractor(handles, parts[-1].strip())
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
            "url": url.lower().strip(),
            "web_app": context["current_project"], # Get the first part as tab name
            "tab_title": context["current_file"],
            "url_segments": url_segments,
            "query_params": query_params,
            "fragment": fragments
        }
    }

    return record