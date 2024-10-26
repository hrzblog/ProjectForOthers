import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义要爬取的页面
file = open('notebook.html', 'rb')

html = file.read().decode('utf-8')

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(html, 'html.parser')

product_items = soup.find_all('div',class_="prod_item_wrapper")#提取特征  

# 初始化列表存储数据
name = []      #商品名字
price = []     #价格
brand = []     #店铺名字
num = []       #销量
num_sub = []   #多少件起批
fac_is = []    #工厂直供

# 遍历提取数据

for item in product_items:
    #提取商品name
    product_name = item.find('div', class_='prod_item_name').get_text(strip=True) if item.find('div', class_='prod_item_name') else '无信息'
    name.append(product_name.strip())

    #提取价格
    price_tag = item.find('div',class_='prod_item_price')
    price_value = price_tag.get_text(strip=True) if price_tag else 0
    if price_value == '面议':#把面议的数据换成0
        price.append(0.0)
    elif price_value:
        price.append(float(price_value.strip()))
    else:
        price.append(0.0)

    #销量    
    num_tag = item.find('div',class_='prod_item_hot')
    num_value = num_tag.get_text(strip=True) if num_tag else 0
    num.append(num_value.split('销量指数：')[-1])

    #起批的数量
    num_sub_tag = item.find('div',class_='minOrderQuantity')
    num_sub_value = num_sub_tag.get_text(strip=True) if num_sub_tag else 0
    num_sub.append(num_sub_value.split('件起批')[0])

    #店铺名字
    brand_name = item.find('div',class_='prod_item_shop_name')
    brand_value = brand_name.get_text(strip=True) if brand_name else 0
    brand.append(brand_value)
    
    #是否工厂直供
    factory = item.find('img',class_='sourceIcon')
    if factory:
        fac_is.append('工厂直供')
    else:
        fac_is.append('非')

# 创建DataFrame
df = pd.DataFrame({'name': name, 
                   'price': price, 
                   'num':num,
                   'num_sub':num_sub,
                   'shop':brand,
                   'fac_is':fac_is,
                   })


#打印所有信息
print("------------------所有信息-----------------")
print(df)

##价格排序
df2 = df.sort_values('price',ascending=False)

print("\n")
#显示最贵的商品的所有信息
print("--------------最贵的商品信息--------------\n{}\n".format(df2.iloc[0]))

#包含  键盘  的商品的所有信息
print("------------------包含'键盘'的商品的所有信息--------------------：\n")
print(df[df['name'].str.contains("键盘",na=False)]) #na=Flase 避免 空 的情况
print("\n")

#销量平均值
print("---------------------价格平均值---------------------")
print(df['num'].mean())

#价格大于300元的所有商品的信息
print("------------价格大于300元的所有商品的信息------------:\n")
print(df[df['price'] > 300])
print("\n")

#价格四舍五入 用整数方式显示
print("--------价格四舍五入 用整数方式显示----------:")
print((df['price']+0.5).astype(int))
print("\n")

