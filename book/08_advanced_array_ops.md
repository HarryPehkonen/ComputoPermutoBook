## **Chapter 8: Advanced Array Operations**

In Chapter 6, we introduced `map`, the fundamental tool for transforming arrays. However, transformation is only one part of the story. Often, you need to select a subset of items from an array or aggregate an entire array into a single value.

This chapter introduces the remaining array operators: `filter`, `reduce`, and specialized query operators (`find`, `some`, `every`, `flatMap`). Mastering these operators alongside `map` will give you a complete and powerful toolkit for virtually any array manipulation task.

### `filter`: Selecting Items from an Array

While `map` transforms every item in an array, `filter` *selects* items from an array. It iterates over an array and returns a new array containing only the items for which a given condition is "truthy".

The syntax is nearly identical to `map`:

`["filter", <array_expression>, ["lambda", ["<item_variable>"], <condition_expression>]]`

The `<condition_expression>` must evaluate to a "truthy" or "falsy" value, following the same rules as the `if` operator. If the condition is truthy, the item is kept; if falsy, it is discarded.

#### `filter` Example: Finding Active Users

Let's return to our `users_input.json` and create a new list containing only the active users.

**`users_input.json` (for reference):**
```json
{
  "users": [
    { "name": "Alice", "active": true, "plan": "premium" },
    { "name": "Bob", "active": false, "plan": "basic" },
    { "name": "Charlie", "active": true, "plan": "basic" }
  ]
}
```

**`filter_active.json`:**
```json
["filter",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"], ["get", ["$", "/user"], "/active"]]
]
```
The lambda here is simple: for each `user` object, it gets the value of the `active` key. Since `true` is truthy and `false` is falsy, this works perfectly as a condition.

**Output:**
```json
[
  {
    "active": true,
    "name": "Alice",
    "plan": "premium"
  },
  {
    "active": true,
    "name": "Charlie",
    "plan": "basic"
  }
]
```
The resulting array contains only the objects for Alice and Charlie, because Bob's `active` field was `false`.

### Chaining `filter` and `map`

The true power of these operators comes from chaining them together. Because `filter` returns an array, you can feed its result directly into a `map` operator.

Let's build on the previous example. We want a list of just the *names* of the active, premium users.

**`active_premium_names.json`:**
```json
["map",
  ["filter",
    ["filter",
      ["get", ["$input"], "/users"],
      ["lambda", ["user"], ["get", ["$", "/user"], "/active"]]
    ],
    ["lambda", ["user"], ["==", ["get", ["$", "/user"], "/plan"], "premium"]]
  ],
  ["lambda", ["user"], ["get", ["$", "/user"], "/name"]]
]
```

This script looks complex, but it's a very clear data pipeline if you read it from the inside out:
1.  **First `filter`**: Selects all users where `active` is true.
2.  **Second `filter`**: Takes the result of the first filter and, from that subset, selects all users where `plan` is equal to `"premium"`.
3.  **`map`**: Takes the final filtered list (which now only contains Alice) and transforms it into an array of names.

**Output:**
```json
[
  "Alice"
]
```

This pattern—**filter, then map**—is one of the most common and powerful patterns in functional data processing.

### `reduce`: Aggregating an Array to a Single Value

While `map` and `filter` produce new arrays, `reduce` (sometimes called "fold" or "accumulate") boils an entire array down to a single value. This is used for tasks like summing numbers, concatenating strings, or flattening a list of lists.

The `reduce` operator is the most complex of the three, introducing an "accumulator".

`["reduce", <array_expression>, <lambda>, <initial_value>]`

The `lambda` for `reduce` takes **two** arguments:
`["lambda", ["<accumulator>", "<current_item>"], <expression>]`

Here's how it works:
1.  The `<accumulator>` is initialized with the `<initial_value>`.
2.  The lambda is called for the first item in the array. The result of its `<expression>` becomes the **new value of the accumulator**.
3.  The lambda is called for the second item, using the updated accumulator. This repeats for all items.
4.  The final value of the accumulator is the result of the `reduce` operation.

#### `reduce` Example: Summing an Array

Let's calculate the total cost of all user plans in our system.

**`total_cost.json`:**
```json
["let",
  [
    ["costs", {"array": [20, 5, 5]}]
  ],
  ["reduce",
    ["$", "/costs"],
    ["lambda", ["total", "cost"], ["+", ["$", "/total"], ["$", "/cost"]]],
    0
  ]
]
```

1.  `total` starts at `0` (the initial value).
2.  **Iteration 1:** `total` is `0`, `cost` is `20`. The lambda returns `0 + 20 = 20`. `total` is now `20`.
3.  **Iteration 2:** `total` is `20`, `cost` is `5`. The lambda returns `20 + 5 = 25`. `total` is now `25`.
4.  **Iteration 3:** `total` is `25`, `cost` is `5`. The lambda returns `25 + 5 = 30`. `total` is now `30`.
5.  The array is exhausted. `reduce` returns the final value of the accumulator.

