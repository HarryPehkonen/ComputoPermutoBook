## **Appendix A: Complete Operator Reference**

This appendix provides a quick reference for all 29 operators available in Computo.

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
Returns the entire input JSON document that was provided to the script (equivalent to the first input when multiple inputs are provided).
*   **Syntax:** `["$input"]`
*   **Example:** If `input.json` is `{"id": 1}`, `["$input"]` -> `{"id": 1}`

---
#### `$inputs`
Returns an array containing all input JSON documents that were provided to the script.
*   **Syntax:** `["$inputs"]`
*   **Example:** If called with `input1.json` and `input2.json`, returns `[<input1_content>, <input2_content>]`

### Logic & Control Flow

---
#### `if`
Evaluates a condition and returns one of two expressions.
*   **Syntax:** `["if", <condition>, <then_expr>, <else_expr>]`
*   **Example:** `["if", true, "Yes", "No"]` -> `"Yes"`

---
#### `&&`
Logical AND operator with short-circuit evaluation. Returns `true` only if all arguments are truthy.
*   **Syntax:** `["&&", <expr1>, <expr2>, <expr3>, ...]`
*   **Example:** `["&&", true, [">", 10, 5], ["!=", "hello", ""]]` -> `true`
*   **Short-circuit:** Stops evaluating at first falsy value

---
#### `||`
Logical OR operator with short-circuit evaluation. Returns `true` if any argument is truthy.
*   **Syntax:** `["||", <expr1>, <expr2>, <expr3>, ...]`
*   **Example:** `["||", false, ["==", 2, 2]]` -> `true`
*   **Short-circuit:** Stops evaluating at first truthy value

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

### JSON Patch Operations (RFC 6902)

---
#### `diff`
Generates an RFC 6902 JSON Patch array that describes the differences between two JSON documents.
*   **Syntax:** `["diff", <original_document>, <modified_document>]`
*   **Example:** `["diff", {"status": "active"}, {"status": "archived"}]` -> `[{"op": "replace", "path": "/status", "value": "archived"}]`

---
#### `patch`
Applies an RFC 6902 JSON Patch array to a document, returning the modified document.
*   **Syntax:** `["patch", <document_to_patch>, <patch_array>]`
*   **Example:** `["patch", {"status": "active"}, [{"op": "replace", "path": "/status", "value": "archived"}]]` -> `{"status": "archived"}`

### Mathematical

---
#### `+`, `-`, `*`, `/`
Performs a mathematical operation on two numbers.
*   **Syntax:** `["<op>", <num1_expr>, <num2_expr>]`
*   **Example:** `["*", 5, 10]` -> `50`

### Lambda Functions

---
#### `lambda`
Defines an anonymous function for use with array operators. **Used ONLY with array operators** (`map`, `filter`, `reduce`, `find`, `some`, `every`, `flatMap`).

*   **Syntax:** `["lambda", ["param1", "param2", ...], <body_expression>]`

*   **How Lambda Works:**
    1. **Parameter Declaration:** The second element is an array of parameter names (as strings)
    2. **Body Expression:** The third element is the expression that gets executed
    3. **Parameter Access:** Inside the body, access parameters using `["$", "/param_name"]`

*   **Single Parameter Example:** 
    `["lambda", ["x"], ["+", ["$", "/x"], 1]]` - adds 1 to parameter `x`

*   **Two Parameter Example (for `reduce`):** 
    `["lambda", ["acc", "item"], ["+", ["$", "/acc"], ["$", "/item"]]]` - adds `item` to accumulator `acc`

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
Returns the number of items in an array.
*   **Syntax:** `["count", <array_expr>]`
*   **Example:** `["count", {"array": [1, 2, 3]}]` -> `3`

### List Processing (Functional)

---
#### `car`
Returns the first element of an array. Inspired by Lisp's car function.
*   **Syntax:** `["car", <array_expr>]`
*   **Example:** `["car", {"array": [1, 2, 3]}]` -> `1`
*   **Note:** Throws `InvalidArgumentException` if array is empty or argument is not an array

---
#### `cdr` 
Returns all elements except the first from an array. Inspired by Lisp's cdr function.
*   **Syntax:** `["cdr", <array_expr>]`
*   **Example:** `["cdr", {"array": [1, 2, 3]}]` -> `[2, 3]`
*   **Note:** Returns empty array `[]` if input array is empty; throws `InvalidArgumentException` if argument is not an array
