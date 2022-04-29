from spyder import *

url = 'https://alumni.xmu.edu.cn/'
page = analysis_page(url)

print(url)
baseurl = get_base_url(url)
if page == None:
    print(None)
    exit()
baseurl = 'https://' + baseurl + '/'
soup = bs(page.content, 'html.parser')
tags = soup.select("a")
ans = set()
for a in tags:
    print(a.get('href'))
    if  not a.get('href') == None :
        context = str(a['href'])
        print("context is ",context)
        if context.endswith('.htm') and not context.startswith('http'):
            ans.add(baseurl + a['href'])
        elif context.__contains__('xmu.edu.cn') and not context.endswith('pdf'):
            ans.add(a['href'])
print(ans)