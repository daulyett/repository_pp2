import re

sample_text = "My phone number is 87051234567 and my email is test123@gmail.com"

#1 re.search()
match = re.search(r"\d+", sample_text)
print("search:", match.group())

#2 re.findall()
all_numbers = re.findall(r"\d+", sample_text)
print("findall:", all_numbers)

#3 re.split()
split_text = re.split(r"\s", sample_text)
print("split:", split_text)

#4 re.sub()
replaced = re.sub(r"\d+", "XXXX", sample_text)
print("sub:", replaced)

#5 re.match()
match_start = re.match(r"My", sample_text)
print("match:", match_start.group())