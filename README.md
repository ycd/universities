

![](https://img.shields.io/github/stars/ycd/universities?style=for-the-badge)
![](https://img.shields.io/github/forks/ycd/universities?style=for-the-badge)
![](https://img.shields.io/github/issues/ycd/universities?style=for-the-badge)
![](https://img.shields.io/github/license/ycd/universities?style=for-the-badge)
![](https://img.shields.io/bitbucket/pr/ycd/universities?style=for-the-badge)

<img src="docs/photo.png" width=700>


## Universities is free & open source API service. :school_satchel:
   
## Features :rocket:

* **Python <a href="https://github.com/tiangolo/fastapi" class="external-link" target="_blank">**FastAPI**</a> backend.** :hammer:
* **SQLAlchemy** - models :bar_chart:
* **Asynchronous** - Thanks to Uvicorn **Universities API** comes with a incredibly fast ASGI server, :rocket:
* **Large database** - Supports over +140 countries +9600 Universities :satellite:
* **Documentation** - Have an automatic API documentation web user interface thanks to FastAPI
* **Open source** - Everything from the code base is opensource and free to use under a permissive MIT license.

## Try it online with the [Documentation](https://universitiesapi.herokuapp.com) now! 

## How to use & query parameters :bulb:
### You can search by:
* **Country**             ```/search?country=India``` or ```/search?country=United+States```
* **Name**                ```/search?name=harvard``` 
* **Alpha_two_code**      ```/search?alpha_two_code=FR```
* **Domain**              ```/search?domain=uni-muenchen.de```

### Multiple querying & Auto completion
* **Name** and **Country** ```/search?country=Brazil&name=Centro```
* **Name** and **Alpha_two_code** ```/search?name=oxford&alpha_two_code=gb```

### Example Response 
```JSON
{
    "name": "Ludwig-Maximilians-Universität München",
    "alpha_two_code": "DE",
    "country": "Germany",
    "web_pages": [
      "http://www.uni-muenchen.de/"
    ],
    "domains": [
      "uni-muenchen.de"
    ],
    "state_province": null
}
```


## For Installation :pushpin:
```shell
git clone https://github.com/ycd/universities.git
cd universities
virtulenv env
source env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## License

This project is licensed under the terms of the MIT license.
