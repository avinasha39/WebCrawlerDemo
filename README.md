# WebCrawalerRepo

A web crawler with a python scrapy framework.


## Installation

Use the package manager [pip] to install all dependencies scrapy framework which is added in requirement.txt.

```bash
python -m venv
pip install -r requirements.txt
```

## Usage

```python
Open CLI inside the folder WebCrawler Demo

To get data from Flipkart.com run the following command:
scrapy crawl flipkart_product_info -a domain='url of website'
or
scrapy crawl flipkart_product_info -a domain='url of a particular product whose info is needed'


To get data from Shopclues.com run the following command:
scrapy crawl shopclues_product_info -a domain='url of website'
or
scrapy crawl shopclues_product_info -a domain='url of a particular product whose info is needed'


```
## Result
After successful scrapping data will be saved in 'CSV file format inside the 'Data' folder, in the parent directory.

## Contributing
Pull requests are welcome. For changes, please open an issue first to discuss what you would like to 
