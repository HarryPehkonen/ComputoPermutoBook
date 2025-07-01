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

### Lambda Variable Resolution: Reusable Functions

As your transformations become more complex, you'll often find yourself writing the same lambda expressions multiple times. Computo provides a powerful feature called **lambda variable resolution** that allows you to store lambda functions in variables using `let` bindings and reuse them throughout your script.

#### Basic Lambda Variable Storage

You can store a lambda function in a variable and then reference it using the `$` operator:

```json
["let", [["function_name", ["lambda", ["param"], <transformation>]]],
  ["map", <array>, ["$", "/function_name"]]
]
```

#### Simple Example: Reusable Double Function

Let's start with a basic example that doubles numbers. Instead of writing the same lambda twice, we'll store it once and reuse it:

**`reusable_double.json`:**
```json
["let", [["double", ["lambda", ["x"], ["*", ["$", "/x"], 2]]]],
  ["obj",
    ["list1", ["map", {"array": [1, 2, 3]}, ["$", "/double"]]],
    ["list2", ["map", {"array": [4, 5, 6]}, ["$", "/double"]]]
  ]
]
```

**Output:**
```json
{
  "list1": [2, 4, 6],
  "list2": [8, 10, 12]
}
```

The `double` function is defined once and used twice, making the code more maintainable and readable.

#### Multiple Lambda Variables

You can define multiple lambda functions in the same `let` binding and use them together:

**`multiple_functions.json`:**
```json
["let", [
    ["increment", ["lambda", ["x"], ["+", ["$", "/x"], 1]]],
    ["is_large", ["lambda", ["x"], [">", ["$", "/x"], 3]]]
  ],
  ["map", 
    ["filter", {"array": [1, 2, 3, 4, 5]}, ["$", "/is_large"]], 
    ["$", "/increment"]
  ]
]
```

**Output:**
```json
[5, 6]
```

This example:
1. Defines two functions: `increment` (adds 1) and `is_large` (checks if > 3)
2. First filters the array to keep only large numbers: `[4, 5]`
3. Then increments each remaining number: `[5, 6]`

#### Real-World Example: User Processing Pipeline

Let's apply this to our user data with more complex, reusable transformations:

**`user_pipeline_with_functions.json`:**
```json
["let", [
    ["is_active", ["lambda", ["user"], ["get", ["$", "/user"], "/active"]]],
    ["is_premium", ["lambda", ["user"], ["==", ["get", ["$", "/user"], "/plan"], "premium"]]],
    ["extract_name", ["lambda", ["user"], ["get", ["$", "/user"], "/name"]]],
    ["format_user_summary", ["lambda", ["user"], 
      ["obj",
        ["name", ["get", ["$", "/user"], "/name"]],
        ["status", ["if", 
          ["get", ["$", "/user"], "/active"], 
          "ACTIVE", 
          "INACTIVE"
        ]],
        ["plan_type", ["get", ["$", "/user"], "/plan"]]
      ]
    ]]
  ],
  ["obj",
    ["active_users", ["filter", ["get", ["$input"], "/users"], ["$", "/is_active"]]],
    ["premium_users", ["filter", ["get", ["$input"], "/users"], ["$", "/is_premium"]]],
    ["active_names", ["map", 
      ["filter", ["get", ["$input"], "/users"], ["$", "/is_active"]], 
      ["$", "/extract_name"]
    ]],
    ["user_summaries", ["map", 
      ["get", ["$input"], "/users"], 
      ["$", "/format_user_summary"]
    ]]
  ]
]
```

Using our familiar `users_input.json`, this produces:

**Output:**
```json
{
  "active_users": [
    { "name": "Alice", "active": true, "plan": "premium" },
    { "name": "Charlie", "active": true, "plan": "basic" }
  ],
  "premium_users": [
    { "name": "Alice", "active": true, "plan": "premium" }
  ],
  "active_names": ["Alice", "Charlie"],
  "user_summaries": [
    { "name": "Alice", "status": "ACTIVE", "plan_type": "premium" },
    { "name": "Bob", "status": "INACTIVE", "plan_type": "basic" },
    { "name": "Charlie", "status": "ACTIVE", "plan_type": "basic" }
  ]
}
```

#### Benefits of Lambda Variable Resolution

1. **Code Reuse**: Define complex transformations once, use them multiple times
2. **Readability**: Give descriptive names to your functions for self-documenting code
3. **Maintainability**: Change the logic in one place and it updates everywhere
4. **Performance**: Avoid redefining identical lambda functions
5. **Composition**: Build complex data pipelines by combining simple, named functions

#### Important Notes

- Lambda variables must be used with array operators (`map`, `filter`, etc.)
- They follow normal `let` scoping rules
- Parameters are still accessed using `["$", "/parameter_name"]` syntax
- You can mix stored lambdas with inline lambdas in the same script

This feature transforms Computo from a simple transformation tool into a powerful functional programming environment where you can build libraries of reusable transformation functions.

### String Concatenation with `str_concat`

When working with array transformations, you'll often need to build strings from multiple values. The `str_concat` operator allows you to concatenate (join together) multiple strings into a single string.

