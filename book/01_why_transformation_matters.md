# **Computo/Permuto: A Practical Guide to JSON Transformations**

## **Chapter 1: Why JSON Transformation Matters**

Welcome. If you're reading this, you're likely an experienced developer. You live and breathe APIs, configuration files, and data interchange. You know that JSON isn't just a data format; it's the lingua franca of the modern web. You also know that while creating and parsing JSON is a solved problem, **transforming it** can be surprisingly messy.

That's the gap this guide—and the Computo/Permuto toolkit—is designed to fill. We won't waste your time explaining what a JSON object is or how a `map` function works. Instead, we'll get straight to the point: giving you a powerful, safe, and elegant way to reshape JSON from one form to another.

### The Problem Space: The Daily Grind of Reshaping JSON

Think about the last time you had to manipulate a JSON structure. Did it feel like one of these scenarios?

*   **API Aggregation:** You're building a backend-for-frontend (BFF) and need to call three different microservices. Each returns a JSON object with a slightly different structure. Your job is to pick and choose fields from each, combine them into a single, clean JSON response, and send it to the client.

*   **Configuration Management:** You have a master configuration template for your application. You need to generate specific `config.json` files for your `development`, `staging`, and `production` environments, each with different database credentials, feature flags, and logging levels.

*   **Data Normalization:** You're ingesting data from a third-party API. The data is messy: some keys are camelCase while others are snake_case, numbers are sometimes strings, and optional fields are sometimes `null` and other times omitted entirely. You need to sanitize and normalize this data into a consistent format for your own systems.

*   **Dynamic Payloads:** You're integrating with multiple Large Language Model (LLM) providers. OpenAI wants a payload with a `messages` array, while Anthropic wants a single `prompt` string. You need to build these different JSON payloads from a single, canonical request object within your application.

Traditionally, you'd solve these problems by writing imperative code in your language of choice—Python, JavaScript, Go, C++. You'd loop through arrays, check for the existence of keys, and manually build new objects. It works, but it's often verbose, error-prone, and mixes transformation logic deep within your business logic.

### Introducing the Computo/Permuto Solution

Computo and Permuto offer a better way. They form a powerful, two-layer system designed specifically for JSON-to-JSON transformation, where each layer has a distinct responsibility.

1.  **Permuto: The Declarative Templating Engine**
    Think of Permuto as a smart, structure-aware "mail merge" for JSON. You provide it a template, and it fills in the blanks. It's for simple, declarative substitutions. If you just need to map values from a context object into a new structure, Permuto is your tool. It's fast, simple, and safe.

    *A quick taste:* `{"user_id": "${/user/id}"}`

2.  **Computo: The Programmatic Logic Engine**
    Think of Computo as a safe, sandboxed Lisp or spreadsheet formula engine that lives inside JSON. It provides the programmatic logic that simple templating lacks: conditionals (`if`), iteration (`map`, `filter`, `reduce`), calculations (`+`, `*`), and variable bindings (`let`).

    *A quick taste:* `["if", <condition>, <then_expr>, <else_expr>]`

### The "Aha!" Moment: Logic Driving Templates

The real power emerges when you combine them. You use Computo's logic to decide *how* and *if* to apply Permuto's templates.

Imagine our user summary problem again. If a user is active, we want to generate a full profile. If not, we want a simple error object.

*   **Computo's `if` operator** handles the conditional logic.
*   It checks a field, like `user.active`.
*   If `true`, it calls **Permuto** with a `user_profile_template.json` to generate the rich object.
*   If `false`, it constructs a simple `{"error": "User is inactive"}` object.

The script for this transformation is a clean piece of data (a JSON file) that you can store, version, and execute safely, without intermingling complex string manipulation or loops in your core application code.

### What's Ahead

In the following chapters, we will explore this toolkit from the ground up.

*   We'll start by **setting up your environment**.
*   Then, we'll master the fundamentals of **Computo and Permuto individually**.
*   Finally, we will combine them to build **sophisticated data pipelines** that solve real-world problems like the ones mentioned above.

By the end of this guide, you'll have a new, powerful tool in your arsenal for one of the most common tasks in modern software development. Let's get started.
