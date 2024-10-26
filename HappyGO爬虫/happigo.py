import requests
from bs4 import BeautifulSoup
import pandas as pd

# 定义要爬取的页面
file = open('happigo.html', 'rb')

html = file.read().decode('utf-8')

# 使用BeautifulSoup解析网页内容
soup = BeautifulSoup(html, 'html.parser')

product_items = soup.find_all('li',class_='noborder')  # 提取特征

# 初始化列表存储数据
price = []     # 价格
name = []      # 商品名称
tips = []      #特殊点
discount = []  # 是否参与活动
size = []      #容量
image = []     #图片地址

#print(product_items)

# 遍历提取数据
for item in product_items:
    # 提取商品名称
    s = []
    product_name = item.find('a', class_='sl_title').get_text(strip=True) if item.find('a', class_='sl_title') else '无信息'
    #print(product_name.split())
    if 'ml' in product_name:#提取毫升数据
        if len(s) == 0:
            temp = product_name.split('ml')[0]
            temp2 = ''
            for j in range(-1,-len(temp)-1,-1):
                if temp[j].isdigit() or temp[j] == '.':
                    temp2 += temp[j]
                else:
                    break
            s.append(float(temp2[::-1]))
            size.append(s)
    else:
        size.append('无')

    if '）' in product_name:
        name.append(product_name.split('）')[-1])
        tips.append(product_name.split('）')[0])
    else:
        tips.append('无')
        name.append(product_name.strip())

    # 提取价格
    price_tag = item.find('span')
    #print(price_tag)
    price_value = price_tag.get_text(strip=True).replace('¥','') if price_tag else 0
    price.append(float(price_value))
    #获取图片地址
    image_tag = item.find('div',style="position: absolute; top: 0; right: 0;width:80px;height:80px;z-index:1;")
    if image_tag:
        discount.append('参与活动')
    else:
        discount.append('不参与活动')

    image_url = item.find('img')
    if image_url:
        image.append(image_url.get('src'))
    else:
        image.append('无图片地址')

# 创建DataFrame
df = pd.DataFrame({'tips':tips,
                   'name': name, 
                   'price': price, 
                   'size':size,
                   'discount':discount,
                   'image':image,
                   })


#打印所有信息
print("------------------所有信息-----------------")
print(df)

#价格排序
df2 = df.sort_values('price',ascending=False)
#显示最贵的商品
print("最贵的商品信息\n{}\n".format(df2.iloc[0]))

##包含精华的商品的所有信息
print("------------------包含'精华'的商品的所有信息--------------------：\n")
print(df[df['name'].str.contains("精华",na=False)]) #na=Flase 防止空值
print("\n")

#价格四舍五入 用整数方式显示
print("价格四舍五入")
print((df['price']+0.5).astype(int))
print("\n")

#价格大于500元的所有商品的信息
print("价格大于500元的所有商品的信息:\n")
print(df[df['price'] > 500])
print("\n")

#价格平均值
print("价格平均值")
print(df['price'].mean())#