**Output:** `30`

### The Complete Pipeline: Map, Filter, Reduce

Now we can combine all three to answer complex questions. For example: "What is the total monthly cost of all active, premium plans?"

**`premium_revenue.json`:**
```json
["reduce",
  ["map",
    ["filter",
      ["get", ["$input"], "/users"],
      ["lambda", ["u"],
        ["&&",
          ["get", ["$", "/u"], "/active"],
          ["==", ["get", ["$", "/u"], "/plan"], "premium"]
        ]
      ]
    ],
    ["lambda", ["u"], ["get", ["$", "/u"], "/monthly_cost"]]
  ],
  ["lambda", ["total", "cost"], ["+", ["$", "/total"], ["$", "/cost"]]],
  0
]
```
*(Note: This example uses a logical AND operator, `&&`, which we haven't formally covered but whose function is intuitive here. We'll cover it later.)*

**The Pipeline:**
1.  **`filter`**: Finds all users who are both active AND have a premium plan. (Result: just Alice's object).
2.  **`map`**: Takes that filtered list and transforms it into a list of costs. (Result: `[20]`).
3.  **`reduce`**: Takes that list of costs and sums it. (Result: `20`).

**Output:** `20`

### Additional Array Query Operators

Beyond the core transformation operators (`map`, `filter`, `reduce`), Computo provides specialized operators for common array query patterns. These operators make it easy to answer questions like "Does any item match this condition?" or "What's the first item that meets my criteria?"

#### `find`: Locating the First Match

The `find` operator searches through an array and returns the **first item** that matches a condition. If no item matches, it returns `null`.

`["find", <array_expression>, ["lambda", ["<item_variable>"], <condition_expression>]]`

**Example: Finding the first premium user**

**`find_premium_user.json`:**
```json
[
  /* Find the first user with a premium plan */
  "find",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"], ["==", ["get", ["$", "/user"], "/plan"], "premium"]]
]
```

**Output:**
```json
{
  "active": true,
  "name": "Alice", 
  "plan": "premium"
}
```

If no premium users existed, the result would be `null`.

#### `some`: Testing for Any Match

The `some` operator returns `true` if **at least one** item in the array matches the condition, `false` otherwise. It's perfect for answering "Is there any..." questions.

`["some", <array_expression>, ["lambda", ["<item_variable>"], <condition_expression>]]`

**Example: Checking if any users are inactive**

**`has_inactive_users.json`:**
```json
[
  /* Check if there are any inactive users in the system */
  "some",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"], ["==", ["get", ["$", "/user"], "/active"], false]]
]
```

**Output:** `true` (because Bob is inactive)

This is much more efficient than filtering and checking the count, especially for large arrays, because `some` stops as soon as it finds the first match.

#### `every`: Testing for Universal Match

The `every` operator returns `true` if **all** items in the array match the condition, `false` otherwise. It answers "Are all..." questions.

`["every", <array_expression>, ["lambda", ["<item_variable>"], <condition_expression>]]`

**Example: Verifying all users are active**

**`all_users_active.json`:**
```json
[
  /* Verify that all users in the system are active */
  "every", 
  ["get", ["$input"], "/users"],
  ["lambda", ["user"], ["get", ["$", "/user"], "/active"]]
]
```

**Output:** `false` (because Bob is inactive)

**Note:** `every` returns `true` for empty arrays, which is mathematically correct (vacuous truth).

#### `flatMap`: Transforming and Flattening

The `flatMap` operator is like `map`, but if the transformation function returns an array, those arrays are flattened into a single result array. This is useful when each item needs to be expanded into multiple items.

`["flatMap", <array_expression>, ["lambda", ["<item_variable>"], <transform_expression>]]`

**Example: Expanding user permissions**

Let's say each user has multiple roles, and we want a flat list of all permissions across all users.

**`expanded_users_input.json`:**
```json
{
  "users": [
    { 
      "name": "Alice", 
      "roles": ["admin", "editor"] 
    },
    { 
      "name": "Bob", 
      "roles": ["viewer"] 
    },
    { 
      "name": "Charlie", 
      "roles": ["editor", "contributor"] 
    }
  ]
}
```

**`all_roles.json`:**
```json
[
  /* Extract all roles from all users into a single flat array */
  "flatMap",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"], ["get", ["$", "/user"], "/roles"]]
]
```

**Output:**
```json
["admin", "editor", "viewer", "editor", "contributor"]
```

Compare this to regular `map`, which would give you nested arrays:
```json
[["admin", "editor"], ["viewer"], ["editor", "contributor"]]
```

#### Practical Combinations

These operators work beautifully together for complex queries:

**`user_validation_report.json`:**
```json
["obj",
  /* Check various conditions about our user base */
  ["has_premium_users", [
    "some", 
    ["get", ["$input"], "/users"],
    ["lambda", ["u"], ["==", ["get", ["$", "/u"], "/plan"], "premium"]]
  ]],
  
  ["all_users_active", [
    "every",
    ["get", ["$input"], "/users"], 
    ["lambda", ["u"], ["get", ["$", "/u"], "/active"]]
  ]],
  
  ["first_inactive_user", [
    "find",
    ["get", ["$input"], "/users"],
    ["lambda", ["u"], ["==", ["get", ["$", "/u"], "/active"], false]]
  ]],
  
  ["total_user_count", [
    "count", 
    ["get", ["$input"], "/users"]
  ]]
]
```

**Output:**
```json
{
  "has_premium_users": true,
  "all_users_active": false,
  "first_inactive_user": {
    "name": "Bob",
    "active": false,
    "plan": "basic"
  },
  "total_user_count": 3
}
```

### Array Pairing and Indexing Operations

Beyond filtering and aggregation, Computo provides specialized operators for working with multiple arrays simultaneously and for accessing positional information within arrays. These operators are essential for complex data correlation and position-aware transformations.

#### `zip`: Combining Arrays Element-Wise

The `zip` operator takes two arrays and combines them into an array of pairs (two-element arrays). Each pair contains corresponding elements from the two input arrays.

`["zip", <array1_expression>, <array2_expression>]`

**Example: Pairing names with scores**

```json
["zip",
  {"array": ["Alice", "Bob", "Charlie"]},
  {"array": [95, 87, 92]}
]
```

**Output:**
```json
[
  ["Alice", 95],
  ["Bob", 87], 
  ["Charlie", 92]
]
```

If the arrays have different lengths, `zip` stops at the shorter array:

```json
["zip",
  {"array": ["Alice", "Bob", "Charlie"]},
  {"array": [95, 87]}
]
```

**Output:**
```json
[
  ["Alice", 95],
  ["Bob", 87]
]
```

**Practical Example: Correlating data from different sources**

**`correlate_data.json`:**
```json
["let",
  [
    ["user_names", ["map", ["get", ["$input"], "/users"], ["lambda", ["u"], ["get", ["$", "/u"], "/name"]]]],
    ["user_scores", ["map", ["get", ["$input"], "/users"], ["lambda", ["u"], ["get", ["$", "/u"], "/score"]]]]
  ],
  ["map",
    ["zip", ["$", "/user_names"], ["$", "/user_scores"]],
    ["lambda", ["pair"], 
      ["obj",
        ["name", ["get", ["$", "/pair"], "/0"]],
        ["score", ["get", ["$", "/pair"], "/1"]],
        ["grade", ["if", [">", ["get", ["$", "/pair"], "/1"], 90], "A", "B"]]
      ]
    ]
  ]
]
```

#### `zipWith`: Custom Array Combination

While `zip` creates pairs, `zipWith` allows you to specify a custom function for combining corresponding elements from two arrays.

`["zipWith", <array1_expression>, <array2_expression>, ["lambda", ["item1", "item2"], <combination_expression>]]`

**Example: Adding corresponding numbers**

```json
["zipWith",
  {"array": [1, 2, 3]},
  {"array": [10, 20, 30]},
  ["lambda", ["a", "b"], ["+", ["$", "/a"], ["$", "/b"]]]
]
```

**Output:**
```json
[11, 22, 33]
```

**Practical Example: Calculating weighted scores**

```json
["let",
  [
    ["scores", {"array": [85, 92, 78]}],
    ["weights", {"array": [0.4, 0.3, 0.3]}]
  ],
  ["reduce",
    ["zipWith", 
      ["$", "/scores"], 
      ["$", "/weights"],
      ["lambda", ["score", "weight"], ["*", ["$", "/score"], ["$", "/weight"]]]
    ],
    ["lambda", ["total", "weighted"], ["+", ["$", "/total"], ["$", "/weighted"]]],
    0
  ]
]
```

This calculates a weighted average: (85×0.4) + (92×0.3) + (78×0.3) = 84.2

#### `mapWithIndex`: Position-Aware Transformation

The `mapWithIndex` operator is like `map`, but the lambda function receives both the item and its index position within the array.

`["mapWithIndex", <array_expression>, ["lambda", ["item", "index"], <transform_expression>]]`

**Example: Creating numbered items**

```json
["mapWithIndex",
  {"array": ["apple", "banana", "cherry"]},
  ["lambda", ["fruit", "index"],
    ["obj",
      ["position", ["+", ["$", "/index"], 1]],  // 1-based numbering
      ["name", ["$", "/fruit"]]
    ]
  ]
]
```

**Output:**
```json
[
  {"position": 1, "name": "apple"},
  {"position": 2, "name": "banana"},
  {"position": 3, "name": "cherry"}
]
```

**Practical Example: Processing data with position-dependent logic**

```json
["mapWithIndex",
  ["get", ["$input"], "/daily_temperatures"],
  ["lambda", ["temp", "day"],
    ["obj",
      ["day", ["+", ["$", "/day"], 1]],
      ["temperature", ["$", "/temp"]],
      ["day_type", ["if", 
        ["==", ["%", ["$", "/day"], 7], 6],  // Check if day % 7 == 6 (Sunday, 0-based)
        "weekend",
        "weekday"
      ]],
      ["temperature_trend", ["if",
        ["==", ["$", "/day"], 0],
        "baseline",
        ["if", [">", ["$", "/temp"], 75], "above_average", "normal"]
      ]]
    ]
  ]
]
```

#### `enumerate`: Creating Index-Value Pairs

The `enumerate` operator transforms an array into an array of `[index, value]` pairs, making it easy to work with both the position and content of each element.

`["enumerate", <array_expression>]`

**Example: Basic enumeration**

```json
["enumerate", {"array": ["red", "green", "blue"]}]
```

**Output:**
```json
[
  [0, "red"],
  [1, "green"], 
  [2, "blue"]
]
```

**Practical Example: Processing with position awareness**

```json
["map",
  ["enumerate", ["get", ["$input"], "/tasks"]],
  ["lambda", ["indexed_task"],
    ["obj",
      ["task_id", ["get", ["$", "/indexed_task"], "/0"]],
      ["task_name", ["get", ["get", ["$", "/indexed_task"], "/1"], "/name"]],
      ["priority", ["if",
        ["<", ["get", ["$", "/indexed_task"], "/0"], 3],
        "high",
        "normal"
      ]],
      ["status", ["get", ["get", ["$", "/indexed_task"], "/1"], "/status"]]
    ]
  ]
]
```

This creates task objects where the first 3 tasks (indices 0, 1, 2) are marked as high priority.

#### Combining Indexing Operations

These operators work well together for complex data processing:

**`complex_array_processing.json`:**
```json
["let",
  [
    ["data", {"array": [10, 25, 15, 30, 20]}],
    ["weights", {"array": [0.1, 0.2, 0.3, 0.2, 0.2]}]
  ],
  ["obj",
    // Create indexed data points
    ["indexed_data", ["enumerate", ["$", "/data"]]],
    
    // Calculate weighted values using zipWith
    ["weighted_values", ["zipWith",
      ["$", "/data"],
      ["$", "/weights"], 
      ["lambda", ["value", "weight"], ["*", ["$", "/value"], ["$", "/weight"]]]
    ]],
    
    // Apply position-dependent transformations
    ["processed_data", ["mapWithIndex",
      ["$", "/data"],
      ["lambda", ["value", "index"],
        ["obj",
          ["original_value", ["$", "/value"]],
          ["position", ["$", "/index"]],
          ["is_first_half", ["<", ["$", "/index"], 3]],
          ["relative_to_average", ["-", ["$", "/value"], 20]]
        ]
      ]
    ]],
    
    // Pair original data with processed data using zip
    ["comparison", ["zip",
      ["$", "/data"],
      ["map", ["$", "/processed_data"], ["lambda", ["item"], ["get", ["$", "/item"], "/relative_to_average"]]]
    ]]
  ]
]
```

This demonstrates how the indexing operators enable sophisticated data analysis patterns that would be difficult to achieve with basic `map`, `filter`, and `reduce` alone.

### In This Chapter

You have now completed the comprehensive functional toolkit for array processing.
*   You learned to use **`filter`** to selectively create new arrays based on a condition.
*   You learned to use **`reduce`** to aggregate an array's contents into a single result.
*   You saw how **chaining `filter` and `map`** creates powerful data pipelines.
*   You combined all three operators—**`filter`, `map`, and `reduce`**—to answer a complex question about a data set in a single, expressive script.
*   You discovered specialized query operators: **`find`** for locating items, **`some`** for existence checks, and **`every`** for universal validation.
*   You explored **`flatMap`** for transforming and flattening nested data structures.
*   You mastered array pairing operations: **`zip`** for element-wise combination and **`zipWith`** for custom combining functions.
*   You learned position-aware transformations with **`mapWithIndex`** for accessing both element and index.
*   You discovered **`enumerate`** for creating index-value pairs and processing with position awareness.
*   You saw how these operators combine to create comprehensive data analysis reports and sophisticated correlation patterns.

You are now equipped to handle a vast range of data transformation challenges. The following chapters will build on this foundation, exploring how to apply these patterns to real-world integration scenarios.
