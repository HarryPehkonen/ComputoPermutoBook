## **Chapter 6: Working with Arrays**

In our previous examples, we manually selected a single user from an array with `["get", ..., "/users/0"]`. This is fine for demonstration, but real-world tasks require processing *every* item in a collection. You might need to transform a list of products, summarize a series of log entries, or, in our case, process a list of users.

This is where Computo's array operators come into play. We'll start with the most fundamental one: `map`.

### The `map` Operator

The `map` operator iterates over an input array and applies a transformation to each item, producing a new array of the transformed items. The original array is not changed.

Its syntax introduces a new concept: the `lambda` (or anonymous function).

`["map", <array_expression>, ["lambda", ["<item_variable>"], <transform_expression>]]`

Let's break that down:
*   `<array_expression>`: An expression that must evaluate to a JSON array.
*   `["lambda", ... ]`: A special expression that defines an operation to be performed on each item.
*   `<item_variable>`: The name you choose for the variable that will hold the current item during each iteration.
*   `<transform_expression>`: The expression that transforms the item. Inside this expression, you can access the current item using `["$", "/<item_variable>"]`.

### Your First `map`: Extracting Usernames

Let's use the same `users_input.json` from the last chapter. Our goal is to produce a simple JSON array containing only the names of all the users.

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

1.  Create a script named `get_names.json`.

    ```json
    ["map",
      ["get", ["$input"], "/users"],
      ["lambda", ["user"], ["get", ["$", "/user"], "/name"]]
    ]
    ```

    Here is what this script tells the engine:
    a.  "Map over the array found at the `/users` path in the input."
    b.  "For each item, create a temporary variable named `user`."
    c.  "As the transformation, `get` the `/name` property from the `user` variable."

2.  Run the script:

    ```bash
    computo get_names.json users_input.json
    ```

The output is a new array containing just the transformed items:
```json
[
  "Alice",
  "Bob",
  "Charlie"
]
```

### Unambiguous Array Syntax: `{"array": [...]}`

Before we continue, we need to address a crucial piece of syntax. In Computo, a JSON array `[...]` is always treated as an operator call. So how do you represent a *literal* array of data? You use a special object wrapper:

`{"array": [item1, item2, ...]}`

When the interpreter sees `{"array": ...}`, it knows you mean "this is a literal array of data," not an action to perform.

For example, to map over a hardcoded array, you would write:
```json
["map",
  {"array": [10, 20, 30]},
  ["lambda", ["n"], ["+", ["$", "/n"], 5]]
]
```
This would produce `[15, 25, 35]`. This syntax prevents any ambiguity between operator calls and literal array data.

### Transforming Objects within a `map`

The real power of `map` comes from transforming each item into a new object structure. You can use `obj` or `permuto.apply` right inside the `lambda`.

Let's transform our user list into a new list of simpler objects, each containing just a `name` and `plan`.

**`transform_users.json`:**
```json
["map",
  ["get", ["$input"], "/users"],
  ["lambda", ["u"],
    ["obj",
      ["name", ["get", ["$", "/u"], "/name"]],
      ["plan", ["get", ["$", "/u"], "/plan"]]
    ]
  ]
]
```

Running this gives us a completely new array of objects:
```json
[
  {
    "name": "Alice",
    "plan": "premium"
  },
  {
    "name": "Bob",
    "plan": "basic"
  },
  {
    "name": "Charlie",
    "plan": "basic"
  }
]
```

### Combining `map` and `if`

You can use any Computo operator inside a `lambda`, including `if`. This allows for powerful, item-specific conditional logic.

Let's generate a status message for each user. Active users get a welcome message; inactive users get a notice.

**`user_statuses.json`:**
```json
["map",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"],
    ["if",
      ["get", ["$", "/user"], "/active"],
      ["permuto.apply",
        {"message": "User ${/name} is active."},
        ["$", "/user"]
      ],
      ["permuto.apply",
        {"message": "User ${/name} is INACTIVE."},
        ["$", "/user"]
      ]
    ]
  ]
]
```

Run this with the `--interpolation` flag:
```bash
computo --interpolation user_statuses.json users_input.json
```

The output is an array of conditionally generated objects:
```json
[
  {
    "message": "User Alice is active."
  },
  {
    "message": "User Bob is INACTIVE."
  },
  {
    "message": "User Charlie is active."
  }
]
```

### In This Chapter

You've added array processing to your skillset. You have learned:
*   How to iterate over an array and transform each item using the **`map`** operator.
*   The syntax for **`lambda`** expressions to define the per-item transformation.
*   The special **`{"array": [...]}`** syntax for representing literal arrays.
*   How to combine `map` with `obj`, `if`, and `permuto.apply` for complex list transformations.

`map` is the first of several array operators. In the next chapters, we will explore others like `filter` and `reduce` to further refine our data pipelines.
