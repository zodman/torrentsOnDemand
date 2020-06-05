import binascii
import urllib.parse
import bencode

TRACKER_URL = "http://nyaa.tracker.wf:7777/announce"

async def main(session, info_hash):
    tracker_url = TRACKER_URL.replace("announce", "scrape")
    info = urllib.parse.quote_plus(binascii.unhexlify(info_hash))
    url = f"{tracker_url}?info_hash={info}"
    resp = await session.get(url)
    content = await resp.read()
    d = bencode.bdecode(content)
    ret = {}
    print(d)
    for hash, stats in d[b'files'].items():
        nice_hash = binascii.b2a_hex(hash).decode("utf-8")
        s = stats[b"complete"]
        p = stats[b"incomplete"]
        c = stats[b"downloaded"]
        ret[nice_hash] = {"seeds": s, "peers": p, "complete": c}
    return ret




