import time
import asyncio

from aiohttp import TCPConnector
from playwright.async_api import async_playwright
import playwright
import json
import requests
import asyncio
import aiohttp
import sys
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


ip89 = [('https://www.89ip.cn/index_1.html','.layui-table tbody tr td:nth-child(1)','.layui-table tbody tr td:nth-child(2)','.layui-laypage-next')]
ipbee = [('https://www.beesproxy.com/free','.wp-block-table tbody tr td:nth-child(1)','.wp-block-table tbody tr td:nth-child(2)','.next.page-numbers')]
ipcloud = [('http://www.ip3366.net/free/?stype=1&page=1','#list tbody tr td:nth-child(1)','#list tbody tr td:nth-child(2)','#listnav ul a:nth-child(7)')]


async def getip(pages,ips,ports,next):
    end = int(input('结束网页数: '))
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(f'{pages}')

            now = 1
            iplist = []

            for _ in range(now, end):
                try:
                    ip_row = await page.query_selector_all(f'{ips}')
                    port_row = await page.query_selector_all(f'{ports}')
                    for iph, port in zip(ip_row, port_row):
                        ip = await (await iph.get_property('textContent')).json_value()
                        port = await (await port.get_property('textContent')).json_value()
                        iplist.append(f"{ip.strip()}:{port.strip()}\n")

                    await page.click(f'{next}')
                    now += 1
                except Exception as error2:
                    print(error2)


            with open('ip.txt', 'a', encoding='utf-8') as f:
                f.writelines(iplist)

            print('IP代理获取成功！')

            await browser.close()

    except Exception as error1:
        print(error1)


async def getiphappy():
    end = int(input('结束网页数:'))
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto('http://www.kxdaili.com/dailiip/1/1.html')

            now = 1
            iplist = []

            for _ in range(now, end):
                try:
                    ip_row = await page.query_selector_all('.active tbody tr td:nth-child(1)')
                    port_row = await page.query_selector_all('.active tbody tr td:nth-child(2)')
                    for iph, port in zip(ip_row, port_row):
                        ip = await (await iph.get_property('textContent')).json_value()
                        port = await (await port.get_property('textContent')).json_value()
                        iplist.append(f"{ip.strip()}:{port.strip()}\n")

                    now += 1
                    await page.goto(f'http://www.kxdaili.com/dailiip/1/{now}.html')

                except Exception as error2:
                    print(error2)


            with open('ip.txt', 'a', encoding='utf-8') as f:
                f.writelines(iplist)

            print('IP代理获取成功！')

            await browser.close()

    except Exception as error1:
        print(error1)


async def iptest(testpage,line):
        proxies = {
            'http': f'http://{line}',
            'https': f'https://{line}'
        }
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,verify_ssl=False)) as session:
                async with session.get(testpage,proxy=proxies['https'],timeout=600,ssl=False) as response:
                    if response.status == 200:
                        print(f"成功连接到代理 {line}")
                        with open('ipgood.txt','a',encoding='utf-8')as fg:
                            fg.write(f'{line}\n')
                    else:
                        print(f"连接失败，代理 {line} 不可用")
        except aiohttp.ClientError as e:
            print('https失败:',e)

        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64,verify_ssl=False)) as session:
                async with session.get(testpage,proxy=proxies['http'],timeout=600,ssl=False) as response:
                    if response.status == 200:
                        print(f"成功连接到代理 {line}")
                        with open('ipgood.txt','a',encoding='utf-8')as fg:
                            fg.write(f'{line}\n')
                    else:
                        print(f"连接失败，代理 {line} 不可用")
        except aiohttp.ClientError as e:
            print('http失败:',e)

async def main():
    testpage = input('待测试的网址：')
    tasks = []

    with open('ip.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            tasks.append(asyncio.create_task(iptest(testpage,line)))

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    for params1 in ip89:
        loop.run_until_complete(getip(*params1))

    for params2 in ipbee:
        loop.run_until_complete(getip(*params2))

    for params3 in ipcloud:
        loop.run_until_complete(getip(*params3))

    loop.run_until_complete(getiphappy())
    loop.close()

    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)
    asyncio.run(main())



