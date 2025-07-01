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

### Logical Operators: `&&` and `||`

For more complex conditional logic, Computo provides logical AND (`&&`) and OR (`||`) operators. These operators support **short-circuit evaluation**, meaning they stop evaluating as soon as the result is determined.

#### The `&&` (Logical AND) Operator

The `&&` operator returns `true` only if **all** of its arguments are truthy. It evaluates arguments from left to right and stops as soon as it encounters a falsy value.

`["&&", <expr1>, <expr2>, <expr3>, ...]`

**Examples:**
```json
// All conditions must be true
["&&", true, [">", 10, 5], ["!=", "hello", ""]]
// Result: true (all are truthy)

// Short-circuit evaluation - stops at first falsy value
["&&", false, ["/", 1, 0]]
// Result: false (division never evaluated, preventing error)

// Practical example: user validation
["&&", 
  ["get", ["$", "/user"], "/active"],
  [">", ["get", ["$", "/user"], "/age"], 18],
  ["!=", ["get", ["$", "/user"], "/status"], "banned"]
]
```

#### The `||` (Logical OR) Operator

The `||` operator returns `true` if **any** of its arguments are truthy. It evaluates arguments from left to right and stops as soon as it encounters a truthy value.

`["||", <expr1>, <expr2>, <expr3>, ...]`

**Examples:**
```json
// Any condition can be true
["||", false, ["==", 2, 2], ["!=", "a", "a"]]
// Result: true (stops at second argument)

// Practical example: role checking
["||", 
  ["==", ["get", ["$", "/user"], "/role"], "admin"],
  ["==", ["get", ["$", "/user"], "/role"], "moderator"],
  ["==", ["get", ["$", "/user"], "/role"], "owner"]
]
```

#### Combining Logical Operators with `if`

These operators are particularly powerful when used as conditions in `if` statements:

**`advanced_user_check.json`:**
```json
["let",
  [
    ["user", ["get", ["$input"], "/users/0"]]
  ],
  ["if",
    ["&&",
      ["get", ["$", "/user"], "/active"],
      ["||",
        ["==", ["get", ["$", "/user"], "/plan"], "premium"],
        [">", ["get", ["$", "/user"], "/credits"], 100]
      ]
    ],
    { 
      "access": "granted", 
      "level": "full",
      "user": ["$", "/user"]
    },
    { 
      "access": "denied", 
      "reason": "User must be active and either premium or have 100+ credits"
    }
  ]
]
```

This script grants full access only if:
1. The user is active AND
2. The user has either a premium plan OR more than 100 credits

The logical operators make complex business rules much more readable than nested `if` statements.

#### Short-Circuit Evaluation Benefits

Short-circuit evaluation provides two key benefits:

1. **Performance**: Unnecessary computations are avoided
2. **Safety**: Potentially error-causing expressions aren't evaluated

```json
// Safe division check
["&&", ["!=", ["$", "/divisor"], 0], [">", ["/", ["$", "/dividend"], ["$", "/divisor"]], 10]]
// If divisor is 0, division is never attempted

// Safe array access
["&&", [">", ["count", ["$", "/items"]], 0], ["!=", ["get", ["$", "/items"], "/0/status"], "deleted"]]
// If array is empty, array access is never attempted
```

### Approximate Equality: The `approx` Operator

When working with floating-point numbers, exact equality comparisons can be problematic due to precision issues. The `approx` operator provides a solution for comparing numbers within a specified tolerance.

`["approx", <number1>, <number2>, <epsilon>]`

The `approx` operator returns `true` if the absolute difference between the two numbers is less than or equal to the epsilon value.

#### Basic Floating-Point Comparison

**Example: Comparing calculated values**

```json
[
  /* Compare a calculated result with an expected value */
  "approx", 
  ["/", 22, 7],        /* 22/7 = 3.142857... */
  3.14159,             /* Expected π approximation */
  0.01                 /* Tolerance of 0.01 */
]
```

**Output:** `true` (because the difference is less than 0.01)

#### Practical Use Cases

**`temperature_comparison.json`:**
```json
["let",
  [
    ["sensor1_temp", 23.456],
    ["sensor2_temp", 23.461],
    ["tolerance", 0.01]
  ],
  ["obj",
    /* Check if sensor readings are approximately equal */
    ["sensors_match", [
      "approx", 
      ["$", "/sensor1_temp"], 
      ["$", "/sensor2_temp"], 
      ["$", "/tolerance"]
    ]],
    
    /* Traditional exact comparison would likely fail */
    ["exact_match", [
      "==", 
      ["$", "/sensor1_temp"], 
      ["$", "/sensor2_temp"]
    ]],
    
    ["difference", [
      "-", 
      ["$", "/sensor2_temp"], 
      ["$", "/sensor1_temp"]
    ]]
  ]
]
```

**Output:**
```json
{
  "sensors_match": true,
  "exact_match": false,
  "difference": 0.005
}
```

#### Financial Calculations

Approximate equality is particularly useful in financial calculations where rounding errors are common:

**`budget_validation.json`:**
```json
["let",
  [
    /* Calculate total from individual items */
    ["calculated_total", [
      "+", 
      ["+", 19.99, 24.95], 
      ["*", 1.08, 44.94]  /* Add 8% tax */
    ]],
    
    /* Expected total from external system */
    ["expected_total", 48.53],
    
    /* Penny tolerance for financial calculations */
    ["penny_tolerance", 0.01]
  ],
  ["obj",
    ["totals_match", [
      "approx",
      ["$", "/calculated_total"],
      ["$", "/expected_total"], 
      ["$", "/penny_tolerance"]
    ]],
    ["calculated", ["$", "/calculated_total"]],
    ["expected", ["$", "/expected_total"]]
  ]
]
```

