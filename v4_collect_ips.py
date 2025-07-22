import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = ['https://api.uouin.com/cloudflare.html', 
        'https://ip.164746.xyz'
        ]

# 正则表达式用于匹配IP地址
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 要添加的端口列表
ports = [443, 8443, 2053, 2083, 2087, 2096]

# 检查ip.txt和ip_only.txt文件是否存在,如果存在则删除它们
for filename in ['v4_ip.txt', 'v4_ip_only.txt']:
    if os.path.exists(filename):
        os.remove(filename)

# 创建一个集合来存储唯一的IP地址(用于ip_only.txt)
unique_ips = set()

# 创建文件来存储带端口的IP地址
with open('v4_ip.txt', 'w') as file, open('v4_ip_only.txt', 'w') as ip_only_file:
    for url in urls:
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://api.uouin.com/cloudflare.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')
        
        # 遍历所有元素,查找IP地址
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            
            # 如果找到IP地址,则写入文件并添加所有端口
            for ip in ip_matches:
                # 添加到唯一IP集合中
                unique_ips.add(ip)
                # 写入带端口的文件
                for port in ports:
                    file.write(f"{ip}:{port}\n")
    
    # 将唯一IP写入ip_only.txt文件
    for ip in unique_ips:
        ip_only_file.write(f"{ip}\n")

print('带端口的IP地址已保存到ip.txt文件中。')
print('不带端口的IP地址已保存到ip_only.txt文件中。')
