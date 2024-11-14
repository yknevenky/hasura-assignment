## Product and Category Schema Documentation

This document describes the MongoDB schema for two collections: **Products** and **Categories**. These schemas define the structure and constraints for the documents within these collections, ensuring data integrity and consistency when inserting or updating documents.

### Overview

- **Products Collection**: Stores information related to the products in the inventory.
- **Categories Collection**: Stores details about product categories.

---

### Products Collection Schema

The `Products` collection stores details about individual products, including the product name, description, price, category, variants, images, and timestamps.

#### Validation Schema for `Products`

```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": [
      "name",
      "price",
      "category_id"
    ],
    "properties": {
      "name": {
        "bsonType": "string",
        "description": "Product name must be a string and is required"
      },
      "description": {
        "bsonType": "string",
        "description": "Product description must be a string"
      },
      "price": {
        "bsonType": "decimal",
        "description": "Product price must be a decimal number"
      },
      "category_id": {
        "bsonType": "objectId",
        "description": "category_id must be an ObjectId referencing the Categories collection"
      },
      "variants": {
        "bsonType": "array",
        "items": {
          "bsonType": "object",
          "properties": {
            "variant_name": {
              "bsonType": "string",
              "description": "Variant name must be a string"
            },
            "variant_value": {
              "bsonType": "string",
              "description": "Variant value must be a string"
            }
          },
          "description": "Each item in the variants array must contain variant_name and variant_value"
        },
        "description": "Variants should be an array of objects with variant_name and variant_value"
      },
      "images": {
        "bsonType": "array",
        "items": {
          "bsonType": "string",
          "description": "Each image URL must be a string"
        },
        "description": "Images should be an array of URLs"
      },
      "created_at": {
        "bsonType": "date",
        "description": "Creation date must be a valid date"
      },
      "updated_at": {
        "bsonType": "date",
        "description": "Updated date must be a valid date"
      }
    }
  }
}
```

#### Fields

- **`name`**: (Required) A string representing the product's name.
- **`description`**: (Optional) A string that describes the product.
- **`price`**: (Required) A decimal representing the price of the product.
- **`category_id`**: (Required) An `ObjectId` referencing the category in the **Categories** collection.
- **`variants`**: (Optional) An array of objects, each representing a variant of the product, with a `variant_name` and `variant_value`.
- **`images`**: (Optional) An array of strings, each representing a URL to an image associated with the product.
- **`created_at`**: (Optional) A `date` field representing when the product was created.
- **`updated_at`**: (Optional) A `date` field representing when the product was last updated.

---

### Categories Collection Schema

The `Categories` collection stores details about the categories to which products belong. Each category can have a name, description, and timestamps.

#### Validation Schema for `Categories`

```json
{
  "$jsonSchema": {
    "bsonType": "object",
    "required": [
      "name"
    ],
    "properties": {
      "name": {
        "bsonType": "string",
        "description": "Category name must be a string and is required"
      },
      "description": {
        "bsonType": "string",
        "description": "Category description must be a string if provided"
      },
      "created_at": {
        "bsonType": "date",
        "description": "Creation date must be a valid date"
      },
      "updated_at": {
        "bsonType": "date",
        "description": "Updated date must be a valid date"
      }
    }
  }
}
```

#### Fields

- **`name`**: (Required) A string representing the name of the category.
- **`description`**: (Optional) A string that describes the category.
- **`created_at`**: (Optional) A `date` field representing when the category was created.
- **`updated_at`**: (Optional) A `date` field representing when the category was last updated.

---

### Summary of Key Constraints

| **Field**        | **Collection** | **Required** | **Type**             | **Description**                                                           |
|------------------|----------------|--------------|----------------------|---------------------------------------------------------------------------|
| `name`           | Product, Category | Yes          | String               | The name of the product/category.                                         |
| `description`    | Product, Category | No           | String               | A detailed description of the product/category.                           |
| `price`          | Product        | Yes          | Decimal              | The price of the product.                                                 |
| `category_id`    | Product        | Yes          | ObjectId             | Reference to the Category collection.                                     |
| `variants`       | Product        | No           | Array of Objects     | Variants of the product, each containing `variant_name` and `variant_value`.|
| `images`         | Product        | No           | Array of Strings     | URLs of images associated with the product.                               |
| `created_at`     | Product, Category | No           | Date                 | Timestamp when the product/category was created.                          |
| `updated_at`     | Product, Category | No           | Date                 | Timestamp when the product/category was last updated.                     |

---

### Example MongoDB Command to Create Collections with Validation

```javascript
// Create Product Collection with Schema Validation
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "price", "category_id"],
      properties: {
        name: { bsonType: "string" },
        description: { bsonType: "string" },
        price: { bsonType: "decimal" },
        category_id: { bsonType: "objectId" },
        variants: {
          bsonType: "array",
          items: {
            bsonType: "object",
            properties: {
              variant_name: { bsonType: "string" },
              variant_value: { bsonType: "string" }
            }
          }
        },
        images: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  }
});

// Create Category Collection with Schema Validation
db.createCollection("categories", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name"],
      properties: {
        name: { bsonType: "string" },
        description: { bsonType: "string" },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  }
});
```

This document ensures that both **Products** and **Categories** collections have a predefined structure, ensuring data consistency and preventing incorrect data from being inserted.