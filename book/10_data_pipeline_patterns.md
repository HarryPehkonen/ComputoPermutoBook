## **Chapter 10: Data Pipeline Patterns**

In the previous chapter, we introduced the most important transformation strategy: building a dynamic context before applying a template. This chapter expands on that idea by introducing several other common and powerful data pipeline patterns.

Think of these as reusable blueprints for your transformations. Recognizing these patterns will help you structure your scripts more effectively and solve complex problems with surprising clarity.

### Pattern 1: The Enrichment Pipeline

**Goal:** To take an existing data structure and add new, computed information to it.

**When to use:** When your input data is mostly correct, but you need to augment it with additional fields, flags, or calculations before passing it on.

The key operator for this pattern is **`merge`**. You start with the original object and merge a new object containing your computed fields onto it.

#### Enrichment Example: Scoring User Engagement

Imagine we have a user object and we want to add an `engagement_score` and a `status` flag based on their activity.

1.  **Input Data (`user_activity.json`):**
    ```json
    {
      "user_id": "u-777",
      "logins": 42,
      "posts_created": 15,
      "comments_made": 112,
      "last_login_days_ago": 3
    }
    ```

2.  **The Script (`enrich_user.json`):**
    This script calculates a score and determines a status, then merges this new information back into the original user object.

    ```json
    ["let",
      [
        ["user", ["$input"]],
        ["score",
          ["+",
            ["*", ["get", ["$", "/user"], "/logins"], 2],
            ["*", ["get", ["$", "/user"], "/posts_created"], 10],
            ["*", ["get", ["$", "/user"], "/comments_made"], 5]
          ]
        ]
      ],
      ["merge",
        ["$", "/user"],
        ["obj",
          ["engagement_score", ["$", "/score"]],
          ["status",
            ["if",
              ["&&",
                [">", ["$", "/score"], 500],
                ["<", ["get", ["$", "/user"], "/last_login_days_ago"], 30]
              ],
              "active_and_high_engagement",
              "at_risk"
            ]
          ]
        ]
      ]
    ]
    ```

3.  **The Output:**
    The result is the original object, plus the two new fields.
    ```json
    {
      "comments_made": 112,
      "engagement_score": 794,
      "last_login_days_ago": 3,
      "logins": 42,
      "posts_created": 15,
      "status": "active_and_high_engagement",
      "user_id": "u-777"
    }
    ```
    This pattern is perfect for middleware, where you receive data, add value to it, and then pass it to the next service in the chain.

### Pattern 2: The Forking Pipeline

**Goal:** To create two or more completely different output structures from a single input source.

**When to use:** When you need to send tailored data to different downstream systems. For example, one payload for your analytics service and another for your search index.

This pattern uses a top-level `obj` or `permuto.apply` to define the separate output "forks," with each fork containing its own independent transformation logic.

#### Forking Example: Indexing and Analytics

From a single raw event, we need to generate a compact document for our search index and a detailed document for our analytics database.

1.  **Input Data (`raw_event.json`):**
    ```json
    {
      "event_id": "evt-aaa-bbb",
      "timestamp": "2023-10-27T10:00:00Z",
      "user": { "id": "u-123", "name": "Alice" },
      "action": "product_view",
      "details": {
        "product_id": "prod-xyz-789",
        "product_name": "Quantum T-Shirt",
        "price_cents": 2999,
        "tags": ["apparel", "t-shirt", "quantum"]
      }
    }
    ```

2.  **The Script (`forking_pipeline.json`):**
    The top-level expression is an `obj` with two keys, `for_search` and `for_analytics`. Each value is a `let` block that defines a self-contained transformation.

    ```json
    ["obj",
      ["for_search",
        ["let", [["d", ["get", ["$input"], "/details"]]],
          ["obj",
            ["doc_id", ["get", ["$", "/d"], "/product_id"]],
            ["content", ["get", ["$", "/d"], "/product_name"]],
            ["tags", ["get", ["$", "/d"], "/tags"]]
          ]
        ]
      ],
      ["for_analytics",
        ["let", [["d", ["get", ["$input"], "/details"]]],
          ["obj",
            ["event_type", ["get", ["$input"], "/action"]],
            ["user", ["get", ["$input"], "/user/id"]],
            ["product", ["get", ["$", "/d"], "/product_id"]],
            ["revenue_potential", ["/", ["get", ["$", "/d"], "/price_cents"], 100]]
          ]
        ]
      ]
    ]
    ```

