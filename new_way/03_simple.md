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


### Mathematical Operations

Computo supports all standard arithmetic operations. In addition to the `+`, `-`, `*`, and `/` operators you've seen, there's also the modulo operator `%` for finding remainders:

```json
["%", 17, 5]
```

This would return `2` (the remainder when 17 is divided by 5).

The modulo operator is particularly useful for tasks like:
- **Determining even/odd numbers**: `["%", number, 2]` returns `0` for even, `1` for odd
- **Cyclic operations**: Creating repeating patterns or rotations
- **Validation**: Checking if numbers are divisible by specific values


### In This Chapter

You've learned the fundamental building blocks of Computo:
*   The **syntax** of operators `["op", ...]` and literal values.
*   **Mathematical operations** including the modulo operator `%` for remainders.

These fundamental operators give you the power to construct new JSON structures and perform data extraction and reshaping. In the next chapter, we'll switch gears and look at Permuto, the templating engine that complements Computo's logic.

