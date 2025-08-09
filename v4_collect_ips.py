import requests
from bs4 import BeautifulSoup
import re
import os
import ssl
from requests.adapters import HTTPAdapter

# 设置文件名变量
IP_PORT_FILE = 'v4_ip.txt'
IP_ONLY_FILE = 'v4_ip_only.txt'

# 自定义 TLS 适配器
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# 设置目标 URL 列表
urls = [
#     'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

# IP 地址正则表达式
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 常用 HTTPS 端口列表
# ports = [443]
ports = [443, 8443, 2053, 2083, 2087, 2096]

# 清理旧文件
for filename in [IP_PORT_FILE, IP_ONLY_FILE]:
    if os.path.exists(filename):
        os.remove(filename)

# 创建 session 并配置 TLS
session = requests.Session()
session.mount('https://', TLSAdapter())

# 存储唯一IP
unique_ips = set()

# 写入文件
with open(IP_PORT_FILE, 'w') as port_file, open(IP_ONLY_FILE, 'w') as ip_file:
    for url in urls:
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 根据网站的不同结构找到包含IP地址的元素
            if url in ['https://api.uouin.com/cloudflare.html', 'https://ip.164746.xyz']:
                elements = soup.find_all('td')
            else:
                elements = soup.find_all('li')
            
            # 从找到的元素中提取IP地址
            for element in elements:
                text = element.get_text()
                for ip in re.findall(ip_pattern, text):
                    if ip not in unique_ips:
                        unique_ips.add(ip)
                        ip_file.write(ip + '\n')
                        for port in ports:
                            port_file.write(f"{ip}:{port}\n")
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            continue

print(f"✅ 所有 IP 地址已保存到 {IP_PORT_FILE} 和 {IP_ONLY_FILE} 文件中。")