3.  **The Output:**
    The final JSON contains two distinct, independent objects, ready to be sent to their respective systems.
    ```json
    {
      "for_analytics": {
        "event_type": "product_view",
        "product": "prod-xyz-789",
        "revenue_potential": 29.99,
        "user": "u-123"
      },
      "for_search": {
        "content": "Quantum T-Shirt",
        "doc_id": "prod-xyz-789",
        "tags": [
          "apparel",
          "t-shirt",
          "quantum"
        ]
      }
    }
    ```

### Pattern 3: The Aggregation Pipeline

**Goal:** To process a list of items and produce a single summary object.

**When to use:** When you need to generate reports, dashboards, or summary statistics from a collection of raw data.

This pattern typically involves heavy use of `filter`, `map`, and `reduce` to calculate summary statistics, which are then assembled into a final object using `obj`.

#### Aggregation Example: Sales Report

Let's generate a summary report from a list of sales transactions.

1.  **Input Data (`sales_data.json`):**
    ```json
    {
      "transactions": [
        { "id": 1, "product": "A", "amount": 100, "region": "NA" },
        { "id": 2, "product": "B", "amount": 150, "region": "EU" },
        { "id": 3, "product": "A", "amount": 120, "region": "NA" },
        { "id": 4, "product": "C", "amount": 200, "region": "NA" },
        { "id": 5, "product": "B", "amount": 180, "region": "APAC" }
      ]
    }
    ```

2.  **The Script (`sales_report.json`):**
    This script uses multiple `let` bindings to calculate different statistics before assembling the final report.

    ```json
    ["let",
      [
        ["txs", ["get", ["$input"], "/transactions"]],
        ["all_amounts", ["map", ["$", "/txs"], ["lambda",["t"],["get",["$","/t"],"/amount"]]]],
        ["na_txs", ["filter", ["$", "/txs"], ["lambda",["t"],["==",["get",["$","/t"],"/region"],"NA"]]]]
      ],
      ["obj",
        ["total_transactions", ["count", ["$", "/txs"]]],
        ["total_revenue",
          ["reduce", ["$", "/all_amounts"], ["lambda",["acc","n"],["+",["$","/acc"],["$","/n"]]], 0]
        ],
        ["avg_revenue",
          ["/",
            ["reduce", ["$", "/all_amounts"], ["lambda",["acc","n"],["+",["$","/acc"],["$","/n"]]], 0],
            ["count", ["$", "/txs"]]
          ]
        ],
        ["na_revenue",
          ["reduce",
            ["map", ["$", "/na_txs"], ["lambda",["t"],["get",["$","/t"],"/amount"]]],
            ["lambda",["acc","n"],["+",["$","/acc"],["$","/n"]]], 0
          ]
        ]
      ]
    ]
    ```
    *Note: `count` is a simple new operator that returns the length of an array.*

3.  **The Output:**
    The script produces a single JSON object summarizing the raw transaction data.
    ```json
    {
      "avg_revenue": 150,
      "na_revenue": 420,
      "total_revenue": 750,
      "total_transactions": 5
    }
    ```

### In This Chapter

You've learned three fundamental blueprints for structuring your transformations:
*   **Enrichment:** Adding computed data to an existing object using `merge`.
*   **Forking:** Creating multiple, distinct outputs from one source.
*   **Aggregation:** Summarizing a list of items into a single report object using `map`, `filter`, and `reduce`.

By recognizing these patterns in your own data challenges, you can write cleaner, more intuitive, and more powerful Computo scripts.
