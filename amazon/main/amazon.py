from lxml import html
import json
import requests
import json, re
from dateutil import parser as dateparser
from time import sleep
from bs4 import BeautifulSoup
import urllib.request
import validators

# p_list = []
p_rev = []
p_revth = []


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


def search_p(query):
    query = query.split()
    query = '+'.join(query)
    url = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=" + query + "&rh=i%3Aaps%2Ck%3A" + query
    print(url)

    header = {
        'User-Agent': "Mozilla/6.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
    soup = get_soup(url, header)

    ActualProducts = []  # contains the link for the products
    reviews = []
    for a in soup.find_all("a", class_="s-access-detail-page"):
        try:
            if a.find("h2") != None and validators.url(a.get("href")):
                name = a.find("h2").string
                link = a.get("href")
                ActualProducts.append((link, name))
        except Exception as e:
            print(e)
    '''''
    for i, (link, name) in enumerate(ActualProducts):
        try:
            p_list.append((i,name))
        except Exception as e:
            print(e)

    #p_list = list(enumerate(ActualProducts))

    l = len(ActualProducts)
    print("There are total " ,l," similar products")
    #print(p_list)
    #print(*p_list, sep="\n")

    '''''
    return ActualProducts


def ParseReviews(asin):
    extracted_data = []
    # for i in range(6):
    # 	try:
    # This script has only been tested with Amazon.com
    amazon_url = 'http://www.amazon.in/dp/' + asin
    # Add some recent user agent to prevent amazon from blocking the request
    # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(amazon_url, headers=headers, verify=False)
    page_response = page.text

    parser = html.fromstring(page_response)
    XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
    XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
    XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

    XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
    XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
    XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'

    raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
    product_price = ''.join(raw_product_price).replace(',', '')

    raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
    product_name = ''.join(raw_product_name).strip()
    total_ratings = parser.xpath(XPATH_AGGREGATE_RATING)
    reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
    if not reviews:
        reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
    ratings_dict = {}
    reviews_list = []

    if not reviews:
        raise ValueError('unable to find reviews in page')

    # grabing the rating  section in product page
    for ratings in total_ratings:
        extracted_rating = ratings.xpath('./td//a//text()')
        if extracted_rating:
            rating_key = extracted_rating[0]
            raw_raing_value = extracted_rating[1]
            rating_value = raw_raing_value
            if rating_key:
                ratings_dict.update({rating_key: rating_value})

    # Parsing individual reviews
    for review in reviews:
        XPATH_RATING = './/i[@data-hook="review-star-rating"]//text()'
        XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
        XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
        XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
        XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
        XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
        XPATH_AUTHOR = './/span[contains(@class,"profile-name")]//text()'
        XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'

        raw_review_author = review.xpath(XPATH_AUTHOR)
        raw_review_rating = review.xpath(XPATH_RATING)
        raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
        raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
        raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
        raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
        raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

        # cleaning data
        author = ' '.join(' '.join(raw_review_author).split())
        review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
        review_header = ' '.join(' '.join(raw_review_header).split())

        try:
            review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
        except:
            review_posted_date = None
        review_text = ' '.join(' '.join(raw_review_text1).split())

        # grabbing hidden comments if present
        if raw_review_text2:
            json_loaded_review_data = json.loads(raw_review_text2[0])
            json_loaded_review_data_text = json_loaded_review_data['rest']
            cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
            full_review_text = review_text + cleaned_json_loaded_review_data_text
        else:
            full_review_text = review_text
        if not raw_review_text1:
            full_review_text = ' '.join(' '.join(raw_review_text3).split())

        raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
        review_comments = ''.join(raw_review_comments)
        review_comments = re.sub('[A-Za-z]', '', review_comments).strip()
        review_dict = {

            'review_text': full_review_text,
            'review_posted_date': review_posted_date,
            'review_header': review_header,
            'review_rating': review_rating,
            'review_author': author

        }
        reviews_list.append(review_dict)
        p_rev.append(review_dict)
        p_revt = {
            'review_text': full_review_text,
            'review_header': review_header,
        }
        p_revth.append(p_revt)

    data = {
        'ratings': ratings_dict,
        'reviews': reviews_list,
        'url': amazon_url,
        'price': product_price,
        'name': product_name
    }
    # print(p_re)
    # print(p_revth)
    # print(p_revth[0])
    return p_rev, p_revth, data['ratings'], data['url'], data['price'], data['name']


def select_num(num, ap):
    link, name = ap[num]
    keyy = link.split("/")
    return keyy[5]


'''''''''''
ap = search_p('book')
p_ind = select_num(2, ap)
dat = ParseReviews(p_ind)
rdata = dat
str1 = str(rdata)
#print(".......")
#print(rdata.keys())
#print(".....")
#print(rdata.items())

#print("......")
#print(rdata.values())
#print(".....")
#print(str1)
#str2 = str(str1.split("}"))
#print(".............")
#print(str2)
#print("''''''''''''")
#str2 = str(str2.replace("["," "))
#print(str2)
#print(str2[3:97])
p_re = str(p_rev)
str4 = str(p_re.split(","))
print(p_rev[0])
'''''''''