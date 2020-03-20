from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

html = urlopen('https://morvanzhou.github.io/static/scraping/table.html')
# print(html)
soup = BeautifulSoup(html, features='lxml')  # 这里提取类型时lxml,xml:可扩展标记语言(X Exrensible Markup Language)
img_links = soup.find_all('img', {'src': re.compile('.*?\.jpg')})
# 找到所有'img'标签的内容,{}中为寻找文本的属性attributes(网页源代码为：src='....jpg'),'src'为标签
# img_links=soup.find_all('img')#和上面结果一样？？
print(img_links)
# print(type(img_links))
# 返回为一个<class 'bs4.element.ResultSet'>,bs类型的元素
for link in img_links:
    print(link['src'])  # 注意这里的表达方式,只要源代码中标签接'='就用这样用？
course_links = soup.find_all('a', {'href': re.compile('https://morvan.*')})  # '.'表示任何除了空行的字符,'*'表示出现0次或多次
# course_links=soup.find_all('a') #这个也是和上面寻找到的结果一样？？
for link in course_links:
    print(link['href'])
