## **Chapter 8: Advanced Array Operations**

In Chapter 6, we introduced `map`, the fundamental tool for transforming arrays. However, transformation is only one part of the story. Often, you need to select a subset of items from an array or aggregate an entire array into a single value.

This chapter introduces the remaining core array operators: `filter` and `reduce`. Mastering these three operators (`map`, `filter`, and `reduce`) will give you a complete and powerful toolkit for virtually any array manipulation task.

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

### In This Chapter

You have now completed the core functional toolkit for array processing.
*   You learned to use **`filter`** to selectively create new arrays based on a condition.
*   You learned to use **`reduce`** to aggregate an array's contents into a single result.
*   You saw how **chaining `filter` and `map`** creates powerful data pipelines.
*   You combined all three operators—**`filter`, `map`, and `reduce`**—to answer a complex question about a data set in a single, expressive script.

You are now equipped to handle a vast range of data transformation challenges. The following chapters will build on this foundation, exploring how to apply these patterns to real-world integration scenarios.
