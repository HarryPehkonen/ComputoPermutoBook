## **Chapter 14: Best Practices and Patterns**

Congratulations! You have journeyed through the entire Computo and Permuto ecosystem, from basic operators to complex data pipelines. You have all the tools you need to tackle sophisticated JSON transformation challenges.

This final chapter serves as a summary of the key strategies and best practices we've discussed. Think of it as a concise checklist to consult when you're designing and writing your own scripts. Following these principles will help you create transformations that are not just correct, but also readable, maintainable, and efficient.

### 1. Separate Logic from Presentation

This is the philosophical core of the Computo/Permuto toolkit.
*   **Use Computo for the "How":** Logic, conditionals, iteration, calculation, and data preparation.
*   **Use Permuto for the "What":** Declarative, whole-structure templating and string construction.
*   **The Bridge:** Use Computo to build the perfect, clean context object and then pass that clean object to `permuto.apply`. This decouples your final output structure from your messy input structure.

### 2. `let` is Your Most Valuable Tool

Proper use of `let` is the key to writing clean and efficient scripts.
*   **DRY (Don't Repeat Yourself):** If you use any expression more than once, bind it to a variable with `let`.
*   **Readability:** Use `let` to give descriptive names to complex, nested expressions. A variable named `active_premium_users` is much clearer than a multi-line `filter` expression.
*   **Performance:** Binding a value with `let` ensures it is evaluated only once. This is the single most important optimization technique in Computo.

### 3. Filter Early, Map Late

When building an array processing pipeline, the order of operations is critical for performance.
*   **Always `filter` first.** Reduce the size of your dataset at the earliest possible moment. There is no reason to `map` over and transform items that you are just going to discard.
*   Perform your `map` operations on the smallest possible array. This minimizes processing time and memory used for temporary objects.

### 4. Be Defensive About Input

Never assume your input data will be perfect.
*   **Guard your `get` calls.** Before accessing a nested value like `"/user/profile/name"`, first check if the parent (`"/user/profile"`) exists and is truthy using an `if` statement.
*   Provide sensible defaults in your `else` branches to handle cases of missing or `null` data. This makes your transformations more resilient and prevents unexpected failures.

### 5. Compose, Don't Build Monoliths

Computo's power comes from composing simple, single-purpose operators.
*   **Embrace the Pipeline:** Think of your transformation as a series of small steps (e.g., filter -> map -> reduce). This is easier to read, debug, and reason about than a single, massive, deeply nested expression.
*   **Recognize Patterns:** Look for opportunities to use the patterns we've discussed:
    *   **Enrichment:** Adding new fields to an object with `merge`.
    *   **Forking:** Creating multiple outputs from a single source.
    *   **Aggregation:** Summarizing a list into a single report object.

### 6. Know When to Use Each Tool

Choosing the right operator or pattern for the job is a sign of mastery.

| If you need to... | Your first thought should be... |
| :--- | :--- |
| Create a new object from pieces | `obj` |
| "Fill in the blanks" of a structure | `permuto.apply` |
| Make a decision | `if` |
| Transform every item in a list | `map` |
| Select a subset of items from a list | `filter` |
| Combine a list into a single value | `reduce` |
| Reuse a value or improve readability | `let` |
| Combine two or more objects | `merge` |

### A Final Thought

The goal of Computo and Permuto is to move complex transformation logic out of your imperative application code and into a declarative, testable, and safe data format. By treating your transformations as data, you gain clarity and flexibility.

You are now fully equipped to apply these principles to your own projects. Happy transforming
