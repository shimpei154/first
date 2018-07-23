import sys
import os
from selenium import webdriver
import pandas
import time

browser = webdriver.Chrome(executable_path='C:/Users/shimpei/Documents/python/webdriver/chromedriver.exe')

#1 
args = sys.argv
print(args)
df = pandas.read_csv('default.csv', index_col=0, encoding="shift_jis")

#2
query = args[1]
print(query)

#3 

browser.get("https://www.mercari.com/jp/search/?sort_order=price_desc&keyword={}&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=".format(query))

#4

page = 1

#5

while True: #continue until getting the last page

    #5-1

    if len(browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")

        #5-1-2

        posts = browser.find_elements_by_css_selector(".items-box")

        #5-1-3

        for post in posts:
            title = post.find_element_by_css_selector("h3.items-box-name").text

            #5-1-3-1

            price = post.find_element_by_css_selector(".items-box-price").text
            price = price.replace('?', '')

            #5-1-3-2

            sold = 0
            if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
                sold = 1

            url = post.find_element_by_css_selector("a").get_attribute("href")
            se = pandas.Series([title, price, sold,url],['title','price','sold','url'])
            df = df.append(se, ignore_index=True)

        #5-1-4

        page+=1

        btn = browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        print("Moving to next page......")

    #5-2

    else:
        print("no pager exist anymore")
        break
#6
#df.to_csv("{}.csv".format(query), encoding="utf-8")
#df.to_csv("{}.csv".format(query), encoding="shift-jis")
df.to_csv("{}.csv".format(query), encoding="cp932")
print("DONE")
