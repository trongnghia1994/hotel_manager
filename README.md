A sample for RESTFul API web services
============

* RESTFul API web services with Python 2.7.x, flask, flask-restplus
* Check user *login required* and *permission required* via decorators
* Login, logout via populating Flask session and use JWT token
* Connect to MongoDb on MongoAtlas, use pymodm as model framework
* Self-documented with Swagger. Documentation for API version 1 is available at /api/v1/docs, for example http://localhost:5000/api/v1/docs

Examples:
1. Search available rooms:  
GET /api/v1/roomInventories/availableItems?hotel_id=5d5ff40668a3ff060c2df835&checkIn=2019-08-25T00%3A00%3A00.000Z&checkOut=2019-08-26T00%3A00%3A00.000Z&adults=2
2. Create reservations  
POST /api/v1/reservations
3. Login, get token  
POST /api/v1/auth/login
4. Logout  
POST /api/v1/auth/login  
Header: Authorization ...  
(pass token in *Authorization* header)     
5. Create room inventory (Permission *inventory.add* required)  
POST /api/v1/roomInventories    
Header: Authorization ...   
(pass token in *Authorization* header)  
...

Test users:  
1. superuser: all permissions  
	super_user@gmail.com 123456	
2. admin: all permissions  
	admin@gmail.com 123456
3. manager: all permissions except user permission  
	manager@gmail.com 123456
4. user: accommodation permissions  
	user@gmail.com 123456

**How to run:**  
Simply **python app.py**
