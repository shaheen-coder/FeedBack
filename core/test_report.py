from core.models import FeedBack 

cat_data = {
    'cat_1' : 0,
    'cat_2' : 0,
    'cat_3' : 0,
    'cat_4' : 0,
    'cat_5' : 0,
    'cat_6' : 0,
    'cat_7' : 0,
    'cat_8' : 0,
    'cat_9' : 0,
    'cat_10' : 0,
}
feeds = FeedBack.objects.filter(staff__id=1)
count = feeds.count()
for feed in feeds:
    for key,data in feed.categories.items():
        cat_data[key] += data
for key,data in cat_data.items():
    cat_data[key] = data / count
print(f'cat data : {cat_data}')