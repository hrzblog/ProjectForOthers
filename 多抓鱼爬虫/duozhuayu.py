import pandas as pd
import requests
from bs4 import BeautifulSoup

file=open('./duoyu.html','rb')
html=file.read().decode('utf-8')
soup=BeautifulSoup(html,'html.parser')

#提取总特征
items = soup.find_all('div',class_='jsx-2961166380 book-item-wrap tag_books_item')  # 提取特征

#存取列表
title = []       #书名
name = []        #作者
Publishers = []  #出版社
time = []        #出版时间
rating = []      #点赞数
price=[]         #价格

#print(items)
for item in items:
   t1 = item.find('h3',class_='jsx-2970330457 title').get_text(strip=True) if item.find('h3',class_='jsx-2970330457 title') else '没有'
   title.append(t1.strip())

   ph = item.find_all('p',class_='jsx-2160765878 meta-info')

   if ph:
      ph_texts = [p.get_text(strip=True) for p in ph]
      if ph_texts:
         if len(ph_texts) > 0:
            t2 = ph_texts[0].strip()
         else:
            t2 = '没有'

         if len(ph_texts) > 1:
            t3 = ph_texts[1].strip()
         else:
            t3 = '没有'

         if len(ph_texts) > 2:
            t4 = ph_texts[2].strip()
         else:
            t4 = '没有'
         name.append(t2)
         Publishers.append(t3)
         time.append(t4)
      else:
         name.append("无信息")
         Publishers.append("无信息")
            
   else:   
      name.append("无信息")
      Publishers.append("无信息")

   #点赞数 
   t5 = item.find('span',class_='jsx-838178438 label').get_text(strip=True) if item.find('span',class_='jsx-838178438 label') else '没有'
   rating.append(int(t5))

   #价格 
   t6 = item.find('span',class_='jsx-2899740217 Price Price--medium').get_text(strip=True) if item.find('span',class_='jsx-2899740217 Price Price--medium') else '没有'
   t6 = t6.replace('起','')
   t6 = t6.replace('¥','')
   price.append(float(t6))



df = pd.DataFrame({'title':title ,    
                   'name':name ,    
                   'Publishers': Publishers,
                   'time': time ,  
                   'rating':rating,   
                   'price':price,
                   })
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(df)

#价格排序
df2 = df.sort_values('price',ascending=False)
#显示最贵的商品的所有信息
print("<<<<<<<<<<<<<<<<<<<<<<<最贵的商品>>>>>>>>>>>>>>>>>>>>>>>>>\n{}\n".format(df2.iloc[0]))
#点赞排序
df3 = df.sort_values('rating',ascending=False)
#显示点赞最多商品的所有信息
print("<<<<<<<<<<<<<<<<<<<<<<<<点赞最多商品>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n{}\n".format(df3.iloc[0]))


#包含大国的商品的所有信息
print("<<<<<<<<<<<<<<<<<<<<包含'大国'的商品的所有信息>>>>>>>>>>>>>>>>>>>\n")
print(df[df['name'].str.contains("大国",na=False)])
print("\n")

#价格大于60元的所有商品的信息
print("<<<<<<<<<<<<<<<<<<价格大于60元的所有商品的信息>>>>>>>>>>>>>>>>>>\n")
print(df[df['price'] > 60])
print("\n")

#价格大于60元且点赞大于10个的所有商品的信息
print("<<<<<<<<<<<<<<<<<<价格大于60元的且点赞10个以上的所有商品的信息>>>>>>>>>>>>>>>>>>\n")
print( df[ (df['price'] > 60) & (df['rating']>10)] )
print("\n")

##价格四舍五入 用整数方式显示
print("<<<<<<<<<<<<<<<<<<<<价格四舍五入 用整数方式显示>>>>>>>>>>>>>>>>>>>>>>>")
print((df['price']+0.5).astype(int))
print("\n")

#点赞平均值
print("<<<<<<<<<<<<<<<<<<<<点赞平均值>>>>>>>>>>>>>>>>>>>>>")
print(df['rating'].mean())