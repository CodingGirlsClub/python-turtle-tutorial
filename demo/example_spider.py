from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords=python")
element = driver.find_element_by_id('s-results-list-atf') # 包含所有商品的表格
books = element.find_elements_by_tag_name('li') # 所有书的list

for book in books: # 对每一本书
    title = book.find_element_by_class_name('s-color-twister-title-link') # 找到title对应的<a>标签
    title_name = title.find_element_by_tag_name('h2') # 找到title对应的<h2>标签
    print(title_name.text) # 输出title
    
    
import time
for i in range(20):
    element = driver.find_element_by_id('s-results-list-atf') 
    books = element.find_elements_by_tag_name('li')
    for n, book in enumerate(books):
        try:
            title = book.find_element_by_class_name('s-color-twister-title-link')
            title_name = title.find_element_by_tag_name('h2')
            print(n, title_name.text)
        except:
            continue
    next_page = driver.find_element_by_id('pagnNextString')
    while(True):
        try:
            next_page.click()
            break
        except:
            time.sleep(1)
            next_page = driver.find_element_by_id('pagnNextString')
            print("翻页错误")
            continue