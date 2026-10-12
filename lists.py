def remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
 
 
def second_largest(nums):
    distinct = sorted(set(nums), reverse=True)
    return distinct[1] if len(distinct) >= 2 else None
 
 
def rotate_right(items, k):
    if not items:
        return []
    k %= len(items)
    return items[-k:] + items[:-k] if k else items[:]
 

 