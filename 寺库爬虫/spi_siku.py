import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义要爬取的页面
file = open('siku.html', 'rb')

html = file.read().decode('utf-8')

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(html, 'html.parser')

product_items = soup.find_all('dl')  # 提取特征

# 初始化列表存储数据
price = []     # 价格
name = []      # 商品名称
ziying = []    #是否自营
num = []       # 件数
discount = []  # 是否降价
size = []      #尺码

#print(product_items)
# 遍历提取数据
for item in product_items:
    # 提取商品名称
    product_name = item.find('dd', class_='dl_name').get_text(strip=True) if item.find('dd', class_='dl_name') else '无信息'
    if '/' not in product_name:   #没有名字就跳过
        continue;
    if ',' in product_name:       #处理长文字
        name.append(product_name.split(',')[0].strip())
    elif '女士' in product_name:   #截取女士之前的文字
        name.append(product_name.split('女士')[0].strip())
    else:
        name.append(product_name.strip().split()[0:1])
    
    #提取 是否自营
    ziying_is = item.find('span',class_='s1').get_text(strip=True) if item.find('span',class_='s1') else '无信息'
    ziying.append(ziying_is.strip())


    # 提取价格
    price_tag = item.find('dd',class_='dl_price clearfix')
    price_value = price_tag.get_text(strip=True).replace('￥', '') if price_tag else '无价格'
    price_value = price_value.replace(',', '')  # 去除千位分隔符
    if price_value.isdigit():
        price.append(float(price_value.strip()))
    else:
        price.append(0.0)  # 如果价格不可用，则设为0

    # 提取剩余件数
    last_num = item.find('span', class_='deal-cnt')
    product_num = last_num.get_text(strip=True) if last_num else '无数量'
    num.append(product_num)

    # 所属活动
    discount_tag = item.find('span', class_='s2')
    product_discount = discount_tag.get_text(strip=True) if discount_tag else '无活动'
    discount.append(product_discount)

    #尺码
    size_tag = item.find('dd', class_='dl_size clearfix')
    product_size = size_tag.get_text(strip=True) if size_tag else '无尺码'
    size.append(product_size.strip())


# 创建DataFrame
df = pd.DataFrame({'name': name, 
                   'ziying': ziying,
                   'price': price, 
                   'num': num,                   
                   'discount': discount,
                   'size':size,
                   })


#打印所有信息
print("------------------所有信息-----------------")
print(df)

#价格排序
df2 = df.sort_values('price',ascending=False)
#显示最贵的商品的所有信息
print("--------------最贵的商品是--------------\n{}\n".format(df2.iloc[0]))

#包含周仰杰的商品的所有信息
print("------------------包含'周仰杰'的商品的所有信息--------------------：\n")
print(df[df['name'].str.contains("周仰杰",na=False)]) #na=Flase 防止空值
print("\n")

#价格大于7000元的所有商品的信息
print("------------价格大于7000元的所有商品的信息------------:\n")
print(df[df['price'] > 7000])
print("\n")

#价格四舍五入 用整数方式显示
print("--------价格四舍五入 用整数方式显示----------:")
print((df['price']+0.5).astype(int))
print("\n")

#价格平均值（因为没有评论）
print("---------------------价格平均值---------------------")
print(df['price'].mean())