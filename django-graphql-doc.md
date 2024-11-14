Here's the GraphQL schema and queries/mutations converted into Markdown for documentation purposes:

---

# E-Commerce GraphQL API Documentation

This document outlines the queries and mutations used in the E-Commerce GraphQL API.

---

## Inventory Management

### Update Inventory Quantity
Updates the inventory of a specific product.

```graphql
mutation UpdateInventory($product_id: String = "", $quantity: Int = -10) {
    update_ECommerce_inventory(where: {product_id: {_eq: $product_id}}, _inc: {quantity: $quantity}) {
        returning {
            quantity
            product_id
            updated_at
        }
    }
}
```

### Add to Inventory
Adds a new product to the inventory with an initial quantity.

```graphql
mutation AddToInventory($product_id: String = "", $quantity: Int = 10) {
    insert_ECommerce_inventory(objects: {product_id: $product_id, quantity: $quantity}) {
        returning {
            product_id
            quantity
            updated_at
        }
    }
}
```

### Reduce Inventory
Decreases the inventory quantity of a specified product.

```graphql
mutation ReduceInventory($product_id: String = "", $quantity: Int = -10) {
    update_ECommerce_inventory(where: {product_id: {_eq: $product_id}}, _inc: {quantity: $quantity}) {
        returning {
            quantity
            product_id
            updated_at
        }
    }
}
```

### Set Inventory Quantity
Sets the inventory quantity to a specific value for a product.

```graphql
mutation SetInventoryQuantity($product_id: String = "", $quantity: Int = 0) {
    update_ECommerce_inventory(where: {product_id: {_eq: $product_id}}, _set: {quantity: $quantity}) {
        returning {
            quantity
            product_id
            updated_at
        }
    }
}
```

### Get Inventory by Product ID
Fetches inventory details for a specific product.

```graphql
query GetInventoryByProductID($product_id: String = "") {
    ECommerce_inventory(where: {product_id: {_eq: $product_id}}) {
        quantity
    }
}
```

---

## Product and Category Retrieval

### Get All Products
Retrieves a list of all products in the catalog.

```graphql
query GetAllProducts {
    products {
        _id
        category_id
        created_at
        description
        images
        name
        price
        updated_at
    }
}
```

### Get All Categories
Fetches all available categories.

```graphql
query GetAllCategories {
    categories {
        _id
        created_at
        description
        name
        updated_at
    }
}
```

---

## Cart Management

### Add to Cart
Adds a specified quantity of a product to the user's cart.

```graphql
mutation AddToCart($product_id: String = "", $cart_id: uuid = "", $quantity: Int = 10) {
    insert_ECommerce_cart_items(objects: {product_id: $product_id, cart_id: $cart_id, quantity: $quantity}) {
        returning {
            cart {
                id
                cart_items {
                    id
                    product_id
                    quantity
                }
            }
        }
    }
}
```

### Remove from Cart
Removes a product from the cart based on `cart_id` and `product_id`.

```graphql
mutation RemoveFromCart($cart_id: uuid = "", $product_id: String = "") {
    delete_ECommerce_cart_items(where: {_and: {cart_id: {_eq: $cart_id}, product_id: {_eq: $product_id}}}) {
        returning {
            cart {
                id
                cart_items {
                    product_id
                    quantity
                }
            }
        }
    }
}
```

### Create Cart
Creates a new cart for a specific user.

```graphql
mutation CreateCart($user_id: uuid = "") {
    insert_ECommerce_carts(objects: {user_id: $user_id}) {
        returning {
            id
        }
    }
}
```

### Get Cart Items
Retrieves items in a user's cart.

```graphql
query GetCartItems($user_id: uuid = "") {
    ECommerce_carts(where: {user_id: {_eq: $user_id}}) {
        cart_items {
            id
            product_id
            quantity
        }
    }
}
```

---

## Order Management

### Place Order
Places an order with items and payment details.

```graphql
mutation PlaceOrder(
    $items: [ECommerce_order_items_insert_input!] = {},
    $payment_info: [ECommerce_payments_insert_input!] = {},
    $user_id: uuid = "",
    $status: String = "",
    $total_amount: numeric = "",
    $payment_status: String = ""
) {
    insert_ECommerce_orders(
        objects: {
            order_items: {data: $items},
            payments: {data: $payment_info},
            user_id: $user_id,
            status: $status,
            total_amount: $total_amount,
            payment_status: $payment_status
        }
    ) {
        returning {
            id
            order_items {
                id
                price
                product_id
                quantity
            }
            payments {
                id
                amount
                payment_method
                payment_status
            }
        }
    }
}
```

### View Orders
Fetches the order history for a user.

```graphql
query ViewOrders($user_id: uuid = "") {
    ECommerce_orders(where: {user_id: {_eq: $user_id}}) {
        id
        order_items {
            product_id
            price
            quantity
        }
        payment_status
        shipping_address
        status
        total_amount
        created_at
        updated_at
    }
}
```

--- 

This concludes the documentation for the GraphQL API for E-Commerce. Each query and mutation can be used to interact with the cart, inventory, products, and orders of the system.