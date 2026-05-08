from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

total = 0
missing_pin_config = 0

response = es.search(
    index="full_ppn",
    scroll="5m",
    size=1000,
    _source=[
        "pin_config",
        "function_blocks",
        "application_circuits"
    ],
    query={
        "match_all": {}
    }
)

scroll_id = response["_scroll_id"]

while True:
    hits = response["hits"]["hits"]

    if not hits:
        break

    for hit in hits:
        total += 1

        source = hit["_source"]

        if not source.get("pin_config"):
            missing_pin_config += 1

    response = es.scroll(
        scroll_id=scroll_id,
        scroll="5m"
    )

    scroll_id = response["_scroll_id"]

es.clear_scroll(scroll_id=scroll_id)

print("总数:", total)
print("pin_config 缺失数:", missing_pin_config)
print("缺失率:", missing_pin_config / total)