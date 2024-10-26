import requests
from bs4 import BeautifulSoup
import pandas as pd

from PIL import Image

# 定义要爬取的页面
file = open('wangyi_yanxuan.html', 'rb')

html = file.read().decode('utf-8')

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(html, 'html.parser')

product_items = soup.find_all('li',class_='item')  # 提取特征

# 初始化列表存储数据
brand = []     #品牌
price = []     #当前价格
price_2 = []   #降价前
name = []      #商品名称
describe = []  #型号
value_l = []   #容量
image_url = [] #图片地址

#print(product_items)
# 遍历提取数据
for item in product_items:
    #商品名称
    product_name = item.find('h4',class_='name').get_text(strip=True) if item.find('h4',class_='name') else '无'
    if product_name == '无' : continue
    name.append(product_name.strip())
    print(product_name.split())
    describe.append(product_name.split()[-1])
    #品牌
    if '电饭煲' in product_name:
        brand.append(product_name.split('电饭煲')[0])
        #print(product_name.split('电饭煲')[0])
    else:
        brand.append('无品牌')
        #print('无品牌')

    #容量
    if 'L' in product_name:
        value = product_name.split('L')[0] # 去除前后空格，并只提取数字部分，避免其他字符干扰
        value_l.append(value.strip().split()[-1])
    elif '升' in product_name:
        value = product_name.split('升')[0]
        value_l.append(value.strip().split()[-1])
    else:
        value_l.append('无')

    
    #描述
    #describe_tag = item.find('p',class_='desc').get_text(strip=True) if item.find('p',class_='desc') else '无信息'
    #describe.append(describe_tag.strip())
    #print(describe_tag.strip())

    #价格 降价前和降价后
    price_tag = item.find('p',class_='price')
    price_value = price_tag.get_text(strip=True).replace('¥', ' ') if price_tag else '无价格'

    price.append(float(price_value.split()[0]))
    #print(float(price_value.split()[0]))

    if len(price_value.split()) > 1:
        price_2.append(float(price_value.split()[1]))
        #print(float(price_value.split()[1]))
    else:
        price_2.append(0.0) #表示没有以前的价格
        ##print(0.0)

    product_url = item.find('img',class_='imgScene img-lazyload j-lazyload img-lazyloaded')
    if product_url:
        url = product_url.get('src')
        img = Image.open(url)
        #img.show()
    else:
        image_url.append('无')
    

# 创建DataFrame
df = pd.DataFrame({'brand':brand,
                   'name': name, 
                   'describe': describe,
                   'price': price, 
                   'price_2':price_2,                
                   'vavlue_l':value_l,
                   })
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#所有商品
print("所有商品…………………………………………………………………………")
print(df)

#价格排序
df2 = df.sort_values('price',ascending=False)
#显示最贵的商品的所有信息
print("最贵的商品…………………………………………………………………………\n{}\n".format(df2.iloc[0]))
#
#包含九阳的商品的所有信息
print("包含'九阳'的商品的所有信息…………………………………………………………………………：\n")
print(df[df['name'].str.contains("九阳",na=False)])
print("\n")

#价格大于6000元的所有商品的信息
print("价格大于6000元的所有商品的信息…………………………………………………………………………:\n")
print(df[df['price'] > 6000])
print("\n")

##价格四舍五入 用整数方式显示
print("价格四舍五入 用整数方式显示…………………………………………………………………………:")
print((df['price']+0.5).astype(int))
print("\n")

#价格平均值
print("价格平均值…………………………………………………………………………")
print(df['price'].mean())

#写到表格里
#df.to_csv('output_file.csv', encoding='gbk')