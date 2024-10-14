from core.models import FeedBack 


feeds = FeedBack.objects.filter(staff__id=1)

for feed in feeds:
    print(f'\tname :{feed.staff.fname} {feed.staff.sname} - {feed.subject.subject_code}')
    print(f'cat1 : {feed.cat1}')
    print(f'cat2 : {feed.cat2}')
    print(f'cat3 : {feed.cat3}')
    print(f'cat4 : {feed.cat4}')
    print(f'cat5 : {feed.cat5}')
    print(f'cat6 : {feed.cat6}')
    print(f'cat7 : {feed.cat7}')
    print(f'cat8 : {feed.cat8}')
    print(f'cat9 : {feed.cat9}')
    print(f'cat10 : {feed.cat10}')
    print("\n")