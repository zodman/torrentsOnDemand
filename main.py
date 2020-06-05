import aiohttp
import asyncio
import lxml.html
from magnet2torrent import Magnet2Torrent
from scrap import main as scrap
from tabulate import tabulate


URL = "https://nyaa.si/?&q=puya&p={}"

async def main():
    table = []
    async with aiohttp.ClientSession() as session:
        for page in range(0, 20):
            result = await session.get(URL.format(page))
            page_content = await result.text()
            root = lxml.html.fromstring(page_content)
            items = root.xpath("//table/tbody/tr")
            for i in items:
                td = i.xpath("./td")
                title = td[1].text_content().strip()
                magneturi = td[2].xpath("./a[2]/@href").pop()
                m = Magnet2Torrent(magneturi)
                infohash = m.infohash.hex()
                result = await scrap(session, infohash)
                table.append(list(result.items()) + ['name',title])
    print(tabulate(table))




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
        
