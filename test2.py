from pywinauto import Desktop
from win32gui import GetForegroundWindow, GetWindowText

handle = GetForegroundWindow()

print("Active:", GetWindowText(handle))

window = Desktop(backend="uia").window(handle=handle)

# # Full UIA Output:
# for control in window.descendants():
#     text = control.window_text().strip()
#     if text:
#         print(f"{control.element_info.control_type} => {text}")

for control in window.descendants():
    if (control.element_info.control_type == "Edit"):
        url = control.window_text().strip()
        if ("." in url) and (" " not in url):
            print(f"URL: {url}")
            domain = url.split(".")[-2].capitalize()
            print(domain)
            break
else:
    url = ""

print(url)

# KNOWN_DOMAINS = {
#     "chatgpt.com": "ChatGPT",
#     "web.whatsapp.com": "Whatsapp",
#     "mail.google.com": "Gmail",
#     "home.atlassian.com": "Atlassian",
#     "github.com": "Github",
#     "yogendiran-s-p.atlassian.net/": "Jira Atlassian"
# }

# url = ""
# for control in window.descendants():
#     if (control.element_info.control_type == "Edit"):
#         url = control.window_text().strip()
#         print(url)
#         break

# url = url.split("/")[0].split(".")[-2].capitalize()
# print(url)
# print(window.descendants().window_text().strip())