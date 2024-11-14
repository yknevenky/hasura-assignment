from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
import time
import jwt 
from django.conf import settings
import uuid
from .models import Product
from mongoengine import DoesNotExist
from datetime import datetime
from bson import ObjectId
from .serializers import ProductSerializer
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from .decorators import jwt_required 
from . import gql_queries

@api_view(['GET'])
def get_cart_items_by_user_id(request):
    return Response()

@api_view(['POST'])
def sign_up(request):
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
    user_id = str(uuid.uuid4())

    django_payload = {
        "sub": "django_server",
        "iat": int(time.time()),  
        "https://hasura.io/jwt/claims": {
            "x-hasura-default-role": "django",
            "x-hasura-allowed-roles": ["django"],
            "x-hasura-user-id": "django_server"
        }
    }

    django_token = jwt.encode(django_payload, settings.HASURA_SECRET_KEY, algorithm="ES256")
    if not email or not phone_number or not password:
        return Response({"error": "Email, phone number, and password are required."}, status=status.HTTP_400_BAD_REQUEST)
  
    external_api_data = {
        "id": user_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "password": password
    }
    
    try:
        external_response = requests.post("http://localhost:8080/api/rest/signup", json=external_api_data, headers={'authorization': 'Bearer ' + django_token})
        external_response_data = external_response.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": "Failed to connect to external service."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
   
   
    if 'error' in external_response_data:
        return Response(external_response_data, status=status.HTTP_400_BAD_REQUEST)
    if 'insert_ECommerce_users' not in external_response_data and 'affected_rows' not in external_response_data['insert_ECommerce_users'] and external_response_data['insert_ECommerce_users']['affected_rows'] == 1:
        return Response({"error": "Sign up failed."}, status=status.HTTP_400_BAD_REQUEST)
   
    payload = {
        "sub": user_id,
        "iat": int(time.time()),
        "https://hasura.io/jwt/claims": {
            "x-hasura-default-role": "user",
            "x-hasura-allowed-roles": ["user"],
            "x-hasura-user-id": user_id
        }
    }
    
    token = jwt.encode(payload, settings.HASURA_SECRET_KEY, algorithm="ES256")
    
    return Response({"token": token}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def sign_in(request):
   
    email = request.data.get("email")
    password = request.data.get("password")
    
   
    if not email or not password:
        return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    external_api_data = {
        "email": email,
        "password": password
    }

    django_payload = {
        "sub": "django_server",
        "iat": int(time.time()),  
        "https://hasura.io/jwt/claims": {
            "x-hasura-default-role": "django",
            "x-hasura-allowed-roles": ["django"],
            "x-hasura-user-id": "django_server"
        }
    }

    django_token = jwt.encode(django_payload, settings.HASURA_SECRET_KEY, algorithm="ES256")
    print(django_token)
    
    # Send data to the hasura authentication REST API
    try:
        external_response = requests.post("http://localhost:8080/api/rest/signin", json=external_api_data, headers={'authorization': 'Bearer ' + django_token})
        external_response_data = external_response.json()
    except requests.exceptions.RequestException as e:
        return Response({"error": "Failed to connect to external service."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    print(external_response_data)
    
    if 'error' in external_response_data:
        return Response(external_response_data, status=status.HTTP_400_BAD_REQUEST)
    if 'ECommerce_users' not in external_response_data and 'id' not in external_response_data['ECommerce_users'][0]:
        return Response({"error": "Sign up failed."}, status=status.HTTP_400_BAD_REQUEST)
    data = external_response_data["ECommerce_users"][0]
    user_id = data['id']  
    
    # Generate a JWT token with hasura payload
    payload = {
        "sub": user_id,
        "iat": int(time.time()),  # Issued at the current time
        "https://hasura.io/jwt/claims": {
            "x-hasura-default-role": "user",
            "x-hasura-allowed-roles": ["user"],
            "x-hasura-user-id": user_id
        }
    }
    
    # Encode the token
    token = jwt.encode(payload, settings.HASURA_SECRET_KEY, algorithm="ES256")
    
    user_data = {
        "id": data["id"],
        "first_name": data.get("first_name", ""),
        "last_name": data.get("last_name", ""),
        "phone_number": data.get("phone_number", ""),
        "email": data.get("email", ""),
        "address": data.get("address", ""),
        "token": token
    }
   
    
    return Response({
        
        "user": user_data  
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@jwt_required
def get_all_products(request):
    
    query = gql_queries.get_all_products

    variables = {
      
    }

    headers = {
        "Authorization": request.headers.get("Authorization"),
         'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': query,
                'variables': variables
            },
            headers=headers
        )
        
        data = response.json()
        

        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data)
        
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to fetch products: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def add_product(request):
      
    serializer = ProductSerializer(data=request.data)
    
    if serializer.is_valid(): 
        product = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product, data=request.data)

    if serializer.is_valid(): 
        serializer.save(updated_at=datetime.now()) 
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=ObjectId(product_id))
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)

    except DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@jwt_required
