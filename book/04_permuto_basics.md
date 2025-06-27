## **Chapter 4: Permuto Basics - Templates**

In the last chapter, we used Computo's `obj` operator to manually construct a new JSON object piece by piece. This is perfect for when you need fine-grained logical control over every field. But often, your goal is simpler: you have a well-defined output structure and you just need to "fill in the blanks" with data from an input object.

This is a job for **templating**, and it's where **Permuto** shines.

Permuto is Computo's declarative partner. While Computo handles programmatic logic (`if`, `map`, etc.), Permuto handles declarative data shaping. Think of it as a smart, structure-aware "mail merge" for JSON.

### The Core Idea: Template + Context = Result

The Permuto workflow is simple and always involves two pieces of JSON:

1.  **The Template:** A JSON document that defines the desired output structure. It contains placeholders for where the dynamic data should go.
2.  **The Context:** A JSON document that provides the data to fill in the placeholders.

Permuto takes the template, substitutes the values from the context, and produces the final result.

### Placeholders and JSON Pointers

Permuto's placeholders use a simple `${...}` syntax. Inside the curly braces, you put the exact same **JSON Pointer** path that you used with Computo's `get` operator.

Let's revisit the user example from the previous chapter.

1.  First, create the **context** data. This is the same `input.json` we've been using, which provides the source data.

    **`input.json`:**
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

2.  Next, create the **template** file. This file defines the shape of our desired output.

    **`user_template.json`:**
    ```json
    {
      "profile_id": "${/user/id}",
      "full_name": "${/user/name}",
      "plan_type": "${/user/plan/name}"
    }
    ```
    Notice this template is just a plain JSON file. There are no operators, no arrays-as-actions. It's just a passive structure.

### Running a Permuto Template with `permuto.apply`

To use a Permuto template from within our Computo-driven workflow, we use the `permuto.apply` operator. This is the bridge between the two systems.

`["permuto.apply", <template>, <context>]`

1.  Create a script that uses this operator. Let's call it `apply_template.json`. It will use the `user_template.json` as the template and our `input.json` as the context.

    **`apply_template.json`:**
    ```json
    ["permuto.apply",
      {
        "profile_id": "${/user/id}",
        "full_name": "${/user/name}",
        "plan_type": "${/user/plan/name}"
      },
      ["$input"]
    ]
    ```
    *Note: For simplicity, we've embedded the template directly in our script. We could also load it from a file if it were more complex.*

2.  Now, run the script:

    ```bash
    ./build/computo apply_template.json input.json
    ```

The output is a new JSON object, perfectly matching the template's structure:
```json
{
  "full_name": "Alice",
  "plan_type": "premium",
  "profile_id": "u-123"
}
```

This is significantly more concise and readable than building the same object with `["obj", ["profile_id", ["get", ...]], ...]`.

### Type Preservation

A key feature of Permuto is that it preserves data types. If a placeholder resolves to a number, boolean, or even a complex object or array, that's what gets inserted into the final result.

Consider this template:
```json
{
  "plan_details": "${/user/plan}",
  "cost": "${/user/plan/monthly_cost}"
}
```
When applied to our `input.json`, this would produce:
```json
{
  "cost": 20,
  "plan_details": {
    "name": "premium",
    "monthly_cost": 20
  }
}
```
The `plan_details` key was populated with the entire plan sub-object, and `cost` was populated with the JSON number `20`, not the string `"20"`.

### String Interpolation

Permuto can also substitute placeholders inside of strings, a feature known as string interpolation. **This feature is disabled by default** and must be explicitly enabled with a command-line flag.

1.  Create a new template, `greeting_template.json`:
    ```json
    {
      "message": "Hello ${/user/name}! Your plan is ${/user/plan/name}."
    }
    ```

2.  Create a new script, `apply_greeting.json`, using this template:
    ```json
    ["permuto.apply",
      {
        "message": "Hello ${/user/name}! Your plan is ${/user/plan/name}."
      },
      ["$input"]
    ]
    ```

3.  Run it with the `--interpolation` flag:

    ```bash
    ./build/computo --interpolation apply_greeting.json input.json
    ```

The output shows the values correctly substituted within the string:
```json
{
  "message": "Hello Alice! Your plan is premium."
}
```

### In This Chapter

You've now seen the other half of the toolkit. You've learned:
*   How Permuto uses a **template** and a **context** to produce a result.
*   How to define placeholders using the **`${/json/pointer}`** syntax.
*   How to invoke Permuto from a Computo script using the **`permuto.apply`** operator.
*   How to enable **string interpolation** for more complex string construction.

You now have a clear understanding of the two distinct tools at your disposal:

*   **Computo:** For programmatic logic, calculations, and step-by-step construction.
*   **Permuto:** For declarative, whole-structure templating.

In the next part of this guide, we will dive deeper into Computo's more advanced features, starting with control flow and conditionals. You will see how to use Computo's logic to make intelligent decisions about which templates to apply and how to build the context for them.
