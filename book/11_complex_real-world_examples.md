## **Chapter 11: Complex Real-World Examples**

You have mastered the operators and learned the fundamental patterns. Now it is time to put it all together. This chapter walks through a single, complex, real-world problem from start to finish. We will not introduce any new operators. Instead, we will focus on how the tools you already know can be composed to build a sophisticated, multi-stage data transformation pipeline.

### The Scenario: E-commerce Order Processing

Imagine we are building the backend for an e-commerce platform. When a customer places an order, our system receives a single, rich JSON object representing that order. Our task is to process this object and generate **three distinct outputs** for different downstream systems:

1.  **A Customer Invoice:** A simplified object containing the customer's details, the items purchased with calculated subtotals, and a final grand total including tax.
2.  **A Shipping Manifest:** A document for the warehouse containing the customer's shipping address and a list of only the *physical* items to be packed, including their SKUs and quantities.
3.  **An Inventory Update:** A list of operations for the inventory system, detailing which SKUs need their stock levels decremented.

This is a perfect example of a **Forking Pipeline**, where each fork (`invoice`, `shipping`, `inventory`) will require its own unique transformation logic.

### The Input Data

Here is the raw order data we'll be working with. Note that it contains a mix of physical and digital goods.

**`order_input.json`:**
```json
{
  "order_id": "ord-112233",
  "customer": {
    "user_id": "u-456",
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "shipping_address": {
      "street": "123 Quantum Lane",
      "city": "Photon Creek",
      "zip": "98765",
      "country": "USA"
    }
  },
  "line_items": [
    { "item_id": "prod-xyz-789", "sku": "QC-TS-M-BLUE", "name": "Quantum T-Shirt", "quantity": 1, "price_cents": 2999, "physical": true },
    { "item_id": "prod-abc-456", "sku": "QC-MUG-BLACK", "name": "Flux-Capacitor Mug", "quantity": 2, "price_cents": 1550, "physical": true },
    { "item_id": "dig-001", "sku": "EBOOK-COMPUTO", "name": "Computo: The Ultimate Guide", "quantity": 1, "price_cents": 999, "physical": false }
  ],
  "tax_rate_percent": 8
}
```

### The Plan of Attack

Our top-level output will be a single JSON object with three keys: `invoice`, `shipping_manifest`, and `inventory_updates`.

1.  **`invoice`:** We will need to map over the `line_items`, calculate a `subtotal_cents` for each, and then `reduce` them to calculate a `grand_total_cents` after applying tax.
2.  **`shipping_manifest`:** We must first `filter` the `line_items` to get only those where `physical` is `true`. Then, we'll `map` that filtered list into the simple format the warehouse needs.
3.  **`inventory_updates`:** This will be similar to the shipping manifest, but it will produce a list of decrement operations.

### The Complete Transformation Script

This script is the most complex we've written, but by using `let` to break down the problem, it remains readable.

**`process_order.json`:**
```json
["let",
  [
    ["order", ["$input"]],
    ["items", ["get", ["$", "/order"], "/line_items"]],
    ["physical_items", ["filter", ["$", "/items"], ["lambda",["i"],["get",["$","/i"],"/physical"]]]]
  ],
  ["obj",
    ["invoice",
      ["let",
        [
          ["items_with_subtotals",
            ["map", ["$", "/items"],
              ["lambda", ["item"],
                ["merge", ["$", "/item"],
                  ["obj", ["subtotal_cents", ["*",["get",["$","/item"],"/quantity"],["get",["$","/item"],"/price_cents"]]]]]
                ]
              ]
            ]
          ],
          ["pre_tax_total", ["reduce", ["$", "/items_with_subtotals"], ["lambda",["acc","i"],["+",["$","/acc"],["get",["$","/i"],"/subtotal_cents"]]], 0]]
        ],
        ["obj",
          ["customer_name", ["get", ["$", "/order"], "/customer/name"]],
          ["items", ["$", "/items_with_subtotals"]],
          ["grand_total_cents",
            ["+",
              ["$", "/pre_tax_total"],
              ["*", ["$", "/pre_tax_total"], ["/", ["get", ["$", "/order"], "/tax_rate_percent"], 100]]
            ]
          ]
        ]
      ]
    ],
    ["shipping_manifest",
      ["obj",
        ["order_id", ["get", ["$", "/order"], "/order_id"]],
        ["shipping_address", ["get", ["$", "/order"], "/customer/shipping_address"]],
        ["items_to_pack",
          ["map", ["$", "/physical_items"],
            ["lambda", ["item"],
              ["obj",
                ["sku", ["get", ["$", "/item"], "/sku"]],
                ["quantity", ["get", ["$", "/item"], "/quantity"]],
                ["description", ["get", ["$", "/item"], "/name"]]
              ]
            ]
          ]
        ]
      ]
    ],
    ["inventory_updates",
      ["map", ["$", "/physical_items"],
        ["lambda", ["item"],
          ["obj",
            ["action", "DECREMENT_STOCK"],
            ["sku", ["get", ["$", "/item"], "/sku"]],
            ["by_quantity", ["get", ["$", "/item"], "/quantity"]]
          ]
        ]
      ]
    ]
  ]
]
```

### The Final Output

Running the script produces a single, comprehensive JSON object with all three required outputs, each perfectly structured for its destination.

```json
{
  "inventory_updates": [
    { "action": "DECREMENT_STOCK", "by_quantity": 1, "sku": "QC-TS-M-BLUE" },
    { "action": "DECREMENT_STOCK", "by_quantity": 2, "sku": "QC-MUG-BLACK" }
  ],
  "invoice": {
    "customer_name": "Jane Doe",
    "grand_total_cents": 7666.92,
    "items": [
      { "item_id": "prod-xyz-789", "name": "Quantum T-Shirt", "physical": true, "price_cents": 2999, "quantity": 1, "sku": "QC-TS-M-BLUE", "subtotal_cents": 2999 },
      { "item_id": "prod-abc-456", "name": "Flux-Capacitor Mug", "physical": true, "price_cents": 1550, "quantity": 2, "sku": "QC-MUG-BLACK", "subtotal_cents": 3100 },
      { "item_id": "dig-001", "name": "Computo: The Ultimate Guide", "physical": false, "price_cents": 999, "quantity": 1, "sku": "EBOOK-COMPUTO", "subtotal_cents": 999 }
    ]
  },
  "shipping_manifest": {
    "items_to_pack": [
      { "description": "Quantum T-Shirt", "quantity": 1, "sku": "QC-TS-M-BLUE" },
      { "description": "Flux-Capacitor Mug", "quantity": 2, "sku": "QC-MUG-BLACK" }
    ],
    "order_id": "ord-112233",
    "shipping_address": { "city": "Photon Creek", "country": "USA", "street": "123 Quantum Lane", "zip": "98765" }
  }
}
```

### In This Chapter

This example was a microcosm of everything you've learned.
*   We used a top-level **forking pipeline** to create multiple outputs.
*   The `invoice` fork used the **enrichment** (`merge`) and **aggregation** (`reduce`) patterns.
*   The `shipping_manifest` fork used a **filter-then-map** pipeline to process a subset of data.
*   We used `let` extensively to break the problem into logical, readable steps, proving that even complex scripts can be managed effectively.

You are now fully equipped to design and implement sophisticated JSON transformations to solve real-world integration challenges. The final part of this guide will cover advanced topics like performance, error handling, and best practices.
