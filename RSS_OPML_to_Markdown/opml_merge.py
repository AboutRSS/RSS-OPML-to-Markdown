import os
import re
from opyml import OPML, Outline, Body, Head
import sys

def opmlparse(filename):
    with open(filename, encoding='utf-8') as f:
       opml1=OPML.from_xml(f.read())
       #opml2=Outline.parse_outlines(f.read())
    return opml1

def get_domain(url):
    """
    获取 URL 的主域名。

    Args:
        url: URL 字符串。

    Returns:
        URL 的主域名。
    """

    match = re.match(r'(https?://)(.*?)/(.*)', url)
    if match:
        return re.sub(r'www\.', '', match.group(2))
    else:
        return None
    
def erase_second_domain(url):
    match = re.match(r'(.*)\.(.*\..*)', url)
    if match:
        return match.group(2)

def merge_opml(opml_dir):
  """
  合并目录中所有 OPML 文件，并处理嵌套的 outline。

  Args:
    opml_dir: OPML 文件所在的目录。

  Returns:
    合并后的 OPML 文件。
  """

  # 读取目录中所有 OPML 文件

  opml_files = [os.path.join(opml_dir, f) for f in os.listdir(opml_dir) if f.endswith('.opml')]
  print(opml_files)

  # 初始化去重列表

  seen_urls = set()

  # 初始化合并后的 OPML 文件

  opml = OPML()
  opml.head = Head(
     title="OPML merged by github.com/aboutrss",
     docs="http://dev.opml.org/spec2.html",
     )


  # 遍历所有 OPML 文件

  for opml_file in opml_files:
    print(f'正在读取 OPML 文件：{opml_file}')
    parser = opmlparse(opml_file)

    # 遍历每个 outline

    for outline in parser.body.outlines:
      
      print(outline.xml_url)
      if outline.xml_url is None: # 如果 outline 是父 outline
        for outline in outline.outlines:
           print(outline.xml_url)
           if outline.html_url is None:
             if outline.xml_url and outline.title:
               url = outline.xml_url
               if url[0:7]=='http://':
                 url = url[7:]
                 if url in seen_urls:
                    continue
                 else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)
               elif url[0:8]=='https://':
                 url = url[8:]
                 if url in seen_urls:
                    continue
                 else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)

               opml.body.outlines.append(Outline(
                  text=outline.title,
                  xml_url=outline.xml_url,
               ))
             elif outline.xml_url and outline.text:
               url = outline.xml_url
               if url[0:7]=='http://':
                 url = url[7:]
                 if url in seen_urls:
                    continue
                 else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)
               elif url[0:8]=='https://':
                 url = url[8:]
                 if url in seen_urls:
                    continue
                 else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)
               opml.body.outlines.append(Outline(
                  text=outline.text,
                  xml_url=outline.xml_url,
               ))
           else:
              if outline.xml_url and outline.title:
                url = outline.html_url
                if url[0:7]=='http://':
                  url = url[7:]
                  print(url)
                  if url in seen_urls:
                     continue
                  else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)
                       
                elif url[0:8]=='https://':
                  url = url[8:]
                  print(url)
                  if url in seen_urls:
                     continue
                  else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)
             
                opml.body.outlines.append(Outline(
                   text=outline.title,
                   xml_url=outline.xml_url,
                   html_url=outline.html_url,
                ))
              elif outline.xml_url and outline.text:
                url = outline.html_url
                if url[0:7]=='http://':
                  url = url[7:]
                  print(url)
                  if url in seen_urls:
                     continue
                  else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)
                elif url[0:8]=='https://':
                  url = url[8:]
                  print(url)
                  if url in seen_urls:
                     continue
                  else:
                    domain = get_domain(outline.xml_url)
                    
                    if re.match(r'(.*)\.(.*\..*)', domain):
                      domain = erase_second_domain(domain)
                      print(domain)
                    if domain=='feed43.com':
                       
                       continue
                    else:
                      seen_urls.add(url)
                opml.body.outlines.append(Outline(
                   text=outline.text,
                   xml_url=outline.xml_url,
                   html_url=outline.html_url,
                ))

  return opml.to_xml()

def main():
    intro = """
    Use this Python script to merge OPML files.
    """
    if len(sys.argv) == 1:
        print(intro)
        sys.exit()
    elif len(sys.argv) == 2:
        opml = merge_opml(sys.argv[1])
        with open(os.path.join(sys.argv[1],'merged.opml'), 'w',encoding='utf-8') as f:
            f.write(opml)
    elif len(sys.argv) == 3:
        opml = merge_opml(sys.argv[1])
        with open(os.path.join(sys.argv[2],'merged.opml'), 'w',encoding='utf-8') as f:
            f.write(opml)
    else:
        print("Error: argv number doesn't match")
        exit(-1)

if __name__ == '__main__':
    main()