`["str_concat", <string1>, <string2>, <string3>, ...]`

The `str_concat` operator accepts any number of arguments and converts them to strings before joining them. This makes it perfect for building formatted messages, labels, or identifiers within your array transformations.

#### Basic String Concatenation

**Simple example:**
```json
["str_concat", "Hello, ", "World", "!"]
```
**Result:** `"Hello, World!"`

#### String Concatenation in Array Transformations

Let's apply this to our user data to create formatted user descriptions:

**`user_descriptions.json`:**
```json
["map",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"],
    ["str_concat",
      ["get", ["$", "/user"], "/name"],
      " (",
      ["get", ["$", "/user"], "/plan"],
      " plan) - ",
      ["if",
        ["get", ["$", "/user"], "/active"],
        "ACTIVE",
        "INACTIVE"
      ]
    ]
  ]
]
```

Using our familiar `users_input.json`, this produces:

**Output:**
```json
[
  "Alice (premium plan) - ACTIVE",
  "Bob (basic plan) - INACTIVE", 
  "Charlie (basic plan) - ACTIVE"
]
```

#### Type Conversion with `str_concat`

The `str_concat` operator automatically converts non-string values to strings, making it useful for combining different data types:

**`format_with_numbers.json`:**
```json
["let", [
    ["format_item", ["lambda", ["item"],
      ["str_concat",
        "Item #",
        ["get", ["$", "/item"], "/id"],
        ": ",
        ["get", ["$", "/item"], "/name"],
        " ($",
        ["get", ["$", "/item"], "/price"],
        ")"
      ]
    ]]
  ],
  ["map",
    {
      "array": [
        {"id": 1, "name": "Widget", "price": 25.99},
        {"id": 2, "name": "Gadget", "price": 15.50}
      ]
    },
    ["$", "/format_item"]
  ]
]
```

**Output:**
```json
[
  "Item #1: Widget ($25.99)",
  "Item #2: Gadget ($15.50)"
]
```

#### Practical Example: Building URLs

String concatenation is particularly useful for building URLs or paths:

**`build_user_urls.json`:**
```json
["map",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"],
    ["obj",
      ["name", ["get", ["$", "/user"], "/name"]],
      ["profile_url", ["str_concat", 
        "/users/",
        ["get", ["$", "/user"], "/name"],
        "/profile"
      ]],
      ["api_endpoint", ["str_concat",
        "https://api.example.com/v1/users/",
        ["get", ["$", "/user"], "/name"],
        "?plan=",
        ["get", ["$", "/user"], "/plan"]
      ]]
    ]
  ]
]
```

**Output:**
```json
[
  {
    "name": "Alice",
    "profile_url": "/users/Alice/profile",
    "api_endpoint": "https://api.example.com/v1/users/Alice?plan=premium"
  },
  {
    "name": "Bob",
    "profile_url": "/users/Bob/profile", 
    "api_endpoint": "https://api.example.com/v1/users/Bob?plan=basic"
  },
  {
    "name": "Charlie",
    "profile_url": "/users/Charlie/profile",
    "api_endpoint": "https://api.example.com/v1/users/Charlie?plan=basic"
  }
]
```

#### Combining with Lambda Variables

String concatenation works well with lambda variable resolution for creating reusable formatting functions:

**`reusable_formatters.json`:**
```json
["let", [
    ["full_name_formatter", ["lambda", ["person"],
      ["str_concat",
        ["get", ["$", "/person"], "/first_name"],
        " ",
        ["get", ["$", "/person"], "/last_name"]
      ]
    ]],
    ["email_formatter", ["lambda", ["person"],
      ["str_concat",
        ["get", ["$", "/person"], "/first_name"],
        ".",
        ["get", ["$", "/person"], "/last_name"],
        "@company.com"
      ]
    ]]
  ],
  ["map",
    {
      "array": [
        {"first_name": "John", "last_name": "Doe"},
        {"first_name": "Jane", "last_name": "Smith"}
      ]
    },
    ["lambda", ["person"],
      ["obj",
        ["full_name", ["$", "/full_name_formatter"]], // This applies the lambda stored in the variable
        ["email", ["$", "/email_formatter"]]           // This applies the lambda stored in the variable
      ]
    ]
  ]
]
```

**Note:** In this example, the lambda variables contain lambda functions that will be applied to the current `person` item in the map operation.

### In This Chapter

You've added array processing to your skillset. You have learned:
*   How to iterate over an array and transform each item using the **`map`** operator.
*   The syntax for **`lambda`** expressions to define the per-item transformation.
*   The special **`{"array": [...]}`** syntax for representing literal arrays.
*   How to combine `map` with `obj`, `if`, and `permuto.apply` for complex list transformations.
*   **Lambda variable resolution** for storing and reusing lambda functions in `let` bindings.
*   How to build complex, maintainable data processing pipelines with named, reusable functions.
*   The **`str_concat`** operator for combining multiple strings and building formatted text within transformations.

`map` is the first of several array operators. In the next chapters, we will explore others like `filter` and `reduce` to further refine our data pipelines.
