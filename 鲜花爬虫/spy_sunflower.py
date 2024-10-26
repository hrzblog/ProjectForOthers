import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义要爬取的页面
file = open('sunflower.html', 'rb')

html = file.read().decode('utf-8')

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(html, 'html.parser')

product_items = soup.find_all('div',class_="grid-item")  # 提取特征

# 初始化列表存储数据
price = []        # 价格
name = []         # 商品名称
num = []          # 销售件数
img = []          # 图片地址
feature = []      # 特点
new = []          # 是否是新品

# 遍历提取数据
for item in product_items:
    # 提取商品名称
    product_name = item.find('div', class_='product-title').get_text(strip=True) if item.find('div', class_='product-title') else '无信息'
    name.append(product_name.strip().split()[0:1])
    
    # 提取价格
    price_tag = item.find('span',class_='price-num')
    price_value = price_tag.get_text(strip=True) if price_tag else '无价格'
    price_value = price_value
    if price_value.isdigit():#判断是否为数字
        price.append(float(price_value.strip()))
    else:
        price.append(0)  # 如果价格不可用，则设为0

    # 提取销售量
    last_num = item.find('p', style="font-size:12px;color:#71797F;line-height:16px;")
    product_num = last_num.get_text(strip=True) if last_num else '无销售量信息'
    num.append(product_num)

    #获取图片地址
    url_tag = item.find('img', class_='width="220"')
    product_url = url_tag.get_text(strip=True) if url_tag else '无有效图片'
    img.append(product_url)

    #判断是否为新品
    feature_tag = item.find('div', class_='feature')
    product_feature = feature_tag.get_text(strip=True) if feature_tag else '无特点'
    feature.append(product_feature)
    new_is = item.find('img',style='width: 34px')#代表新品的图片
    if new_is:
        new.append("新品")
    else:
        new.append("非新品")

# 创建DataFrame
df = pd.DataFrame({'name': name, 
                   'price': price, 
                   'num': num,                   
                   'img': img,
                   'feature':feature,
                   'new':new,
                   })


#打印所有信息
print("------------------所有信息-----------------")
print(df)

#价格排序
df2 = df.sort_values('price',ascending=False)
#显示最贵的商品的所有信息
print("--------------最贵的商品是--------------\n{}\n".format(df2.iloc[0]))

#包含韩式的商品的所有信息
print("------------------包含'韩式'的商品的所有信息--------------------：\n")
print(df[df['name'].str.contains("韩式",na=False)]) #na=Flase 防止空值
print("\n")

#价格大于200元的所有商品的信息
print("------------价格大于200元的所有商品的信息------------:\n")
print(df[df['price'] > 200])
print("\n")



#价格平均值（因为没有评论）
print("---------------------价格平均值---------------------")
print(df['price'].mean())
df.to_csv('output.csv', index=False, encoding='utf-8-sig')