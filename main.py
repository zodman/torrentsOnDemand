import aiohttp
import asyncio
import lxml.html
from magnet2torrent import Magnet2Torrent
from scrap import main as scrap
import tqdm
import tabulate

URL = "https://nyaa.si/?&q=puya&p={}"


async def task(item, session):
    td = item.xpath("./td")
    title = td[1].text_content().strip()
    magneturi = td[2].xpath("./a[2]/@href").pop()
    m = Magnet2Torrent(magneturi)
    infohash = m.infohash.hex()
    result = await scrap(session, {"title": title, "infohash": infohash})
    return result

async def pretask(item):
    s = lambda x,y: x.get("stats", {}).get(y,"")
    return {
        "title": item.get("title"),
#        "hash": item.get("infohash"),
        "complete": s(item, "complete"),
        "seeds": s(item, "seeds"),
        "peers": s(item, "peers"),
    }.values()



async def main():
    results = []
    tasks = []
    async with aiohttp.ClientSession() as session:
        for page in tqdm.tqdm(range(0, 20), desc="Pages"):
            result = await session.get(URL.format(page))
            page_content = await result.text()
            root = lxml.html.fromstring(page_content)
            items = root.xpath("//table/tbody/tr")
            for i in items:
                tasks.append(task(i, session))
        for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks),
                               desc="Executing task"):
            results.append(await pretask(await f))
    print(tabulate.tabulate(results, headers=["title", "complete", "seeds", "peers"]))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
