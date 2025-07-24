import requests
from bs4 import BeautifulSoup
import re
import os
import ssl
from requests.adapters import HTTPAdapter

# 自定义 TLS 适配器
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

# 设置目标 URL 列表
urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html',
    'https://ip.164746.xyz'
]

# IP 地址正则表达式
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 常用 HTTPS 端口列表
ports = [443, 8443, 2053, 2083, 2087, 2096]

# 清理旧文件
for filename in ['v4_ip.txt', 'v4_ip_only.txt']:
    if os.path.exists(filename):
        os.remove(filename)

# 创建 session 并配置 TLS
session = requests.Session()
session.mount('https://', TLSAdapter())

# 存储唯一IP
unique_ips = set()

# 写入文件
with open('v4_ip.txt', 'w') as port_file, open('v4_ip_only.txt', 'w') as ip_file:
    for url in urls:
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            elements = soup.find_all('tr') if url in urls else soup.find_all('li')
            
            for element in elements:
                for ip in re.findall(ip_pattern, element.get_text()):
                    if ip not in unique_ips:
                        unique_ips.add(ip)
                        ip_file.write(ip + '\n')
                        for port in ports:
                            port_file.write(f"{ip}:{port}\n")
        except Exception:
            continue

print("✅ 所有 IP 地址已保存到 ip.txt 文件中。")