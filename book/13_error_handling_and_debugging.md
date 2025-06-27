## **Chapter 13: Error Handling and Debugging**

In an ideal world, all of our scripts would run perfectly on the first try. In the real world, data is often messier than we expect, and scripts can contain subtle bugs. A robust system isn't just one that works when everything is perfect; it's one that behaves predictably and provides clear feedback when things go wrong.

This chapter covers how to handle errors gracefully within Computo and how to debug your scripts effectively.

### Types of Errors

When a Computo script fails, the engine will throw a structured exception. Understanding the different types of exceptions can help you quickly diagnose the problem. The main categories are:

*   **`InvalidScriptException`:** There is a fundamental structural problem with your script's JSON itself. This is rare if your JSON is well-formed.
*   **`InvalidOperatorException`:** You've tried to use an operator that doesn't exist. This is almost always a typo in the operator name (e.g., `["fliter", ...]` instead of `["filter", ...]`).
*   **`InvalidArgumentException`:** This is the most common category of error. It means an operator was called with the wrong number or type of arguments. Examples include:
    *   `["+", 1]` (not enough arguments)
    *   `["+", 1, "hello"]` (wrong argument type)
    *   `["get", <object>, "/non/existent/path"]` (invalid JSON Pointer)
    *   A `lambda` expression with the wrong structure.

When you run the `computo` CLI tool, it will catch these exceptions and print a descriptive error message to the console, which is your first and most important debugging tool.

### Defensive Programming: The `if` Guard

The most common source of runtime errors is unexpected input data. A script that works perfectly with one input might fail on another if a key is missing or a value has a different type. The `if` operator is your primary tool for defensive programming.

**Anti-Pattern: Assuming a Key Exists**
```json
["get", ["$input"], "/user/profile/name"]
```
This script will fail immediately if the `profile` key is missing from the `user` object.

**Defensive Pattern: Checking for Existence**
A better approach is to check if the data exists before trying to access it. While Computo doesn't have a dedicated `has_key` operator, you can often achieve the same result by checking the "truthiness" of a parent object.

```json
["let",
  [
    ["profile", ["get", ["$input"], "/user/profile"]]
  ],
  ["if",
    ["$", "/profile"],
    ["get", ["$", "/profile"], "/name"],
    "Default Name"
  ]
]
```
This script is more robust. It first tries to get the entire `profile` object. The `if` condition then checks if `profile` is truthy (i.e., not `null` or an empty object). Only if it's truthy does it attempt to get the `/name`. If not, it safely returns a default value.

*Note: This specific pattern doesn't guard against a `profile` object that exists but is missing the `name` key. A true `has_key` or `get_with_default` operator might be added in future versions of Computo to make this even cleaner.*

### The "Debug by Deconstruction" Technique

When a complex script fails and the error message isn't immediately obvious, the best way to debug is to **deconstruct the problem**.

Imagine this complex script fails:
```json
["reduce",
  ["map",
    ["filter", ["get", ["$input"], "/items"], <lambda1>],
    <lambda2>
  ],
  <lambda3>,
  0
]
```
Instead of trying to fix the whole thing at once, test each part in isolation.

1.  **Test the Innermost Part:** Create a new script that *only* contains the `filter` expression.
    `["filter", ["get", ["$input"], "/items"], <lambda1>]`
    Does it work? Does it produce the array you expect? If not, the problem is in your `filter` logic.

2.  **Test the Next Layer:** Once the `filter` works, wrap it in the `map`.
    `["map", [<working_filter_expression>], <lambda2>]`
    Does this produce the correct transformed array? If not, the bug is in your `map`'s lambda.

3.  **Test the Final Layer:** Once the `map` and `filter` produce the correct array, use that result as the input for your `reduce` operation.

By breaking the problem down and verifying the output of each stage of your pipeline, you can methodically isolate the source of the error. Using `let` can also help here, as you can bind the result of each stage to a variable and then output that variable directly to see the intermediate data.

### Using `permuto.apply` for Debug Output

Sometimes, the easiest way to see what's happening inside a script is to print out the state. The `permuto.apply` operator with string interpolation is a surprisingly effective debugging tool.

Let's say you're inside a `map` and you're not sure what the `user` variable contains at each step. You can insert a debugging string.

```json
["map",
  ["get", ["$input"], "/users"],
  ["lambda", ["user"],
    ["permuto.apply",
      {
        "debug_message": "Processing user: ${/name} with plan: ${/plan}",
        "original_user_obj": "${/}"
      },
      ["$", "/user"]
    ]
  ]
]
```
Running this with the `--interpolation` flag will produce an array of objects, where each object is a snapshot of the `user` variable at that point in the iteration. This can be invaluable for understanding why a filter isn't working or why a value isn't what you expect. The `${/}` pointer is particularly useful, as it resolves to the entire context object.

### In This Chapter

You've learned practical strategies for making your scripts robust and easier to debug.
*   You can diagnose issues by understanding Computo's **structured exception types**.
*   You can write **defensive scripts** that anticipate missing data by using `if` guards.
*   You know how to use the **"Debug by Deconstruction"** technique to methodically isolate bugs in complex pipelines.
*   You can use **`permuto.apply` as a "print statement"** to inspect the state of your variables during execution.

Writing code that handles failure gracefully is just as important as writing code that handles success. These techniques will help you build reliable, production-grade transformations.
