## **Appendix A: Complete Operator Reference**

This appendix provides a quick reference for all 22 operators available in Computo.

### Data Access & Scoping

---
#### `let`
Binds variables to expressions for use within a scoped body.
*   **Syntax:** `["let", [["var1", <expr1>], ...], <body_expr>]`
*   **Example:** `["let", [["x", 5]], ["+", ["$", "/x"], 10]]` -> `15`

---
#### `$`
Retrieves the value of a variable defined by `let`.
*   **Syntax:** `["$", "/variable_name"]`
*   **Example:** `["let", [["x", 5]], ["$", "/x"]]` -> `5`

---
#### `get`
Retrieves a value from a JSON object or array using a JSON Pointer.
*   **Syntax:** `["get", <object_expr>, <json_pointer_string>]`
*   **Example:** `["get", {"obj": {"a": 1}}, "/obj/a"]` -> `1`

---
#### `$input`
Returns the entire input JSON document that was provided to the script.
*   **Syntax:** `["$input"]`
*   **Example:** If `input.json` is `{"id": 1}`, `["$input"]` -> `{"id": 1}`

### Logic & Control Flow

---
#### `if`
Evaluates a condition and returns one of two expressions.
*   **Syntax:** `["if", <condition>, <then_expr>, <else_expr>]`
*   **Example:** `["if", true, "Yes", "No"]` -> `"Yes"`

---
#### `==`, `!=`, `>`, `<`, `>=`, `<=`
Perform a comparison between two values. Math comparisons require numbers.
*   **Syntax:** `["<op>", <expr1>, <expr2>]`
*   **Example:** `[">", 10, 5]` -> `true`
*   **Example:** `["==", "a", "a"]` -> `true`

---
#### `approx`
Checks if two numbers are approximately equal within a given epsilon.
*   **Syntax:** `["approx", <num1_expr>, <num2_expr>, <epsilon_expr>]`
*   **Example:** `["approx", 3.14, 3.141, 0.01]` -> `true`

### Data Construction & Manipulation

---
#### `obj`
Creates a JSON object from key-value pairs.
*   **Syntax:** `["obj", ["key1", <val1>], ["key2", <val2>], ...]`
*   **Example:** `["obj", ["a", 1], ["b", 2]]` -> `{"a": 1, "b": 2}`

---
#### `merge`
Merges two or more objects. Rightmost keys win in case of conflict.
*   **Syntax:** `["merge", <obj1_expr>, <obj2_expr>, ...]`
*   **Example:** `["merge", {"a": 1, "b": 1}, {"b": 2, "c": 3}]` -> `{"a": 1, "b": 2, "c": 3}`

---
#### `permuto.apply`
Applies a Permuto template to a context object.
*   **Syntax:** `["permuto.apply", <template_expr>, <context_expr>]`
*   **Example:** `["permuto.apply", {"id": "${/user_id}"}, {"user_id": 123}]` -> `{"id": 123}`

### Mathematical

---
#### `+`, `-`, `*`, `/`
Performs a mathematical operation on two numbers.
*   **Syntax:** `["<op>", <num1_expr>, <num2_expr>]`
*   **Example:** `["*", 5, 10]` -> `50`

### Array Operators

*Note: For all array operators, literal arrays must be specified using `{"array": [...]}` syntax.*

---
#### `map`
Applies a lambda to each item in an array, returning a new array of transformed items.
*   **Syntax:** `["map", <array_expr>, ["lambda", ["item_var"], <transform_expr>]]`
*   **Example:** `["map", {"array": [1,2]}, ["lambda",["x"],["+",["$","/x"],1]]]` -> `[2, 3]`

---
#### `filter`
Returns a new array containing only items for which the lambda returns a truthy value.
*   **Syntax:** `["filter", <array_expr>, ["lambda", ["item_var"], <condition_expr>]]`
*   **Example:** `["filter", {"array": [0,1,2]}, ["lambda",["x"],["$", "/x"]]]` -> `[1, 2]`

---
#### `reduce`
Reduces an array to a single value by applying a two-argument lambda.
*   **Syntax:** `["reduce", <array_expr>, ["lambda", ["acc", "item"], <expr>], <initial_value>]`
*   **Example:** `["reduce", {"array": [1,2,3]}, ["lambda",["a","i"],["+",["$","/a"],["$","/i"]]], 0]` -> `6`

---
#### `find`
Returns the **first item** in an array for which the lambda returns a truthy value, or `null` if no match is found.
*   **Syntax:** `["find", <array_expr>, ["lambda", ["item_var"], <condition_expr>]]`
*   **Example:** `["find", {"array": [1,5,10]}, ["lambda",["x"],[">",["$","/x"],3]]]` -> `5`

---
#### `some`
Returns `true` if the lambda returns a truthy value for **at least one item** in the array, `false` otherwise.
*   **Syntax:** `["some", <array_expr>, ["lambda", ["item_var"], <condition_expr>]]`
*   **Example:** `["some", {"array": [1,5,10]}, ["lambda",["x"],["==",["$","/x"],5]]]` -> `true`

---
#### `every`
Returns `true` if the lambda returns a truthy value for **all items** in the array, `true` for an empty array, `false` otherwise.
*   **Syntax:** `["every", <array_expr>, ["lambda", ["item_var"], <condition_expr>]]`
*   **Example:** `["every", {"array": [2,4,6]}, ["lambda",["x"],["==",["%",["$","/x"],2],0]]]` -> `true`

---
#### `flatMap`
Like `map`, but if a lambda returns an array, its items are flattened into the result array.
*   **Syntax:** `["flatMap", <array_expr>, ["lambda", ["item_var"], <transform_expr>]]`
*   **Example:** `["flatMap", {"array": [1,2]}, ["lambda",["x"],{"array":[["$","/x"],["$","/x"]]}]` -> `[1, 1, 2, 2]`

---
#### `count`
Returns the number of items in an array. *(Note: this was proposed in a pattern but is not a formally implemented operator in the C++ code. I am assuming it should exist based on the context of the book.)*
*   **Syntax:** `["count", <array_expr>]`
*   **Example:** `["count", {"array": [1, 2, 3]}]` -> `3`

---
[CRITIQUE NEEDED]: I noticed that the `count` operator was used in Chapter 10's Aggregation Pipeline pattern, but it's not actually defined in the C++ implementation (`src/computo.cpp`) or tested in `tests/test_operators.cpp`.

1.  Was this an oversight, and should we add `count` to the implementation? It's a very useful and simple addition.
2.  Or should I remove `count` from the book and rewrite the example in Chapter 10 to use a different method (e.g., `["reduce", ..., 1]]` which is much clunkier)?

My recommendation is to add the `count` operator. For now, I will leave it in this reference.
