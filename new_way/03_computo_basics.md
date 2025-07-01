## **Chapter 3: Computo Basics - Data and Logic**

Now that you have a working environment, it's time to start transforming JSON. In this chapter, we'll focus on the core of Computo: its syntax, its fundamental operators, and how it handles data.

At its heart, Computo treats **code as data**. Every Computo script is itself a valid JSON document. This is a powerful concept borrowed from Lisp-like languages that makes scripts easy to generate, store, and even manipulate programmatically.


### In This Chapter

You've learned the fundamental building blocks of Computo:
*   The **syntax** of operators `["op", ...]` and literal values.
*   **Mathematical operations** including the modulo operator `%` for remainders.
*   How to **create objects** using the `obj` operator with key-value pairs.
*   How to **create arrays** using the `{"array": [...]}` syntax.
*   How to access the entire input document with **`$input`**.
*   How to extract specific data with **`get`** and JSON Pointers.
*   How to create temporary variables with **`let`** and access them with **`$`**.

These fundamental operators give you the power to construct new JSON structures and perform data extraction and reshaping. In the next chapter, we'll switch gears and look at Permuto, the templating engine that complements Computo's logic.

