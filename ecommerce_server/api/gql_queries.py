update_inventory_query = """
    mutation MyMutation($product_id: String = "", $quantity: Int = -10) {
        update_ECommerce_inventory(where: {product_id: {_eq: $product_id}}, _inc: {quantity: $quantity}) {
            returning {
            quantity
            product_id
            updated_at
            }
        }
    }
"""

add_to_cart_mutation = """
    mutation MyMutation($product_id: String = "", $cart_id: uuid = "", $quantity: Int = 10) {
        insert_ECommerce_cart_items(objects: {product_id: $product_id, cart_id: $cart_id, , quantity: $quantity}) {
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
"""

get_all_products = """
    query MyQuery {
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
"""

get_all_categories = """
    query MyQuery {
        categories {
            _id
            created_at
            description
            name
            updated_at
        }
    }
"""

remove_from_cart_mutation = """
    mutation MyMutation($cart_id: uuid = "", $product_id: String = "") {
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
"""

create_cart_mutation = """
    mutation MyMutation($user_id: uuid = "") {
        insert_ECommerce_carts(objects: {user_id: $user_id}) {
            returning {
                id
            }
        }
    }
"""

get_cart_items_query = """
    query MyQuery($user_id: uuid = "") {
        ECommerce_carts(where: {user_id: {_eq: $user_id}}) {
            cart_items {
            id
            product_id
            quantity
            }
        }
    }
"""

place_order_mutation = """
    mutation MyMutation($items: [ECommerce_order_items_insert_input!] = {}, $payment_info: [ECommerce_payments_insert_input!] = {}, $user_id: uuid = "", $status: String = "", $total_amount: numeric = "", $payment_status: String = "") {
        insert_ECommerce_orders(objects: {order_items: {data: $items}, payments: {data: $payment_info}, user_id: $user_id, status: $status, total_amount: $total_amount, payment_status: $payment_status}) {
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
"""

reduce_inventory_mutation = """
    mutation MyMutation($product_id: String = "", $quantity: Int = -10) {
        update_ECommerce_inventory(where: {product_id: {_eq: $product_id}}, _inc: {quantity: $quantity}) {
            returning {
                quantity
                product_id
                updated_at
            }
        }
    }
"""

add_to_inventory_mutation = """
    mutation MyMutation($product_id: String = "", $quantity: Int = 10) {
        insert_ECommerce_inventory(objects: {product_id: $product_id, quantity: $quantity}) {
            returning {
            product_id
            quantity
            updated_at
            }
        }
    }
"""

update_inventory_mutation = """
     mutation MyMutation($product_id: String = "", $quantity: Int = 0) {
        update_ECommerce_inventory(where: {product_id: {_eq: $product_id}}, _set: {quantity: $quantity}) {
            returning {
                quantity
                product_id
                updated_at
            }
        }
    }
"""

view_orders_mutation = """
    query MyQuery($user_id: uuid = "") {
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
"""

get_inventory_by_product_id = """
    query MyQuery($product_id: String = "") {
        ECommerce_inventory(where: {product_id: {_eq: $product_id}}) {
            quantity
        }
    }
"""