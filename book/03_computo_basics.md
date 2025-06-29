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
    computo add.json input.json
    ```

The output will be:
```
150
```

By default, Computo outputs JSON in compact form. For development and learning, you might prefer pretty-printed output:

```bash
computo --pretty=2 add.json input.json
```

This produces the same result but with proper indentation when dealing with complex structures.

### Understanding Output Formatting

The `--pretty=N` option controls how Computo formats its JSON output:

- **No flag (default)**: Compact output - `{"name":"Alice","age":30}`
- **`--pretty=2`**: Pretty-printed with 2-space indentation
- **`--pretty=4`**: Pretty-printed with 4-space indentation

For learning and development, we recommend using `--pretty=2` to make complex JSON structures easier to read. In production scripts or pipelines, you might prefer the compact default format for efficiency.

### Adding Comments to Scripts (CLI Only)

When working with complex transformations, you might want to add comments to your script files for documentation. The CLI tool supports this with the `--comments` flag:

```bash
# Enable comment parsing in script files
computo --comments --pretty=2 script_with_comments.json input.json
```

**Important**: Comments are only supported in **script files**, not input files, and only when using the CLI tool (not the C++ library API).

Example commented script:
```json
[
  // This creates a user profile object
  "obj", // obj creates a JSON object
  /* Extract the user's name from input data
     and format it for display */
  ["name", ["get", ["$input"], "/user/name"]],
  ["greeting", "Welcome!"] // Static greeting message
]
```

Supported comment styles:
- `// Single line comments`
- `/* Multi-line comments */`

The Computo engine evaluated the expression and printed the resulting JSON to your console. Now let's try nesting. Change `add.json` to:

```json
["+", 100, ["*", 5, 10]]
```

Run it again. The output is `150`. The engine first evaluated the inner expression `["*", 5, 10]` to get `50`, then evaluated the outer expression `["+", 100, 50]`.

### Creating Objects and Arrays

After experimenting with basic arithmetic, you might wonder how to create more complex JSON structures. Computo provides specific syntax for constructing objects and arrays.

#### Creating Objects with `obj`

To create a JSON object, use the `obj` operator with key-value pairs:

```json
["obj", ["key1", "value1"], ["key2", "value2"]]
```

Let's try this. Create a script called `make_object.json`:

```json
["obj", 
  ["name", "Alice"], 
  ["age", 30], 
  ["score", ["+", 85, 15]]
]
```

Run it:
```bash
computo --pretty=2 make_object.json input.json
```

Output:
```json
{
  "name": "Alice",
  "age": 30,
  "score": 100
}
```

Note: We're using `--pretty=2` to format the output with 2-space indentation for readability. Without this flag, the output would be compact: `{"name":"Alice","age":30,"score":100}`

Notice how the `score` value is computed from the nested arithmetic expression `["+", 85, 15]`.

#### Creating Arrays

For arrays, use the special `{"array": [...]}` syntax:

```json
{"array": [1, 2, ["*", 3, 4]]}
```

Create a script called `make_array.json`:

```json
{"array": [
  "hello",
  42,
  ["+", 10, 5],
  ["obj", ["type", "computed"], ["value", true]]
]}
```

Run it:
```bash
computo --pretty=2 make_array.json input.json
```

Output:
```json
[
  "hello",
  42,
  15,
  {
    "type": "computed",
    "value": true
  }
]
```

This array contains:
- A literal string `"hello"`
- A literal number `42`
- A computed number `15` from `["+", 10, 5]`
- A computed object from the `obj` operator

### **A Note on Syntax: Why `{"array": [...]}`?**

You may wonder why literal arrays are written as `{"array": [...]}` instead of a simpler `["arr", ...]` operator. This was a deliberate design choice for one critical reason: **to eliminate ambiguity**.

In Computo, a JSON array like `["operator", ...]` is always an action. But what about a simple array of strings, like `["red", "green", "blue"]`? Without a special rule, the interpreter would see `"red"` and think it's an invalid operator.

The `{"array": [...]}` syntax provides a clear, unambiguous signal to the interpreter: "Treat this as a literal piece of data, not an action to perform."

This allows the core rule—**arrays are for actions, objects are for data**—to hold true, making the language robust and predictable. It trades a small amount of verbosity for absolute clarity.

Now that you know how to construct basic data structures, let's learn how to work with dynamic input data.

### Accessing Input Data with `$input` and `get`

Static scripts are only so useful. The real power comes from transforming dynamic input data. Computo makes the entire contents of your `input.json` file available through a special, zero-argument operator: `$input`.  Please note that the name of the operator has nothing to do with the filename.

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
    computo get_plan.json input.json
    ```

The output will be:
```
"premium"
```

For simple values like strings, the `--pretty` flag doesn't make much difference, but it's helpful for complex structures.
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
      ["obj",
        ["name", ["$", "/user_name"]],
        ["cost", ["get", ["$", "/user_plan"], "/monthly_cost"]]
      ]
    ]
    ```

2.  Run the script with our previous `input.json`:

    ```bash
    computo --pretty=2 build_user.json input.json
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
*   How to **create objects** using the `obj` operator with key-value pairs.
*   How to **create arrays** using the `{"array": [...]}` syntax.
*   How to **format output** using the `--pretty=N` CLI option for readable JSON.
*   How to **add comments** to script files using the `--comments` CLI flag.
*   How to access the entire input document with **`$input`**.
*   How to extract specific data with **`get`** and JSON Pointers.
*   How to create temporary variables with **`let`** and access them with **`$`**.

These fundamental operators give you the power to construct new JSON structures and perform data extraction and reshaping. In the next chapter, we'll switch gears and look at Permuto, the templating engine that complements Computo's logic.
