html=""
html+="<ul>\n"
f=open('../nodetxt/disease.txt','r')
n=1
for i in f:
    html+='<li class="second-menu"><a href="/deal_request?name={}&id={}">{}</a></li>\n'.format(i.strip(),n,i.strip())
    n+=1
html+="</ul>"
print(html)
