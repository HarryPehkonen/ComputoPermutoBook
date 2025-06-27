## **Chapter 12: Performance and Optimization**

You've now seen how to solve complex problems with Computo and Permuto. As you move from writing small scripts to building business-critical data pipelines, performance becomes an important consideration.

The Computo engine is designed to be efficient, but the structure of your script can have a significant impact on its execution speed and memory usage. This chapter provides guidance on writing high-performance transformations and understanding the trade-offs involved.

### The Golden Rule: `let` is Your Best Friend

The single most important optimization technique in Computo is the proper use of the `let` operator.

**Anti-Pattern: Re-evaluating Expressions**
Consider this script that uses the same `get` expression multiple times:
```json
["obj",
  ["name", ["get", ["get", ["$input"], "/user"], "/profile"], "/name"]],
  ["email", ["get", ["get", ["$input"], "/user"], "/profile"], "/email"]]
]
```
The expression `["get", ["$input"], "/user"]` is evaluated twice. While this is a small example, in a complex script with many nested operators, this redundant work can add up.

**Optimized Pattern: Bind Once, Use Many Times**
By binding the result of an expensive or frequently used expression to a variable, you ensure it is evaluated only once.

```json
["let",
  [
    ["user_profile", ["get", ["get", ["$input"], "/user"], "/profile"]]
  ],
  ["obj",
    ["name", ["get", ["$", "/user_profile"], "/name"]],
    ["email", ["get", ["$", "/user_profile"], "/email"]]
  ]
]
```
This version is not only faster and more memory-efficient, but it's also significantly more readable. **When in doubt, use `let` to store the result of any non-trivial expression that you plan to use more than once.**

### Understanding Lazy Evaluation

Computo's `if` operator is "lazy." This means it only evaluates the branch that is actually chosen. The other branch is never touched. This has important performance implications.

**Inefficient: Evaluating Before the `if`**
```json
["let",
  [
    ["premium_dashboard", <... very expensive expression to build a dashboard ...>],
    ["basic_dashboard", <... another expensive expression ...>]
  ],
  ["if",
    ["get", ["$input"], "/user/is_premium"],
    ["$", "/premium_dashboard"],
    ["$", "/basic_dashboard"]
  ]
]
```
In this script, **both** the premium and basic dashboards are fully computed and stored in variables, even though only one will ever be used.

**Efficient: Evaluating Inside the `if`**
By moving the expensive expressions inside the `if` branches, you ensure that only the necessary work is done.

```json
["if",
  ["get", ["$input"], "/user/is_premium"],
  <... very expensive expression to build a dashboard ...>,
  <... another expensive expression ...>
]
```
This is a critical pattern for performance. **Defer expensive computations by placing them inside the branches of an `if` statement whenever possible.**

### Operator Performance Characteristics

Not all operators are created equal. Here is a general guide to their relative performance cost:

*   **Low Cost (Fast):** `+`, `-`, `*`, `/`, `==`, `>`, `get`, `$`, `obj`. These are typically very fast, often mapping to single machine instructions or efficient hash map lookups.
*   **Medium Cost (Depends on Data Size):** `merge`, `permuto.apply`. The cost of these operators is proportional to the size of the objects or templates they are processing.
*   **High Cost (Iterative):** `map`, `filter`, `reduce`. These are the most powerful operators, but also the most expensive. Their cost is directly proportional to the number of items in the array they are iterating over. A `map` over an array with 1,000,000 items will be 1,000 times slower than a `map` over an array with 1,000 items.

### Pipeline Ordering Matters

The order of your chained array operations can have a massive impact on performance. The key principle is to **reduce the size of your dataset as early as possible.**

**Anti-Pattern: `map` before `filter`**
Imagine you need to get the names of all active users.
```json
["map",
  ["filter",
    ["map",
      ["get", ["$input"], "/users"],
      ["lambda", ["u"], ["obj", ["name", ["get",...]], ["active", ["get",...]]]]
    ],
    ["lambda", ["u"], ["get", ["$", "/u"], "/active"]]
  ],
  ["lambda", ["u"], ["get", ["$", "/u"], "/name"]]
]
```
This is highly inefficient. If you have 10,000 users, the first `map` operation will create 10,000 new, temporary objects in memory. Then, `filter` will iterate over those 10,000 new objects and likely discard most of them.

**Optimized Pattern: `filter` before `map`**
```json
["map",
  ["filter",
    ["get", ["$input"], "/users"],
    ["lambda", ["u"], ["get", ["$", "/u"], "/active"]]
  ],
  ["lambda", ["u"], ["get", ["$", "/u"], "/name"]]
]
```
This version is dramatically better. The `filter` operator runs first on the raw input. If only 100 users are active, the subsequent `map` only has to do work on those 100 items. It creates far fewer temporary objects and performs fewer iterations.

**Always filter as early as you can to reduce the amount of data that later stages in your pipeline need to process.**

### In This Chapter

You've learned the core principles of writing high-performance Computo scripts:
*   Use **`let`** to avoid re-evaluating expressions.
*   Leverage the **lazy evaluation** of the `if` operator to defer expensive work.
*   Understand the relative performance costs of different operators.
*   Structure your array pipelines to **`filter` early and `map` late**.

By applying these principles, you can ensure that your transformations are not only correct but also fast and efficient enough for production workloads. The final chapters will cover error handling and best practices to round out your expertise.
