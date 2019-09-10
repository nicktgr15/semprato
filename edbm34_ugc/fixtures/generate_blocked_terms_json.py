import json

with open("blockedterms.txt") as f:
    blocked_terms = f.readlines()[0]

blocked_terms = [t.strip() for t in blocked_terms.split(",")]

blocked_terms_list = []
for k, b in enumerate(blocked_terms):
    blocked_terms_list.append(
        {
            "model": "article_manager.blockedterm",
            "pk": k+1,
            "fields": {
                "name": "%s" % b
            }
        }
    )

with open('blocked_terms.json', 'w') as f:
    json.dump(blocked_terms_list, f)




