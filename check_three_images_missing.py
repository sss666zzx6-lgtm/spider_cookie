import requests
from src.utils.config import settings

ES   = "http://lumy-z4p.public.cn-hangzhou.es-serverless.aliyuncs.com:9200"
AUTH = (settings.ES_USER, settings.ES_PWD)

FIELDS = ["application_circuits", "function_blocks", "pin_config"]

total = 0
counts = {f: 0 for f in FIELDS}
all_three   = 0
missing_one = 0
missing_two = 0
missing_all = 0
missing_details = {}
missing_one_detail = {f: 0 for f in FIELDS}
missing_two_detail = {f: 0 for f in FIELDS}

brand_stats = {}

search_after = None

while True:
    body = {
        "query": {"match_all": {}},
        "_source": FIELDS + ["product_number", "brand"],
        "size": 1000,
        "sort": [{"key": "asc"}]
    }
    if search_after:
        body["search_after"] = search_after

    r= requests.post(f"{ES}/full_ppn/_search", auth=AUTH, json=body, timeout=30)
    hits = r.json()["hits"]["hits"]
    if not hits:
        break

    for h in hits:
        total += 1
        s = h["_source"]
        ppn = s.get("product_number") or h["_id"]

        missing_fields = [f for f in FIELDS if not s.get(f)]
        if missing_fields:
            missing_details.setdefault(ppn, []).extend(missing_fields)

        has = sum(1 for f in FIELDS if s.get(f))
        for f in FIELDS:
            if s.get(f):
                counts[f] += 1
        if has == 3:
            all_three += 1
        elif has == 2:
            missing_one += 1
            for f in FIELDS:
                if not s.get(f):
                    missing_one_detail[f] += 1
        elif has == 1:
            missing_two += 1
            for f in FIELDS:
                if s.get(f):
                    missing_two_detail[f] += 1
        else:
            missing_all += 1

        brand = (s.get("brand") or {}).get("name", "未知")
        if brand not in brand_stats:
            brand_stats[brand] = {"total": 0, "all_three": 0, "missing_one": 0, "missing_two": 0, "missing_all": 0}
        brand_stats[brand]["total"] += 1
        brand_stats[brand]["all_three"] += (has == 3)
        brand_stats[brand]["missing_one"] += (has == 2)
        brand_stats[brand]["missing_two"] += (has == 1)
        brand_stats[brand]["missing_all"] += (has == 0)

    search_after = hits[-1]["sort"]
    print(f"已扫描 {total} 条...", flush=True)

print(f"\n总文档数: {total:,}")
print()
print("单字段空缺率:")
print(f"{'字段':<25} {'有图':>8} {'缺失':>8} {'空缺率':>8}")
print("-" * 55)
for f in FIELDS:
    has     = counts[f]
    missing = total - has
    print(f"{f:<25} {has:>8,} {missing:>8,} {missing/total*100:>7.2f}%")

print()
print("三图组合分布:")
print(f"  三图齐全:           {all_three:>6,}  ({all_three/total*100:.2f}%)")
print(f"  缺 1 张（有 2 张）: {missing_one:>6,}  ({missing_one/total*100:.2f}%)")
print(f"  缺 2 张（只有 1 张）:{missing_two:>6,}  ({missing_two/total*100:.2f}%)")
print(f"  三图全缺:           {missing_all:>6,}  ({missing_all/total*100:.2f}%)")

print()
print("缺1张细分（具体缺哪个字段）:")
for f in FIELDS:
  print(f"  缺 {f:<26}{missing_one_detail[f]:>8,}  ({missing_one_detail[f]/total*100:.2f}%)")

print()
print("缺2张细分（具体只剩哪个字段）:")
for f in FIELDS:
  print(f"  仅剩 {f:<25}{missing_two_detail[f]:>8,}  ({missing_two_detail[f]/total*100:.2f}%)")

print()
print("=" * 80)
print("按品牌图片完整度统计:")
print(f"{'品牌':<18} {'总数':>8} {'三图齐全':>8} {'缺1张':>6}{'缺2张':>6} {'三图全缺':>6}")
print("-" * 80)

# 按总数降序排列
for brand, st in sorted(brand_stats.items(), key=lambda x: x[1]["total"], reverse=True):
    t = st["total"]
    print(
        f"{brand:<18} {t:>8,} {st['all_three']:>8,} {st['missing_one']:>6,}({st['missing_one'] / t * 100:>.2f}%)"
        f" {st['missing_two']:>6,}({st['missing_two'] / t * 100:>.2f}%) {st['missing_all']:>6,}({st['missing_all'] / t * 100:>.2f}%)")
print()
if missing_details:
    print(f"缺失明细（共 {len(missing_details)} 个型号缺失）:")
    print("-" * 60)
    for ppn, fields in sorted(missing_details.items()):
        # 去重 + 排序
        unique = sorted(set(fields))
        print(f"  {ppn:20s} 缺: {', '.join(unique)}")
else:
    print("所有型号三图齐全，无缺失")