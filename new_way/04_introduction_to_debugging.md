## **Chapter 4: Introduction to Debugging**

### Why Debugging Matters

As you start building more complex Computo transformations, you'll quickly want to "see inside" what's happening. Unlike traditional programming languages where you can add print statements, Computo scripts are pure JSON expressions. This is where Computo's powerful debugging features become essential.

Think of debugging not as something you do when things go wrong, but as a learning tool that helps you:

- **Understand execution flow** - See exactly how your script processes data
- **Verify your logic** - Confirm each step produces what you expect  
- **Learn performance characteristics** - Identify which operations are expensive
- **Build confidence** - Experiment with complex operations safely
- **Troubleshoot efficiently** - Quickly identify issues when they occur

Computo provides professional-grade debugging tools that make complex transformations transparent and understandable.


### Basic Execution Tracing

The most fundamental debugging tool is **execution tracing**. This shows you exactly which operations are being executed and in what order.

**Basic Usage:**
```bash
computo --trace script.json input.json
```

The trace output goes to stderr (error stream), while your JSON result still goes to stdout. This means you can see the debugging information while still capturing clean output.

**What You'll See:**
- Each operator call with its arguments
- The result of each operation
- Nested operation flow with indentation
- Variable bindings and lookups

This is invaluable when learning how `map`, `filter`, `reduce`, and other operations actually work under the hood.


### Performance Awareness

Even simple scripts can have performance implications. Computo's **profiling** helps you understand which operations are taking time.

**Basic Profiling:**
```bash
computo --profile script.json input.json
```

**What to Look For:**
- Operations that take significantly longer than others
- Repeated expensive operations that could be optimized
- Memory-intensive operations with large datasets

**Performance Tips:**
- `reduce` operations are generally faster than multiple `map` calls
- Avoid deeply nested operations when possible
- Consider the size of your datasets with operations like `filter` and `map`

You don't need to optimize everything, but understanding where time is spent helps you make informed decisions as your scripts grow in complexity.


### Reading Error Messages

Computo provides detailed error messages that pinpoint exactly where issues occur. Learning to read these messages efficiently will save you significant debugging time.

**Common Error Types:**
- **Path errors**: When JSON pointers don't exist (`/user/name` but `user` is null)
- **Type errors**: Wrong data types for operations (trying to add a string and number)
- **Operator errors**: Invalid arguments to operators
- **Structure errors**: Malformed JSON or incorrect operator syntax

**Error Message Components:**
- **Location**: Which part of your script caused the error
- **Context**: What data was being processed
- **Suggestion**: Often includes hints about what went wrong

The key is to read the full error message - Computo's errors are designed to be helpful, not cryptic.


### Variable Watching and Data Flow

One of the most powerful debugging techniques is watching how data flows through your transformations, especially with `let` expressions and complex nested operations.

**Variable Inspection:**
When using `let` bindings, you can see exactly what values are assigned to each variable and how they're used throughout the expression.

**Data Flow Tracing:**
- Watch how arrays are transformed step by step
- See intermediate results in complex calculations
- Understand how nested operations pass data between levels

**Best Practices:**
- Use meaningful variable names in `let` expressions
- Break complex operations into smaller, named steps
- Watch how data changes shape through transformations

This becomes especially valuable when working with real-world data that might have unexpected structure or missing fields.


### Output Formatting for Development

While debugging, readable output is crucial. Computo provides several formatting options to make development easier.

**Pretty Printing:**
```bash
computo --pretty=2 script.json input.json
```

The number after `--pretty` controls indentation depth. Use 2 or 4 for most development work.

**Combining Debugging Flags:**
```bash
# Trace execution with pretty output
computo --trace --pretty=2 script.json input.json

# Profile performance with readable results  
computo --profile --pretty=2 script.json input.json
```

**Development Workflow:**
1. Start with basic execution and pretty output
2. Add tracing when you need to understand flow
3. Add profiling when performance matters
4. Use plain output for production scripts

Remember: debugging flags are for development. Production scripts should typically run without them for best performance.


### Next Steps: Advanced Debugging

This chapter covered the essential debugging skills you'll use every day. As you progress through the book and tackle more complex transformations, you'll encounter advanced debugging techniques including:

- **Interactive debugging sessions** for step-through analysis
- **Conditional breakpoints** for specific scenarios  
- **Advanced performance optimization** strategies
- **Complex error diagnosis** for production systems
- **Debugging multi-input transformations** and pipelines

For now, practice using these basic debugging tools with the examples in this chapter. The more comfortable you become with tracing and profiling, the more confident you'll be tackling advanced Computo transformations.

**Key Takeaway:** Debugging isn't just for fixing problems - it's a learning tool that makes you a better Computo developer.


## 💻 Hands-On Examples

These examples demonstrate the debugging concepts covered in this chapter. Each example includes the complete script, expected output, and instructions for running it yourself.

### 🔧 Basic Tracing

**Purpose**: Basic execution tracing to see operation flow

