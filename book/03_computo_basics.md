## **Chapter 3: Computo Basics - Data and Logic**

Now that you have a working environment, it's time to start transforming JSON. In this chapter, we'll focus on the core of Computo: its syntax, its fundamental operators, and how it handles data.

At its heart, Computo treats **code as data**. Every Computo script is itself a valid JSON document. This is a powerful concept borrowed from Lisp-like languages that makes scripts easy to generate, store, and even manipulate programmatically.

### The Anatomy of a Computo Expression

An "operation" in Computo is represented by a JSON array where the first element is a string identifying the operator.

```json
["+", 10, 5]
```

This is a Computo expression that instructs the engine to use the `+` operator on the numbers `10` and `5`. If you were to run this script, the engine would evaluate it and return the JSON number `15`.

Any JSON that isn't an operator call is treated as a **literal value**.

*   `42` evaluates to the number `42`.
*   `"hello"` evaluates to the string `"hello"`.
*   `{"name": "Alice"}` evaluates to a JSON object.

The magic happens when you start nesting these expressions.

### Your First Transformation: Simple Arithmetic

Let's start with the simplest possible script.

1.  Create a file named `add.json`:

    ```json
    ["+", 100, 50]
    ```

2.  Create an empty file for our input, `input.json`:
    *(Computo requires an input file, even if the script doesn't use it yet.)*

    ```json
    {}
    ```

3.  Now, run it from your terminal:

    ```bash
    ./build/computo add.json input.json
    ```

The output will be:
```json
150
```

The Computo engine evaluated the expression and printed the resulting JSON to your console. Now let's try nesting. Change `add.json` to:

```json
["+", 100, ["*", 5, 10]]
```

Run it again. The output is `150`. The engine first evaluated the inner expression `["*", 5, 10]` to get `50`, then evaluated the outer expression `["+", 100, 50]`.

### Accessing Input Data with `$input` and `get`

Static scripts are only so useful. The real power comes from transforming dynamic input data. Computo makes the entire contents of your `input.json` file available through a special, zero-argument operator: `$input`.

Let's create a more realistic scenario.

1.  Update `input.json` with some user data:

    ```json
    {
      "user": {
        "id": "u-123",
        "name": "Alice",
        "plan": {
          "name": "premium",
          "monthly_cost": 20
        }
      },
      "last_login_ts": 1672531200
    }
    ```

2.  Create a new script, `get_plan.json`, to extract the plan name. To do this, we need another operator: `get`.

    `["get", <object>, <json_pointer>]`

    The `get` operator takes an object to query and a [JSON Pointer](https://datatracker.ietf.org/doc/html/rfc6901) string to specify which value to extract.

    ```json
    ["get", ["$input"], "/user/plan/name"]
    ```

3.  Run the script:

    ```bash
    ./build/computo get_plan.json input.json
    ```

The output will be:
```json
"premium"
```
The engine first evaluated `["$input"]` to get the entire input object, then `get` extracted the value at `/user/plan/name`.

### Storing Intermediate Values with `let` and `$`

Often, you need to calculate an intermediate value and reuse it multiple times. Constantly re-evaluating long expressions like `["get", ["$input"], "/user/plan"]` would be tedious and inefficient.

Computo provides the `let` operator for binding values to variables within a specific scope.

`["let", [["var1", <expr1>], ...], <body_expr>]`

Variables defined in a `let` block are accessed using the `$` operator: `["$", "/var_name"]`. Note the required `/` prefix, which makes variable access look similar to root-level JSON Pointers.

Let's build a new user object containing just the name and monthly cost.

1.  Create a script named `build_user.json`:

    ```json
    ["let",
      [
        ["user_plan", ["get", ["$input"], "/user/plan"]],
        ["user_name", ["get", ["$input"], "/user/name"]]
      ],
      {
        "name": ["$", "/user_name"],
        "cost": ["get", ["$", "/user_plan"], "/monthly_cost"]
      }
    ]
    ```
    [CRITIQUE NEEDED]: The final object construction `{ "name": ..., "cost": ... }` uses a plain JSON object. While this works because the *values* are Computo expressions, it might be confusing. The `["obj", ...]` operator is more explicit. Should we introduce `obj` here for clarity, or save it for the dedicated "Objects" chapter and keep this simpler for now?

2.  Run the script with our previous `input.json`:

    ```bash
    ./build/computo build_user.json input.json
    ```

The output is a completely new JSON object, built from pieces of the input:

```json
{
  "cost": 20,
  "name": "Alice"
}
```

Here's the flow:
1.  `let` creates a new scope.
2.  It evaluates `["get", ["$input"], "/user/plan"]` and binds the resulting `{"name": "premium", "monthly_cost": 20}` object to the variable `user_plan`.
3.  It evaluates `["get", ["$input"], "/user/name"]` and binds the string `"Alice"` to the variable `user_name`.
4.  It then evaluates the body expression, substituting `["$", "/user_name"]` with `"Alice"` and using `get` on the `user_plan` object.

### In This Chapter

You've learned the fundamental building blocks of Computo:
*   The **syntax** of operators `["op", ...]` and literal values.
*   How to access the entire input document with **`$input`**.
*   How to extract specific data with **`get`** and JSON Pointers.
*   How to create temporary variables with **`let`** and access them with **`$`**.

These few operators are already enough to perform some powerful data extraction and reshaping. In the next chapter, we'll switch gears and look at Permuto, the templating engine that complements Computo's logic.
