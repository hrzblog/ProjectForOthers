import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义要爬取的页面
file = open('wandou.html', 'rb')

html = file.read().decode('utf-8')

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(html, 'html.parser')

product_items = soup.find_all('a',class_="goods")#提取特征  

# 初始化列表存储数据
slogan = []      #宣传语
price = []       #价格
brand = []       #品牌
container = []   #容量
color = []       #颜色
image = []         #买手心选

# 遍历提取数据

for item in product_items:
    #提取商品slogan
    product_slogan = item.find('div', class_='goods-slogan').get_text(strip=True) if item.find('div', class_='goods-slogan') else '无信息'
    slogan.append(product_slogan.strip())
  
    #提取商 品品牌 容量 颜色
    product_name = item.find('div',class_='goods-title').get_text(strip=True) if item.find('div',class_='goods-title') else '无信息'
    brand.append(product_name.split()[1].strip())#品牌
    container.append(product_name.split()[-1].strip())#容量
    color.append(product_name.split()[-2].strip())#颜色


    #提取价格
    price_tag = item.find('div',class_='goods-price')
    price_value = price_tag.get_text(strip=True).replace('¥', '') if price_tag else '无价格'
    price_value = price_value.replace(',', '')  # 去除千位分隔符
    if price_value.isdigit():
        price.append(float(price_value.strip()))
    else:
        price.append(0.0)  # 如果价格不可用，则设为0

    #是否买手心选right-corner-img
    image_tag = item.find('div',class_="right-corner-img")
    if image_tag:
        image.append("买手心选")
    else:
        image.append('无心选')

    while len(slogan)!=len(brand):
        slogan.append(float(0))



# 创建DataFrame
df = pd.DataFrame({'slogan': slogan, 
                   'brand': brand,
                   'price': price, 
                   'container': container,                   
                   'color': color,
                   'image':image,
                   })


#打印所有信息
print("------------------所有信息-----------------")
print(df)

#价格排序
df2 = df.sort_values('price',ascending=False)

print("\n")
#显示最贵的商品的所有信息
print("--------------最贵的商品信息--------------\n{}\n".format(df2.iloc[0]))

#包含  象印  的商品的所有信息
print("------------------包含'象印'的商品的所有信息--------------------：\n")
print(df[df['brand'].str.contains("象印",na=False)]) #na=Flase 防止空值
print("\n")

#价格大于150元的所有商品的信息
print("------------价格大于300元的所有商品的信息------------:\n")
print(df[df['price'] > 300])
print("\n")

#价格四舍五入 用整数方式显示
print("--------价格四舍五入 用整数方式显示----------:")
print((df['price']+0.5).astype(int))
print("\n")

#价格平均值（因为没有评论）
print("---------------------价格平均值---------------------")
print(df['price'].mean())