#### Combining with Conditional Logic

The `approx` operator works seamlessly with `if` and logical operators:

**`quality_control.json`:**
```json
["let",
  [
    ["measured_weight", 10.003],
    ["target_weight", 10.0],
    ["tolerance", 0.005]
  ],
  ["if",
    ["approx", 
      ["$", "/measured_weight"], 
      ["$", "/target_weight"], 
      ["$", "/tolerance"]
    ],
    {
      "status": "PASS",
      "message": "Weight within acceptable tolerance"
    },
    ["obj",
      ["status", "FAIL"],
      ["message", "Weight exceeds tolerance"],
      ["deviation", [
        "-", 
        ["$", "/measured_weight"], 
        ["$", "/target_weight"]
      ]]
    ]
  ]
]
```

**Why Not Regular Comparison?**

Consider this problematic scenario without `approx`:

```json
/* This might unexpectedly return false due to floating-point precision */
["==", ["/", 1, 3], 0.3333333333333333]

/* This is more reliable for floating-point comparisons */
["approx", ["/", 1, 3], 0.3333333333333333, 0.0001]
```

The `approx` operator provides a robust solution for real-world applications where perfect precision isn't possible or necessary.

### Logical NOT: The `not` Operator

Sometimes you need to negate a boolean value or invert the truthiness of an expression. The `not` operator provides this functionality.

`["not", <expression>]`

The `not` operator evaluates its argument and returns the logical opposite:
- If the argument is truthy, `not` returns `false`
- If the argument is falsy, `not` returns `true`

**Examples:**

```json
// Basic boolean negation
["not", true]        // Result: false
["not", false]       // Result: true

// Negating comparison results
["not", [">", 5, 10]]    // Result: true (because 5 > 10 is false)
["not", ["==", "a", "a"]] // Result: false (because "a" == "a" is true)
```

#### Practical Use Cases

**Checking for empty collections:**

```json
// Check if an array is NOT empty
["not", ["==", ["count", ["$", "/items"]], 0]]

// Check if a string is NOT empty  
["not", ["==", ["$", "/message"], ""]]

// Check if an object is NOT empty
["not", ["==", ["$", "/config"], {}]]
```

**Inverting complex conditions:**

```json
["let",
  [
    ["user", ["get", ["$input"], "/user"]]
  ],
  ["if",
    ["not", 
      ["&&",
        ["get", ["$", "/user"], "/active"],
        [">=", ["get", ["$", "/user"], "/age"], 18]
      ]
    ],
    {
      "access": "denied",
      "reason": "User must be active and 18 or older"
    },
    {
      "access": "granted",
      "user_data": ["$", "/user"]
    }
  ]
]
```

This script denies access if the user is NOT (active AND 18+), which is equivalent to saying the user is either inactive OR under 18.

#### Understanding Truthiness with `not`

The `not` operator follows Computo's truthiness rules:

```json
// These evaluate to true (because the inputs are falsy)
["not", 0]           // true (0 is falsy)
["not", ""]          // true (empty string is falsy)
["not", []]          // true (empty array is falsy)
["not", {}]          // true (empty object is falsy)
["not", null]        // true (null is falsy)

// These evaluate to false (because the inputs are truthy)
["not", 42]          // false (non-zero number is truthy)
["not", "hello"]     // false (non-empty string is truthy)
["not", {"a": 1}]    // false (non-empty object is truthy)
```

#### Combining `not` with Other Logical Operators

The `not` operator works well with other logical operators to create complex expressions:

```json
// Check if user is NOT an admin AND NOT a moderator
["&&",
  ["not", ["==", ["get", ["$", "/user"], "/role"], "admin"]],
  ["not", ["==", ["get", ["$", "/user"], "/role"], "moderator"]]
]

// Alternative using De Morgan's law - this is equivalent to the above
["not", 
  ["||",
    ["==", ["get", ["$", "/user"], "/role"], "admin"],
    ["==", ["get", ["$", "/user"], "/role"], "moderator"]
  ]
]
```

**Validation example:**

```json
["let",
  [
    ["email", ["get", ["$input"], "/email"]],
    ["password", ["get", ["$input"], "/password"]]
  ],
  ["if",
    ["||",
      ["not", ["$", "/email"]],           // Email is falsy (missing/empty)
      ["not", ["$", "/password"]],        // Password is falsy (missing/empty)
      ["<", ["count", ["$", "/password"]], 8]  // Password too short
    ],
    {
      "valid": false,
      "error": "Email and password are required, password must be 8+ characters"
    },
    {
      "valid": true,
      "message": "Credentials accepted"
    }
  ]
]
```

### In This Chapter

You've learned how to add decision-making to your transformations:
*   The syntax and behavior of the **`if`** operator.
*   The rules for **truthiness and falsiness** in Computo.
*   How to use `if` to return different JSON structures based on a condition.
*   The powerful pattern of using `if` to **conditionally apply different Permuto templates**.
*   The **`&&` (logical AND)** and **`||` (logical OR)** operators for complex conditional logic.
*   How **short-circuit evaluation** improves performance and safety.
*   Combining logical operators to create readable business rule expressions.
*   The **`not`** operator for negating boolean values and inverting truthiness.
*   The **`approx`** operator for robust floating-point number comparisons with tolerance.
*   Practical applications of approximate equality in financial and scientific calculations.

So far we've only processed single data items. In the next chapter, we'll learn how to work with arrays, allowing us to process every item in a collection.
