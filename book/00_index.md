# **Computo/Permuto: A Practical Guide to JSON Transformations**

*A comprehensive guide to mastering JSON transformation with Computo and Permuto*

---

## **Table of Contents**

### **Part I: Foundations**

**[Chapter 1: Why JSON Transformation Matters](01_why_transformation_matters.md)**
- The problem space of JSON transformation
- Introduction to the Computo/Permuto solution
- Real-world use cases and scenarios

**[Chapter 2: Setting Up Your Environment](02_setting_up_environment.md)**
- Building Computo from source
- Verifying your installation
- Running your first transformation

**[Chapter 3: Computo Basics - Data and Logic](03_computo_basics.md)**
- Understanding the "code as data" philosophy
- Basic syntax and operators
- Your first transformations

**[Chapter 4: Permuto Basics - Template Processing](04_permuto_basics.md)**
- Declarative templating with `${path}` syntax
- Type preservation and string interpolation
- Integration with Computo scripts

### **Part II: Core Operations**

**[Chapter 5: Control Flow and Logic](05_control_flow.md)**
- Conditional expressions with `if`
- Comparison operators
- Building decision trees

**[Chapter 6: Working with Arrays](06_working_with_arrays.md)**
- Array literals and basic operations
- Introduction to functional programming concepts
- Lambda expressions

**[Chapter 7: Object Manipulation](07_object_manipulation.md)**
- Creating and merging objects
- JSON Pointer navigation
- Variable scoping with `let`

**[Chapter 8: Advanced Array Operations](08_advanced_array_ops.md)**
- Functional programming with `map`, `filter`, and `reduce`
- Complex data transformations
- Performance considerations

### **Part III: Advanced Techniques**

**[Chapter 9: Template-Driven Transformations](09_template_driven_transformations.md)**
- Combining Computo logic with Permuto templates
- Dynamic template generation
- Configuration management patterns

**[Chapter 10: Data Pipeline Patterns](10_data_pipeline_patterns.md)**
- Multi-step transformations
- Aggregation and summarization
- Validation and error handling

**[Chapter 11: Complex Real-World Examples](11_complex_real-world_examples.md)**
- API response transformation
- Configuration file generation
- Data migration scenarios

**[Chapter 12: Performance and Optimization](12_performance_and_optimization.md)**
- Understanding Computo's execution model
- Memory usage and large datasets
- Optimization strategies

### **Part IV: Production Usage**

**[Chapter 13: Error Handling and Debugging](13_error_handling_and_debugging.md)**
- Understanding exception types
- Debugging strategies
- Graceful error recovery

**[Chapter 14: Best Practices and Patterns](14_best_practices_and_patterns.md)**
- Code organization and reusability
- Testing transformation scripts
- Maintainable patterns

**[Chapter 15: Multiple Input Processing and JSON Patch Operations](15_multiple_inputs_and_json_patch.md)**
- Working with multiple input documents using `$inputs`
- RFC 6902 JSON Patch support with `diff` and `patch` operators
- Document versioning and change management
- Multi-document processing patterns

### **Appendices**

**[Appendix A: Complete Operator Reference](appendices/A_operator_reference.md)**
- Comprehensive reference for all 25 operators
- Syntax examples and use cases
- Quick lookup guide

---

## **Quick Navigation**

### **For Beginners**
Start with [Chapter 1](01_why_transformation_matters.md) to understand the motivation, then proceed through [Chapter 2](02_setting_up_environment.md) for setup and [Chapter 3](03_computo_basics.md) for fundamentals.

### **For Experienced Developers**
Skip directly to [Chapter 3](03_computo_basics.md) for syntax basics, then jump to specific topics of interest or the [Operator Reference](appendices/A_operator_reference.md) for quick lookup.

### **For Specific Use Cases**
- **API Integration**: [Chapter 11](11_complex_real-world_examples.md)
- **Configuration Management**: [Chapter 9](09_template_driven_transformations.md)
- **Data Pipelines**: [Chapter 10](10_data_pipeline_patterns.md)
- **Document Versioning**: [Chapter 15](15_multiple_inputs_and_json_patch.md)
- **Performance Tuning**: [Chapter 12](12_performance_and_optimization.md)

### **Reference Materials**
- **Complete Operator List**: [Appendix A](appendices/A_operator_reference.md)
- **Error Types**: [Chapter 13](13_error_handling_and_debugging.md)
- **Best Practices**: [Chapter 14](14_best_practices_and_patterns.md)

---

## **About This Guide**

This guide assumes you are an experienced developer familiar with JSON, functional programming concepts, and command-line tools. We focus on practical examples and real-world scenarios rather than theoretical explanations.

### **What You'll Learn**
- Master both Computo (programmatic logic) and Permuto (declarative templates)
- Build robust JSON transformation pipelines
- Handle complex multi-document processing scenarios
- Implement RFC 6902 JSON Patch workflows
- Apply best practices for production usage

### **Prerequisites**
- Familiarity with JSON syntax and structure
- Basic understanding of functional programming (map, filter, reduce)
- Command-line experience
- C++ build tools (for building from source)

---

*Ready to transform JSON like a pro? Let's begin with [Chapter 1: Why JSON Transformation Matters](01_why_transformation_matters.md).*