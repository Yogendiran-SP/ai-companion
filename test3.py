from urllib.parse import urlparse

url = [
    "search.brave.com/search?q=Hello+Bro&source=desktop",
    "www.youtube.com/watch?v=vAZ_9lbriOk&list=RDvAZ_9lbriOk&start_radio=1",
    "chatgpt.com/c/6a0c816e-1954-8321-af23-9b2735c3f358",
    "mail.google.com/mail/u/0/?ogbl#inbox",
    "learn.microsoft.com/en-us/training/modules/analyze-text-ai-language/1-introduction?pivots=text"
]

for i in url:
    print(f"i: {i}")
    parsed = urlparse(i)
    # print(f"Fragements: {parsed.fragment}")
    fragments = parsed.fragment
    print("Fragments:",fragments)
    print("Path:",parsed.path)
    path = parsed.path.split("/")
    if path[-1] == "": path = path[:-1]
    print("Path List:",path)
    # print(f"query: {parsed.query.split("&")}")
    queries=[]
    for q in parsed.query.split("&"):
        if "=" in q:
            queries.append(q.split("="))
        else:
            queries.append(q.split())
            queries[-1].append("")
    # print(f"queries: {queries}")
    # queries = [q.split("=") for q in parsed.query.split("&")]
    try:
        queries = dict(queries)
        for key, value in queries.items():
            if "+" in value:
                queries[key] = " ".join(value.split("+"))
    except:
        queries = dict()
    print(f"Queries: {queries}")
    print()