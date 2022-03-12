# Flask Live Corona Info

Live Corona statistics and information site with flask.

#
## Tools

- Flask
- Scrapy
- Matplotlib

#

# How to Run Project

## Download Codes

```
git clone https://github.com/dori-dev/flask-corona-info.git
```

```
cd flask-corona-info/
```

## Build Virtual Environment

```
python3 -m venv env
```

```
source env/bin/activate
```

## Install Project Requirements

```
pip install -r requirements.txt
```

## Use Flask to Run Project

```
flask run
```

## Use Python to Run Project

```
python app.py
```

## See Result

Open This Link in Your Browser: [127.0.0.1:5000](http://127.0.0.1:5000/)

#
# Project Tree

```
flask-corona-info
├── app.py
├── dictionary.py
├── get_info.py
├── README.md
├── requirements.txt
├── run_spider.py
├── scrapy.cfg
├── templates
│   └── index.html
├── static
│   ├── DB
│   │   ├── info_db.dat
│   │   ├── old_info_db.dat
│   │   └── plot.png
│   ├── font
│   │   └── IRANSansWeb.woff2
│   ├── img
│   │   ├── favicon.ico
│   │   ├── live.png
│   │   └── logo.png
│   └── style.css
└── corona_crawler
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders
        ├── __init__.py
        └── spider.py
```

#
## Links

Demo of Project: [corona-dori.herokuapp.com](https://corona-dori.herokuapp.com/)

Download Source Code: [Click Here](https://github.com/dori-dev/flask-corona-info/archive/refs/heads/master.zip)

My Github Account: [Click Here](https://github.com/dori-dev/)