def get_all_categories(request):
    
    query = gql_queries.get_all_categories
    
    variables = {
    }
    
    headers = {
        "Authorization": request.headers.get("Authorization"),
         'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': query,
                'variables': variables
            },
            headers=headers
        )
        
        data = response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(data)
        
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to fetch categories: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def add_category(request):
    serializer = CategorySerializer(data=request.data)
    
    if serializer.is_valid():  
        
        category = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data)

    if serializer.is_valid():  
        serializer.save(updated_at=datetime.now())  
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@jwt_required
def add_cart_item(request):

    product_id = request.data.get("product_id")
    cart_id = request.data.get("cart_id")
    quantity = request.data.get("quantity", 10)

    if not product_id or not cart_id:
        return Response(
            {"error": "Both 'product_id' and 'cart_id' are required fields and cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )

    query = gql_queries.add_to_cart_mutation
    
    variables = {
       "product_id": product_id,
        "cart_id": cart_id,
        "quantity": int(quantity)
    }
    

    headers = {
        "Authorization": request.headers.get("Authorization"),
         'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': query,
                'variables': variables
            },
            headers=headers
        )
        
        data = response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(data['data']['insert_ECommerce_cart_items']['returning'])
        
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to fetch products: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['DELETE'])
@jwt_required
def remove_cart_item(request):
    product_id = request.data.get("product_id")
    cart_id = request.data.get("cart_id")
   
    if not product_id or not cart_id:
        return Response(
            {"error": "Both 'product_id' and 'cart_id' are required fields and cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )

    query = gql_queries.remove_from_cart_mutation

    variables = {
       "product_id": product_id,
        "cart_id": cart_id,
    }
    
    headers = {
        "Authorization": request.headers.get("Authorization"),
         'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': query,
                'variables': variables
            },
            headers=headers
        )
        
        data = response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(data['data']['delete_ECommerce_cart_items']['returning'])
        
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to delete cart item: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@jwt_required
def create_cart(request):    
    user_id = request.data.get("user_id")

    if not user_id:
        return Response(
            {"error": "'user_id' is a required field and cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )

    query = gql_queries.create_cart_mutation

    variables = {       
        "user_id": user_id        
    }
    
    headers = {
        "Authorization": request.headers.get("Authorization"),
         'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': query,
                'variables': variables
            },
            headers=headers
        )

        data = response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(data['data']['insert_ECommerce_carts']['returning'])
        
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to create cart: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['POST'])
@jwt_required
def place_order(request):    
    user_id = request.data.get("user_id")
    payment_method = request.data.get("payment_method")
   
    if not user_id or not payment_method:
        return Response(
            {"error": "'user_id' and 'payment_method' are required fields and cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )

    headers = {
        "Authorization": request.headers.get("Authorization"),
         'Content-Type': 'application/json',
    }

    cart_items_query = gql_queries.get_cart_items_query

    cart_items_variables = {       
        "user_id": user_id        
    }

    place_order_query = gql_queries.place_order_mutation

    update_inventory_query = gql_queries.reduce_inventory_mutation

    try:
        cart_items_response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': cart_items_query,
                'variables': cart_items_variables
            },
            headers=headers
        )

        cart_items_data = cart_items_response.json()
        
        if 'errors' in cart_items_data:
            return Response(
                {'error': cart_items_data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
        print(cart_items_data)
        if not cart_items_data['data'].get('ECommerce_carts'):
            # If `ECommerce_carts` is empty or not present, return a custom error message
            return Response(
                {'error': 'No items found in the cart or cart does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = cart_items_data['data']['ECommerce_carts'][0]['cart_items']
        total_price = 0
        order_items = []
        for cart_item in cart_items:
            product_id = cart_item.get('product_id',"")
            product = Product.objects.get(id=product_id)
            price = product.price
            quantity = cart_item.get('quantity',0)
            total_price += price * quantity
            order_items.append({
                "product_id": product_id,
                "quantity": quantity,
                "price": float(price)
            })

            check_inventory_query = gql_queries.get_inventory_by_product_id
            check_inventory_variables = {
                "product_id": product_id,
            }

            check_inventory_response = requests.post(
                settings.GRAPHQL_END_POINT,
                json={
                    'query': check_inventory_query,
                    'variables': check_inventory_variables
                },
                headers = {
                    "Authorization": request.headers.get("Authorization"),
                    'Content-Type': 'application/json',
                }
            )

            check_inventory_data = check_inventory_response.json()

            
            # Check if `ECommerce_inventory` exists and is not empty
            if not check_inventory_data.get('data') or not check_inventory_data['data'].get('ECommerce_inventory'):
                # If `ECommerce_inventory` is empty, return an error message
                return Response(
                    {'error': 'Inventory not found for the specified product.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get the quantity from `ECommerce_inventory`
            available_quantity = check_inventory_data['data']['ECommerce_inventory'][0].get('quantity', 0)

            # Check if available quantity is less than the required quantity
            if available_quantity < quantity:
                return Response(
                    {'error': f'Insufficient inventory. Only {available_quantity} items are available.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            update_inventory_variables = {
                "product_id": product_id,
                "quantity": -quantity
            }

            django_payload = {
                "sub": "django_server",
                "iat": int(time.time()), 
                "https://hasura.io/jwt/claims": {
                    "x-hasura-default-role": "django",
                    "x-hasura-allowed-roles": ["django"],
                    "x-hasura-user-id": "django_server"
                }
            }

            django_token = jwt.encode(django_payload, settings.HASURA_SECRET_KEY, algorithm="ES256")
        
            update_inventory_response = requests.post(
                settings.GRAPHQL_END_POINT,
                json={
                    'query': update_inventory_query,
                    'variables': update_inventory_variables
                },
                headers={'authorization': 'Bearer ' + django_token}
            )

            update_inventory_data = update_inventory_response.json()
            if 'errors' in update_inventory_data:
                return Response(
                    {'error': update_inventory_data['errors'][0]['message']},
                    status=status.HTTP_400_BAD_REQUEST
                )

        place_order_variables = {   
            "user_id": user_id,    
            "items": order_items,
            "status": "placed",
            "total_amount": float(total_price),
            "payment_status": "completed",
            "payment_info": {
                "payment_method": payment_method,
                "payment_status": "completed",
                "amount": float(total_price)
            }        
        }

        place_order_response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': place_order_query,
                'variables': place_order_variables
            },
            headers=headers
        )

        data = place_order_response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(data['data'])

        
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to create cart: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def add_inventory(request):    
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity")

    django_payload = {
        "sub": "django_server",
        "iat": int(time.time()),  
        "https://hasura.io/jwt/claims": {
            "x-hasura-default-role": "django",
            "x-hasura-allowed-roles": ["django"],
            "x-hasura-user-id": "django_server"
        }
    }

    django_token = jwt.encode(django_payload, settings.HASURA_SECRET_KEY, algorithm="ES256")
   
    if not product_id or not quantity:
        return Response(
            {"error": "'product_id' and 'quantity' are required fields and cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )
    headers={'authorization': 'Bearer ' + django_token}

    add_inventory_query = gql_queries.add_to_inventory_mutation

    add_inventory_variables = {       
        "product_id": product_id,
        "quantity": quantity        
    }    
   

    try:
        inventory_response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': add_inventory_query,
                'variables': add_inventory_variables
            },
            headers=headers
        )

        data = inventory_response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(data['data'])

    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to add to the inventory: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
def update_inventory(request):    
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity")

    django_payload = {
        "sub": "django_server",
        "iat": int(time.time()),  
        "https://hasura.io/jwt/claims": {
            "x-hasura-default-role": "django",
            "x-hasura-allowed-roles": ["django"],
            "x-hasura-user-id": "django_server"
        }
    }

    django_token = jwt.encode(django_payload, settings.HASURA_SECRET_KEY, algorithm="ES256")
   
    if not product_id or not quantity:
        return Response(
            {"error": "'product_id' and 'quantity' are required fields and cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST
        )
    headers={'authorization': 'Bearer ' + django_token}

    update_inventory_query = gql_queries.update_inventory_mutation

    update_inventory_variables = {       
        "product_id": product_id,
        "quantity": quantity        
    }  
    try:
        inventory_response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': update_inventory_query,
                'variables': update_inventory_variables
            },
            headers=headers
        )

        data = inventory_response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data['data'])
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to create cart: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@jwt_required
def view_orders(request, user_id):
    view_orders_query = gql_queries.view_orders_mutation

    view_orders_variables = {       
        "user_id": user_id,    
    }  
    try:
        view_orders_response = requests.post(
            settings.GRAPHQL_END_POINT,
            json={
                'query': view_orders_query,
                'variables': view_orders_variables
            },
            headers = {
                "Authorization": request.headers.get("Authorization"),
                'Content-Type': 'application/json',
            }
        )

        data = view_orders_response.json()
        
        if 'errors' in data:
            return Response(
                {'error': data['errors'][0]['message']},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data['data']['ECommerce_orders'])
    except requests.RequestException as e:
        return Response(
            {'error': f'Failed to create cart: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