**Computo Script**:
```json
[
  "let", 
  [
    ["x", 10],
    ["y", 32]
  ],
  ["+", ["$", "/x"], ["$", "/y"]]
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch04_introduction_to_debugging/general/basic_tracing/

# Run the example
computo --trace --pretty=2 script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
42
```

**💡 What to Learn**: Watch how let binding creates variables and how they're accessed

**🛠️ CLI Flags Used**:
- `--trace`: Shows execution flow and operation details
- `--pretty=2`: Formats output with proper indentation for readability

**📁 Download**:
- [📂 This example's files](code/ch04_introduction_to_debugging/general/basic_tracing/)
- [📦 Chapter 4 examples](code/ch04_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---

### 🔧 Array Operation Tracing

**Purpose**: Trace array operations to understand iteration

**Computo Script**:
```json
[
  "map",
  {"array": [1, 2, 3, 4]},
  ["lambda", ["x"], ["*", ["$", "/x"], 2]]
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch04_introduction_to_debugging/general/array_operation_tracing/

# Run the example
computo --trace script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
[
  2,
  4,
  6,
  8
]
```

**💡 What to Learn**: See how map processes each array element individually

**🛠️ CLI Flags Used**:
- `--trace`: Shows execution flow and operation details

**📁 Download**:
- [📂 This example's files](code/ch04_introduction_to_debugging/general/array_operation_tracing/)
- [📦 Chapter 4 examples](code/ch04_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---

### 🔧 Performance Profiling

**Purpose**: Basic performance profiling to identify slow operations

**Computo Script**:
```json
[
  "reduce",
  {"array": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
  ["lambda", ["acc", "x"], ["+", ["$", "/acc"], ["*", ["$", "/x"], ["$", "/x"]]]],
  0
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch04_introduction_to_debugging/general/performance_profiling/

# Run the example
computo --profile --pretty=2 script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
385
```

**💡 What to Learn**: See timing information for each operation

**🛠️ CLI Flags Used**:
- `--profile`: Displays timing information for performance analysis
- `--pretty=2`: Formats output with proper indentation for readability

**📁 Download**:
- [📂 This example's files](code/ch04_introduction_to_debugging/general/performance_profiling/)
- [📦 Chapter 4 examples](code/ch04_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---

### 🔧 Variable Watching

**Purpose**: Watch variable creation and usage in complex expressions

**Computo Script**:
```json
[
  "let",
  [
    ["numbers", {"array": [5, 10, 15]}],
    ["multiplier", 3]
  ],
  [
    "map",
    ["$", "/numbers"],
    ["lambda", ["n"], ["*", ["$", "/n"], ["$", "/multiplier"]]]
  ]
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch04_introduction_to_debugging/general/variable_watching/

# Run the example
computo --trace --pretty=2 script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
[
  15,
  30,
  45
]
```

**💡 What to Learn**: Watch how variables are bound and accessed in nested operations

**🛠️ CLI Flags Used**:
- `--trace`: Shows execution flow and operation details
- `--pretty=2`: Formats output with proper indentation for readability

**📁 Download**:
- [📂 This example's files](code/ch04_introduction_to_debugging/general/variable_watching/)
- [📦 Chapter 4 examples](code/ch04_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---

### 🔧 Error Demonstration

**Purpose**: Demonstrate clear error messages for common mistakes

**Computo Script**:
```json
[
  "obj",
  ["safe_value", ["+", 20, 22]],
  ["message", "This works fine"]
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch04_introduction_to_debugging/general/error_demonstration/

# Run the example
computo --pretty=2 script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
{
  "safe_value": 42,
  "message": "This works fine"
}
```

**💡 What to Learn**: Example of successful execution - compare with error cases you encounter

**🛠️ CLI Flags Used**:
- `--pretty=2`: Formats output with proper indentation for readability

**📁 Download**:
- [📂 This example's files](code/ch04_introduction_to_debugging/general/error_demonstration/)
- [📦 Chapter 4 examples](code/ch04_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---

### 🔧 Nested Operation Flow

**Purpose**: Trace complex nested operations to understand execution order

**Computo Script**:
```json
[
  "obj",
  ["total", [
    "reduce",
    ["filter", {"array": [1, 2, 3, 4, 5, 6]}, ["lambda", ["x"], [">", ["$", "/x"], 3]]],
    ["lambda", ["sum", "x"], ["+", ["$", "/sum"], ["$", "/x"]]],
    0
  ]],
  ["count", ["filter", {"array": [1, 2, 3, 4, 5, 6]}, ["lambda", ["x"], [">", ["$", "/x"], 3]]]]
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch04_introduction_to_debugging/general/nested_operation_flow/

# Run the example
computo --trace script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
{
  "total": 18,
  "count": 3
}
```

**💡 What to Learn**: See how nested filter and reduce operations execute step by step

**🛠️ CLI Flags Used**:
- `--trace`: Shows execution flow and operation details

**📁 Download**:
- [📂 This example's files](code/ch04_introduction_to_debugging/general/nested_operation_flow/)
- [📦 Chapter 4 examples](code/ch04_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---
