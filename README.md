# TastyTrails Food Delivery App - Backend

Welcome to the backend repository for **TastyTrails**, your ultimate guide to delightful culinary experiences! This backend is built using the Django REST framework and provides all the necessary APIs for user management, menu browsing, detailed menu viewing, cart management, and order processing.

## Features

### User Management
- **User Registration**: New users can register an account.
- **User Login**: Existing users can log in using their credentials.
- **User Logout**: Users can log out of their account.
- **User Profile**: Users can view their profile information.

### Menu Browsing and Categories
- **Home Page**: Users can browse through a list of available menu items.
- **Menu**: Click on a restaurant to view its menu and other details.
- **Product Details**: Users can view details of specific products.
- **Menu Categories**: Filter items by categories.

### Favourite Management
- **Save as Favourite**: Users can add a menu item to their favourites.
- **Remove from Favourites**: Users can remove a menu item from their favourites list.

### Cart Management and Orders
- **Add to Cart**: Users can add items to their cart from the menu.
- **View Cart**: Users can view the items added to their cart.
- **Edit Cart**: Users can modify the quantity of items in their cart or remove items.
- **Checkout**: Users can proceed to purchase the items in their cart.
- **Order**: Users can place an order for the items in their cart.

---

## API Endpoints

**Backend API Base URL**: `https://tasty-trails-server.onrender.com`

### User Management
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login/` - User login
- `GET /api/auth/logout/` - User Logout
- `GET /users/:id/` - User Profile

### Menu Category
- `GET /category/list/` - List all menu categories
- `GET /category/list/:id` - Get details of a specific menu category

### Menu Browsing
- `GET /menu/list/` - List all menu items
- `POST /menu/list/` - Add new menu item
- `GET /menu/list/:id/` - Get details of a specific menu item
- `DELETE /menu/list/:id/` - Delete a specific menu item
- `GET /menu/list/?search=” ”` - Filter the menu by category

### Favourite Menu
- `GET /menu/favourite/` - List all favourite menu items
- `POST /menu/favourite/` - Add a menu item to favourites
- `DELETE /menu/favourite/:id/` - Remove a menu item from favourites
- `GET /menu/favourite/?user_id=2` - User-specific favourite menu list

### Cart Management
- `GET /carts/list/` - View all cart items
- `GET /carts/list/?user_id=” ”` - View cart for a specific user
- `POST /carts/list/` - Add item to cart
- `PUT /carts/list/:id/` - Update cart item
- `DELETE /carts/list/:id/` - Remove item from cart
- `GET /carts/checkout/` - Cart checkout details

### Order Management
- `GET /orders/list/` - View all orders
- `POST /orders/list/` - Place an order
- `PATCH /orders/list/:id/` - Update order status
- `GET /orders/list/:id/` - Get details of a specific order
- `GET /orders/list/?user_id=” ”` - Get specific user’s order
- `GET /orders/items/?order_id=” ”` - Get specific order items

---

## Prerequisites
- Python 3.x
- Django
- Django REST framework

## Installation

1. **Clone the repository**
 ```sh
   git clone https://github.com/Rafiul29/tasty-trails-server.git
```
2. **Navigate to the project directory**
```sh
cd tasty-trails-server
```
3. **Create a virtual environment**
```sh
python3 -m venv venv
```
4. **Activate the virtual environment**
```sh
source venv/bin/activate
```
5. **Install dependencies**
```sh
pip install -r requirements.txt
```
6. **Set up environment variables**
- Create a .env file in the root directory and add the following variables:
```sh
EMAIL_HOST=
EMAIL_PASSWORD=
APP_LOGIN_URL=
APP_REGISTER_URL=
APP_VERIFIED_URL=
```
7. **Run migrations**
 ```sh
python manage.py migrate
```
8. **Start the server**
```sh
python manage.py runserver
```
### Running the App
The server will be running on http://localhost:8000/
