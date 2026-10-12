def is_palindrome(s):
    cleaned = [ch.lower() for ch in s if ch.isalnum()]
    return cleaned == cleaned[::-1]
 
 
def is_anagram(a, b):
    return sorted(a.lower().replace(" ", "")) == sorted(b.lower().replace(" ", ""))
 
 
def compress(s):
    if not s:
        return s
    parts = []
    count = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            count += 1
        else:
            parts.append(f"{s[i - 1]}{count}")
            count = 1
    parts.append(f"{s[-1]}{count}")
    compressed = "".join(parts)
    return compressed if len(compressed) < len(s) else s