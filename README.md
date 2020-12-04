# An Item Based Recommender (for [Jumia](https://www.jumia.com.ng) links)

This projects implements an item-based recommender using HDBSCAN clustering. Product data, gotten from [Jumia](https://www.jumia.com.ng) was used to fit (train) the cluster model.

Details on setup, usage and limitations are given in subsequent sections.
HDBSCAN stands for Hierarchical Density-Based Spatial Clustering of Applications with Noise.

## Setup

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the project requirements.

```bash
pip install -r requirements.txt
```
There might be an error when installing the hdbscan library. If that happens, it could be downloaded through its [GitHub page] (https://github.com/scikit-learn-contrib/hdbscan). After that, it could be installed by running the following:

```bash
pip install -r requirements.txt
python setup.py install
```
After this a database is required to be setup. The configuration could be found in the file **sql_database.py**. Suitable values could be filled in. Please make sure the database filled in already exists.

```python
#sql_database.py

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='0011',
    database='recommender_db'
)
```
After that the file (**sql_database.py**) should be run to create the tables and populate the relevant one.

## Usage

The project is implemented as a web application (without a front end) that returns JSON responses. The server can be started by running the **python app.py** command as shown:
```bash
C:\Users\project_directory>python app.py

* Serving Flask app "app" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
Interaction with the web application involves making a request as shown below:

```json
http://localhost:5000/api/recommend
```
### Parameters

Name| Description | Required | Example 
--- | --- | --- | ---  
**link** | A Jumia product page URL. Similar products are recommended based on this. | required | https://www.jumia.com.ng/style-addiction-mesh-sleeve-belted-skater-dress-red-59493603.html
**phone** | Phone number of the link requestor. It is stored in the database and can be used for the implementation of a user-based recommendation system. | optional | 08123092414

### Request Example
```json
http://localhost:5000/api/recommend?link=https://www.jumia.com.ng/style-addiction-mesh-sleeve-belted-skater-dress-red-59493603.html?phone=08123092414
```
### Response Example
```json
[
    {
        "id": 5662,
        "image_link": "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/27/831034/1.jpg?4255",
        "product_brand": "Style Addiction",
        "product_link": "/style-addiction-faux-button-down-skater-dress-blue-43013872.html",
        "product_name": "Style Addiction Faux Button Down Skater Dress - Blue",
        "product_price": " 3799",
        "product_rating": "3.7",
        "product_type": "Dresses"
    },
    {
        "id": 6015,
        "image_link": "https://ng.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/74/281415/1.jpg?9417",
        "product_brand": "",
        "product_link": "/fashion-classy-formal-design-dress-black-and-red.-51418247.html",
        "product_name": "Classy Formal Design  Dress- Black And Red.",
        "product_price": " 4250",
        "product_rating": "3.8",
        "product_type": "Dresses"
    }
]
```
Also, if no recommendation is found, the following response is returned:
```json
{
    "status": "No recommendations are available for the given link"
}
```
There will also be an error message if the URL is not a valid Jumia link as seen below:
```json
{
    "error": "url not valid"
}
```
## Limitations
The training of the model relied on vectors from the names and categories
of the products. The dimensions of the vectors were then reduced drastically in order to save training time and memory.
In addition, the data mined was relatively noisy with inconsistencies in product classifications and naming conventions.\
These factors led to a relatively high amount of product vector points classified as noise or outlier values.

Overall, trade-offs had to be made between training time based on computational resources, runtime performance, and accuracy. On a good note, if a product is classified and not considered as noise, the classification would be within a very reasonable acceptance level.

A more ideal recommendation system would implement collaborative filtering based on user data, and the relationships between users and the products they interact with. This was not possible in this case, as user data was not available.
