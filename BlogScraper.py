import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
from markdownify import markdownify as md
import markdown
import html2text

def extract_blog(url):
    posts = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for article in soup.find_all('div', class_='post-outer'):  
        text_element = article.find('div', class_='post-body')
        tables = text_element.find_all('table')
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True

        if len(tables) > 0:
            text_element = str(text_element)
            start = text_element.find("<table")
            end = text_element.rfind("</table>")
            table = text_element[start:end+len("</table>")]
            beforetable = text_element[:start]
            aftertable = text_element[end+len("</table>"):]

            beforetable = text_maker.handle(beforetable)
            beforetable = markdown.markdown(beforetable, extensions=['extra', 'smarty'])
            aftertable = text_maker.handle(aftertable)
            aftertable = markdown.markdown(aftertable, extensions=['extra', 'smarty'])

            details = beforetable + table + aftertable
        else:
            details = md(str(text_element), autolinks=True, keep_inline_images_in=['td'], newline_style = 'SPACES')
            details = markdown.markdown(details, extensions=['extra', 'smarty']) 
            if 'img' in details:
                index = details.index("img") + len("img")
                firstpart = details[:index]
                backpart = details[index:]
                details = firstpart + ' style = "width: 100%"' + backpart

        header = article.find('h3', class_='post-title')  
        if header:
            header = header.text.strip()

        post = {'header': header, 'details': details}
        posts.append(post)
    return posts

def getNewPage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    older_posts = soup.find('a', class_='blog-pager-older-link')
    older_posts_url = older_posts['href']
    print(older_posts_url)
    return older_posts_url


def getfilters(url):
    filters = {}
    fils = []
    filterlinks = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    x = soup.find_all('div', class_="widget-content list-label-widget-content")[0]
    links = x.find_all('a')
    for link in links:
        filterlinks.append(link.get('href'))
        fils.append(link.get_text())
    filters["Filter"] = fils
    filters["Filterlinks"]  = filterlinks
    return filters

url = 'http://studentsblog.sst.edu.sg/'
app = Flask(__name__)

@app.route('/')
def home():
    posts = extract_blog(url)
    filters = getfilters(url)
    return render_template('blog.html', posts=posts, filters=filters)

