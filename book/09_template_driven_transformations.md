## **Chapter 9: Template-Driven Transformations**

Welcome to Part III of our guide. By now, you have a solid grasp of Computo's logic and Permuto's templating. You can make decisions with `if`, iterate with `map`, and reshape data with `permuto.apply`. Now, it's time to elevate our approach and learn the patterns that separate simple scripts from robust, maintainable data pipelines.

This chapter focuses on a powerful strategy: **Template-Driven Transformation**. The core idea is to let a clean, declarative Permuto template define the "what" (the final data structure), while a focused Computo script handles the "how" (the logic needed to prepare the data for that template).

### The Core Pattern: Dynamic Context Building

So far, we have often passed our raw input directly to `permuto.apply` like this:

`["permuto.apply", <template>, ["$input"]]`

This works, but it tightly couples your template to the (potentially messy) structure of your input data. If the input API changes a field name, you have to change your template.

A more robust pattern is to use Computo to **build a clean, intermediate context object first**. This new context is tailored specifically to what the template expects.

**The Workflow:**
1.  Define a "perfect" output structure in a Permuto template.
2.  Write a Computo script that reads the messy raw input.
3.  The script uses `map`, `filter`, `let`, and `obj` to build a new, clean context object.
4.  The script's final step is to call `permuto.apply`, passing it the template and the **newly-built context**.

This decouples your final output from your raw input, making your transformations more resilient to change.

#### Example: Generating a Product Display Card

Let's imagine we're receiving a product data object from a backend service, and we need to transform it into a format suitable for a UI display card.

1.  **The Raw Input (`product_input.json`):**
    This data is a bit messy. It has internal IDs, a list of variants with stock counts, and prices in cents.
    ```json
    {
      "product_id": "prod-xyz-789",
      "base_price_cents": 2999,
      "name": "Quantum T-Shirt",
      "variants": [
        { "sku": "xyz-s-red", "attrs": { "size": "S", "color": "Red" }, "stock": 10 },
        { "sku": "xyz-m-red", "attrs": { "size": "M", "color": "Red" }, "stock": 0 },
        { "sku": "xyz-l-blue", "attrs": { "size": "L", "color": "Blue" }, "stock": 25 }
      ],
      "metadata": { "source": "warehouse-api" }
    }
    ```

2.  **The Target Template:**
    Our UI card needs a clean, simple structure. We'll define this in a Permuto template. Notice this template expects a `price` (in dollars), a `title`, and a list of `available_options`. It knows nothing about `base_price_cents` or `stock`.

    **`card_template.json`:**
    ```json
    {
      "display_card": {
        "title": "${/title}",
        "price": "USD $${/price}",
        "options": "${/available_options}"
      }
    }
    ```

3.  **The Computo "Glue" Script (`build_card_context.json`):**
    This is where the magic happens. This script will read the raw input and build the perfect context for `card_template.json`.

    ```json
    ["let",
      [
        ["product", ["$input"]],
        ["in_stock_variants",
          ["filter",
            ["get", ["$", "/product"], "/variants"],
            ["lambda", ["v"], [">", ["get", ["$", "/v"], "/stock"], 0]]
          ]
        ]
      ],
      ["let",
        [
          ["clean_context",
            ["obj",
              ["title", ["get", ["$", "/product"], "/name"]],
              ["price", ["/", ["get", ["$", "/product"], "/base_price_cents"], 100]],
              ["available_options",
                ["map",
                  ["$", "/in_stock_variants"],
                  ["lambda", ["v"], ["get", ["$", "/v"], "/attrs"]]
                ]
              ]
            ]
          ]
        ],
        ["permuto.apply",
          {
            "display_card": {
              "title": "${/title}",
              "price": "USD $${/price}",
              "options": "${/available_options}"
            }
          },
          ["$", "/clean_context"]
        ]
      ]
    ]
    ```

**Let's analyze the script's logic:**
*   It uses `let` to store the raw `product` data.
*   It uses `filter` to create a new array, `in_stock_variants`, containing only variants with `stock > 0`.
*   It enters a new `let` block to build the `clean_context`.
    *   The `title` is extracted directly.
    *   The `price` is *calculated* by dividing `base_price_cents` by 100.
    *   `available_options` is created by *mapping* over the `in_stock_variants` and extracting just the `attrs` object from each.
*   Finally, it calls `permuto.apply`, passing our hardcoded template and the newly created `clean_context` variable.

Run it with the `--interpolation` flag for the price string:
```bash
computo --interpolation build_card_context.json product_input.json
```

**Final Output:**
```json
{
  "display_card": {
    "options": [
      {
        "color": "Red",
        "size": "S"
      },
      {
        "color": "Blue",
        "size": "L"
      }
    ],
    "price": "USD $29.99",
    "title": "Quantum T-Shirt"
  }
}
```
We successfully transformed a messy backend object into a perfect UI-ready object by separating the data preparation logic from the final presentation template.

### In This Chapter

This chapter shifted our focus from learning operators to learning strategy.
*   You learned the **Dynamic Context Building** pattern, a robust method for decoupling templates from raw data structures.
*   You saw how to use a chain of Computo operators (`let`, `filter`, `map`, `obj`) to prepare a clean dataset.
*   You reinforced the clear division of labor: **Computo prepares the data, Permuto presents the data.**

This pattern is the key to creating scalable and maintainable transformations. In the next chapter, we'll look at other common data pipeline patterns that build on this foundation.
