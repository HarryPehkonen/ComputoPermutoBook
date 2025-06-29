## **Chapter 5: Control Flow and Conditionals**

So far, our scripts have been linear. They execute from the inside out, following a single, predetermined path. To build truly dynamic transformations, we need the ability to make decisions. We need to be able to say: "If this condition is met, do this; otherwise, do that."

This is the role of the `if` operator in Computo.

### The `if` Operator

The `if` operator is the primary tool for conditional logic in Computo. Its structure is simple and should be familiar from other programming languages.

`["if", <condition>, <then_expression>, <else_expression>]`

The engine evaluates the `<condition>` expression first.
*   If the result is "truthy", the engine evaluates and returns the result of the `<then_expression>`.
*   If the result is "falsy", the engine evaluates and returns the result of the `<else_expression>`.

A crucial feature of `if` is **lazy evaluation**: only the branch that is chosen gets evaluated. The other branch is completely ignored, which is important for both performance and preventing errors.

### Computo's Definition of "Truthy" and "Falsy"

Since JSON has several data types, Computo has clear rules for what it considers `true` or `false` in a conditional context. These rules are very similar to those in languages like Python or JavaScript.

| Value Type | Falsy (evaluates to `false`) | Truthy (evaluates to `true`) |
| :--- | :--- | :--- |
| **Boolean** | `false` | `true` |
| **Number** | `0` and `0.0` | Any non-zero number |
| **String** | The empty string `""` | Any non-empty string |
| **Object** | The empty object `{}` | Any object with one or more keys |
| **Array** | The empty array `[]` or `{"array": []}` | Any array with one or more elements |
| **Null** | `null` | (never truthy) |

### Example: Conditional Greeting

Let's build a script that generates a different output based on whether a user is active.

1.  We'll start with a new `input.json` containing a list of users.

    **`users_input.json`:**
    ```json
    {
      "users": [
        { "name": "Alice", "active": true, "plan": "premium" },
        { "name": "Bob", "active": false, "plan": "basic" },
        { "name": "Charlie", "active": true, "plan": "basic" }
      ]
    }
    ```

2.  Now, let's write a script to process a single user. We'll use `let` to grab the first user from the array for simplicity.

    **`conditional_user.json`:**
    ```json
    ["let",
      [
        ["user", ["get", ["$input"], "/users/0"]]
      ],
      ["if",
        ["get", ["$", "/user"], "/active"],
        { "status": "Welcome!", "user_data": ["$", "/user"] },
        { "status": "Access Denied", "reason": "User is inactive" }
      ]
    ]
    ```

3.  Run the script:

    ```bash
    computo conditional_user.json users_input.json
    ```

The output will be:
```json
{
  "status": "Welcome!",
  "user_data": {
    "active": true,
    "name": "Alice",
    "plan": "premium"
  }
}
```
Because the `active` field for the first user (`Alice`) is `true`, the `then_expression` was evaluated and returned.

Now, change the `get` expression to select the second user, Bob: `["get", ["$input"], "/users/1"]`. Run the script again.

The output now reflects the `else_expression`:
```json
{
  "reason": "User is inactive",
  "status": "Access Denied"
}
```

### Pattern: Conditional Templating

The real power of `if` emerges when you combine it with `permuto.apply`. You can use Computo's logic to select the correct Permuto template based on input data.

Let's create two different Permuto templates.

**`active_user_template.json`:**
```json
{
  "message": "Welcome back, ${/name}!",
  "dashboard_url": "/dashboard",
  "plan": "${/plan}"
}
```

**`inactive_user_template.json`:**
```json
{
  "message": "Your account for ${/name} is inactive.",
  "reactivation_url": "/reactivate-account"
}
```

Now, we can write a script that uses `if` to choose which template to apply.

**`template_selector.json`:**
```json
["let",
  [
    ["user", ["get", ["$input"], "/users/0"]]
  ],
  ["if",
    ["get", ["$", "/user"], "/active"],
    ["permuto.apply",
      {
        "message": "Welcome back, ${/name}!",
        "dashboard_url": "/dashboard",
        "plan": "${/plan}"
      },
      ["$", "/user"]
    ],
    ["permuto.apply",
      {
        "message": "Your account for ${/name} is inactive.",
        "reactivation_url": "/reactivate-account"
      },
      ["$", "/user"]
    ]
  ]
]
```

Run this script (with the `--interpolation` flag to handle the strings):

```bash
computo --interpolation template_selector.json users_input.json
```

**Output for Alice (user 0):**
```json
{
  "dashboard_url": "/dashboard",
  "message": "Welcome back, Alice!",
  "plan": "premium"
}
```

**Output for Bob (if you change the script to user 1):**
```json
{
  "message": "Your account for Bob is inactive.",
  "reactivation_url": "/reactivate-account"
}
```

This pattern is incredibly powerful. Your application logic remains clean; it simply executes a Computo script. The complex conditional templating logic is entirely self-contained within the script data itself.

### In This Chapter

You've learned how to add decision-making to your transformations:
*   The syntax and behavior of the **`if`** operator.
*   The rules for **truthiness and falsiness** in Computo.
*   How to use `if` to return different JSON structures based on a condition.
*   The powerful pattern of using `if` to **conditionally apply different Permuto templates**.

So far we've only processed single data items. In the next chapter, we'll learn how to work with arrays, allowing us to process every item in a collection.
