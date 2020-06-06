Small application for check the torrents what need seed.

This small app it is scrape the torrents from a nyaa torrent. Then parse the magneturi
to get the hashinfo of the torrent. Then goes to the tracker and extract the realtime stats for that infohash.


Using aiolibs, we put a queue all task, the task it's a small function what parse the data and fetch the info from the tracker.

The app fired all torrents to the same time.


```

+----------+             +-----------+           +-----------+           +---------------------------+
|          |             |           |           |           |           |                           |
|  Page 1  |  -------->  |   Page 2  |-------->  |   Page N  |  ----->   |  Execute task on parallel |
|          |             |           |           |           |           |                           |
+----------+             +-----------+           +-----------+           +---------------------------+




 +-----------+          +-----------+           +-----------+
 |           |          |           |           |           |
 | taskQueue |          | taskQueue |           | taskQueue |
 |           |          |           |           |           |
 | 0         |          | 75        |           | 75*N      |
 |           |          |           |           |           |
 |           |          |           |           |           |
 |           |          |           |           |           |
 +-----------+          +-----------+           +-----------+


```


## Install

    python3.8 -m venv .env
    source .env/bin/activate
    pip install -r requirements.txt
    python main.py

## Demo

[![asciicast](https://asciinema.org/a/337147.svg)](https://asciinema.org/a/337147)
