## **Chapter 7: Object Construction and Manipulation**

In modern data exchange, much of the work involves creating, reshaping, and merging JSON objects. In previous chapters, we've seen how to construct objects piece-by-piece using `obj`. This chapter will formalize those patterns and introduce new tools for more complex object manipulation.

### Review: The `obj` Operator

As a quick refresher, the `obj` operator is the most fundamental way to build a new JSON object. It takes a series of `[key, value]` pairs and assembles them into an object.

`["obj", ["key1", <value_expr1>], ["key2", <value_expr2>], ...]`

The keys must be literal strings, but the values can be any valid Computo expression. This allows you to construct objects from a mix of static and dynamic data.

**Example: Building a metadata object**
```json
["obj",
  ["timestamp", 1672531200],
  ["source", "api-gateway"],
  ["user_id", ["get", ["$input"], "/user/id"]],
  ["is_premium_user", [">", ["get", ["$input"], "/user/credits"], 100]]
]
```

This expression creates a new object by:
*   Using two literal values (`1672531200` and `"api-gateway"`).
*   Extracting a value directly from the input using `get`.
*   Calculating a boolean value using the `>` comparison operator.

### New Operator: `merge`

A common task is to combine multiple objects. For example, you might have a set of default configuration values that you want to override with user-specific settings. Doing this manually with `obj` and `if` would be tedious.

Computo provides the `merge` operator for this exact purpose.

`["merge", <object1>, <object2>, <object3>, ...]`

The `merge` operator takes two or more expressions that evaluate to objects and combines them into a single new object. If multiple source objects contain the same key, the value from the **rightmost** object wins.

#### `merge` Example: Default and User Settings

Let's imagine our application has default settings, but we want to allow a user to override them.

1.  **`settings_input.json`:**
    ```json
    {
      "user_preferences": {
        "theme": "dark",
        "notifications": {
          "email": false
        }
      }
    }
    ```

2.  **`merge_settings.json`:**
    In this script, we'll define a default settings object and merge the user's preferences over it.

    ```json
    ["let",
      [
        ["defaults", {"obj":
          [
            ["theme", "light"],
            ["notifications", {"obj": [
              ["email", true],
              ["sms", true]
            ]}],
            ["language", "en-US"]
          ]}
        ],
        ["user_prefs", ["get", ["$input"], "/user_preferences"]]
      ],
      ["merge", ["$", "/defaults"], ["$", "/user_prefs"]]
    ]
    ```

3.  Run the script:

    ```bash
    ./build/computo merge_settings.json settings_input.json
    ```

**Output:**
```json
{
  "language": "en-US",
  "notifications": {
    "email": false
  },
  "theme": "dark"
}
```

Let's analyze the result:
*   `language`: `"en-US"` was preserved from the default settings because it didn't exist in the user's preferences.
*   `theme`: `"dark"` from the user's preferences (the rightmost object) overwrote the default of `"light"`.
*   `notifications`: This is a **shallow merge**. The `notifications` *object* from the user preferences completely replaced the default `notifications` object. The `sms: true` key from the defaults is gone.

This shallow merge behavior is intentional and predictable. For a "deep" or recursive merge, you would need to apply `merge` at each level of the object hierarchy.

### Pattern: Creating Dynamic Keys

A limitation of the `obj` operator is that keys must be literal strings. You cannot use an expression to generate a key name dynamically.

While Computo doesn't have a direct "dynamic key" operator, you can achieve this result by combining `map` and `merge`. The pattern is to create an array of single-key objects and then merge them all together.

Let's say we have an array of settings and we want to turn it into a key-value map.

1.  **`kv_input.json`:**
    ```json
    {
      "settings_list": [
        { "key": "user_theme", "value": "dark" },
        { "key": "user_font_size", "value": 14 },
        { "key": "user_id", "value": "u-456" }
      ]
    }
    ```

2.  **`dynamic_keys.json`:**
    This script is a bit more advanced. It uses `map` to turn each item into a single-key object, and then uses `reduce` (which we'll cover in detail later) with `merge` to combine them.

    ```json
    ["reduce",
      ["map",
        ["get", ["$input"], "/settings_list"],
        ["lambda", ["item"],
          ["obj",
            [
              ["get", ["$", "/item"], "/key"],
              ["get", ["$", "/item"], "/value"]
            ]
          ]
        ]
      ],
      ["lambda", ["acc", "obj"], ["merge", ["$", "/acc"], ["$", "/obj"]]],
      {}
    ]
    ```
    *Note: This is an advanced preview of `reduce`. Don't worry if it's not fully clear yet; the key takeaway is the `map`-then-`merge` pattern.*

**Output:**
```json
{
  "user_font_size": 14,
  "user_id": "u-456",
  "user_theme": "dark"
}
```

This pattern demonstrates how you can compose Computo's core operators to achieve sophisticated results that might otherwise seem to require a dedicated operator.

### In This Chapter

You've deepened your understanding of how to work with objects in Computo.
*   You've reviewed the **`obj`** operator for explicit object construction.
*   You've learned to use the **`merge`** operator to combine multiple objects, with a clear "right-most wins" rule for conflicting keys.
*   You've seen an advanced pattern for creating objects with **dynamic keys** by composing `map` and `merge`.

With these tools, you have complete control over the shape and content of the JSON objects you produce. In the next chapter, we will return to arrays and explore the remaining powerhouse operators: `filter` and `reduce`.
