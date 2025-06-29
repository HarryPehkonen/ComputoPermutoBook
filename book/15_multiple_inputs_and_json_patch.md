## **Chapter 15: Multiple Input Processing and JSON Patch Operations**

In this chapter, we'll explore Computo's advanced capabilities for working with multiple input documents and performing standardized JSON diff/patch operations. These features enable sophisticated data comparison, versioning, and multi-document transformations while maintaining RFC 6902 compliance.

### The `$inputs` System Variable: Working with Multiple Documents

Up until now, we've been working with single input documents using the `$input` variable. Computo now supports processing multiple input files simultaneously through the `$inputs` system variable.

#### Basic Multiple Input Usage

The `$inputs` variable returns an array containing all input documents provided on the command line:

```bash
# Single input (traditional)
computo script.json input1.json

# Multiple inputs (new capability)
computo script.json input1.json input2.json input3.json
```

```json
// Access all inputs as an array
["$inputs"]

// Access specific inputs by index
["get", ["$inputs"], "/0"]  // First input
["get", ["$inputs"], "/1"]  // Second input
["get", ["$inputs"], "/2"]  // Third input
```

#### Backward Compatibility

The familiar `$input` variable remains fully supported and is equivalent to accessing the first input:

```json
// These are equivalent:
["$input"]
["get", ["$inputs"], "/0"]
```

### Practical Multiple Input Examples

#### Example 1: Merging User Profiles

Let's say you have user data from two different systems that need to be merged:

**profile1.json:**
```json
{
  "id": "user123",
  "name": "Alice Johnson",
  "last_seen": "2024-01-15T10:30:00Z"
}
```

**profile2.json:**
```json
{
  "id": "user123",
  "email": "alice@example.com",
  "preferences": {
    "theme": "dark",
    "notifications": true
  }
}
```

**merge_profiles.json:**
```json
["let", [
    ["profile1", ["get", ["$inputs"], "/0"]],
    ["profile2", ["get", ["$inputs"], "/1"]]
  ],
  ["obj",
    ["user_id", ["get", ["$", "/profile1"], "/id"]],
    ["name", ["get", ["$", "/profile1"], "/name"]],
    ["email", ["get", ["$", "/profile2"], "/email"]],
    ["preferences", ["get", ["$", "/profile2"], "/preferences"]],
    ["last_seen", ["get", ["$", "/profile1"], "/last_seen"]]
  ]
]
```

**Usage:**
```bash
computo --pretty=2 merge_profiles.json profile1.json profile2.json
```

**Output:**
```json
{
  "user_id": "user123",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "preferences": {
    "theme": "dark",
    "notifications": true
  },
  "last_seen": "2024-01-15T10:30:00Z"
}
```

#### Example 2: Cross-Document Validation

Check if documents are consistent across different sources:

**validate_consistency.json:**
```json
["let", [
    ["doc1", ["get", ["$inputs"], "/0"]],
    ["doc2", ["get", ["$inputs"], "/1"]],
    ["user_id_match", ["==", 
      ["get", ["$", "/doc1"], "/id"],
      ["get", ["$", "/doc2"], "/id"]
    ]]
  ],
  ["obj",
    ["documents_consistent", ["$", "/user_id_match"]],
    ["doc1_id", ["get", ["$", "/doc1"], "/id"]],
    ["doc2_id", ["get", ["$", "/doc2"], "/id"]],
    ["total_inputs", ["count", ["$inputs"]]]
  ]
]
```

### JSON Patch Operations: Diff and Patch

Computo implements RFC 6902 JSON Patch standard, enabling precise document comparison and modification through standardized operations.

#### The `diff` Operator

Generates a JSON Patch array that describes the differences between two documents:

```json
["diff", <original_document>, <modified_document>]
```

**Example:**
```json
["diff", 
  {"status": "active", "id": 123},
  {"status": "archived", "id": 123}
]
```

**Output:**
```json
[{"op": "replace", "path": "/status", "value": "archived"}]
```

#### The `patch` Operator

Applies a JSON Patch array to a document:

```json
["patch", <document_to_modify>, <patch_array>]
```

**Example:**
```json
["patch",
  {"status": "active", "id": 123},
  [{"op": "replace", "path": "/status", "value": "archived"}]
]
```

**Output:**
```json
{"status": "archived", "id": 123}
```

### Complete Diff/Patch Workflow Example

Let's walk through a complete workflow that demonstrates document versioning and change management.

#### Step 1: Create a Transformation Script

**archive_user.json:**
```json
["obj",
  ["id", ["get", ["$input"], "/id"]],
  ["name", ["get", ["$input"], "/name"]],
  ["status", "archived"],
  ["archived_at", "2024-01-15T12:00:00Z"]
]
```

#### Step 2: Generate a Patch Using CLI

**original_user.json:**
```json
{
  "id": 123,
  "name": "Alice",
  "status": "active"
}
```

**Generate the patch:**
```bash
computo --diff archive_user.json original_user.json > archive_patch.json
```

**archive_patch.json (generated):**
```json
[
  {"op": "replace", "path": "/status", "value": "archived"},
  {"op": "add", "path": "/archived_at", "value": "2024-01-15T12:00:00Z"}
]
```

#### Step 3: Create a Reusable Patch Application Script

**apply_patch.json:**
```json
["patch",
  ["get", ["$inputs"], "/0"],
  ["get", ["$inputs"], "/1"]
]
```

#### Step 4: Apply the Patch

```bash
computo --pretty=2 apply_patch.json original_user.json archive_patch.json
```

**Output:**
```json
{
  "id": 123,
  "name": "Alice",
  "status": "archived",
  "archived_at": "2024-01-15T12:00:00Z"
}
```

### Advanced Multi-Document Processing Patterns

#### Pattern 1: Document Synchronization

Compare configurations between environments and generate sync patches:

**sync_configs.json:**
```json
["let", [
    ["prod_config", ["get", ["$inputs"], "/0"]],
    ["staging_config", ["get", ["$inputs"], "/1"]],
    ["sync_patch", ["diff", ["$", "/prod_config"], ["$", "/staging_config"]]]
  ],
  ["obj",
    ["requires_sync", [">", ["count", ["$", "/sync_patch"]], 0]],
    ["patch_operations", ["$", "/sync_patch"]],
    ["staging_after_sync", ["if",
      ["$", "/requires_sync"],
      ["patch", ["$", "/staging_config"], ["$", "/sync_patch"]],
      ["$", "/staging_config"]
    ]]
  ]
]
```

#### Pattern 2: Version Rollback Generation

Create rollback patches by reversing the diff direction:

**generate_rollback.json:**
```json
// Generate rollback patch (reverse diff)
["diff",
  ["get", ["$inputs"], "/1"],  // new version
  ["get", ["$inputs"], "/0"]   // original version
]
// This creates a patch that rolls back from new to original
```

#### Pattern 3: Multi-Source Data Aggregation

Combine data from multiple APIs or databases:

**aggregate_user_data.json:**
```json
["let", [
    ["profile_service", ["get", ["$inputs"], "/0"]],
    ["settings_service", ["get", ["$inputs"], "/1"]],
    ["activity_service", ["get", ["$inputs"], "/2"]]
  ],
  ["obj",
    ["user_id", ["get", ["$", "/profile_service"], "/id"]],
    ["basic_info", ["obj",
      ["name", ["get", ["$", "/profile_service"], "/name"]],
      ["email", ["get", ["$", "/profile_service"], "/email"]]
    ]],
    ["preferences", ["get", ["$", "/settings_service"], "/preferences"]],
    ["recent_activity", ["get", ["$", "/activity_service"], "/last_actions"]],
    ["last_updated", ["get", ["$", "/activity_service"], "/timestamp"]]
  ]
]
```

### Error Handling for Patch Operations

When working with patch operations, be aware of potential failures:

#### Common Patch Failures

1. **Invalid patch format** - Patch must be a valid JSON array
2. **Failed test operations** - `test` operations that don't match expected values
3. **Invalid paths** - Attempting to modify non-existent paths
4. **Malformed operations** - Invalid operation types

#### Safe Patch Application Pattern

Use conditional logic to handle potential patch failures gracefully:

**safe_patch_apply.json:**
```json
["let", [
    ["document", ["get", ["$inputs"], "/0"]],
    ["patch_ops", ["get", ["$inputs"], "/1"]],
    ["patch_count", ["count", ["$", "/patch_ops"]]]
  ],
  ["obj",
    ["original_document", ["$", "/document"]],
    ["patch_operations", ["$", "/patch_ops"]],
    ["patch_safe", ["==", ["$", "/patch_count"], 1]],
    ["result", ["if",
      ["$", "/patch_safe"],
      ["patch", ["$", "/document"], ["$", "/patch_ops"]],
      ["$", "/document"]
    ]]
  ]
]
```

### CLI Features for Diff/Patch Operations

#### The `--diff` Flag

Generate patches directly from transformations without modifying your scripts:

```bash
# Traditional transformation
computo transform.json input.json

# Generate patch from same transformation
computo --diff transform.json input.json
```

This is particularly useful for:
- **Version control integration** - Generate patches for change tracking
- **Automated deployment** - Create configuration update patches
- **Data migration planning** - Preview changes before applying them

#### Combining with Multiple Inputs

Remember that `--diff` only works with a single input file:

```bash
# Valid: Single input with --diff
computo --diff script.json input.json

# Invalid: Multiple inputs with --diff
computo --diff script.json input1.json input2.json
```

## Functional List Processing with car and cdr

Computo includes functional programming operators `car` and `cdr` inspired by Lisp, which provide elegant ways to work with arrays and multiple inputs.

### Understanding car and cdr

```json
// car: Get the first element
["car", {"array": [1, 2, 3, 4]}]
// Result: 1

// cdr: Get everything except the first element
["cdr", {"array": [1, 2, 3, 4]}]
// Result: [2, 3, 4]

// Composition: Get the second element
["car", ["cdr", {"array": [1, 2, 3, 4]}]]
// Result: 2
```

### Functional Multiple Input Processing

The `car` and `cdr` operators are particularly powerful for processing multiple inputs in a functional style:

#### Example: Applying Multiple Patches

**Traditional approach:**
```json
["let", [
    ["initial", ["get", ["$inputs"], "/0"]],
    ["patch1", ["get", ["$inputs"], "/1"]],
    ["patch2", ["get", ["$inputs"], "/2"]]
  ],
  ["patch", ["patch", ["$", "/initial"], ["$", "/patch1"]], ["$", "/patch2"]]
]
```

**Functional approach with car/cdr:**
```json
["reduce", 
  ["cdr", ["$inputs"]],                    // All patches (skip first input)
  ["lambda", ["state", "patch"],
    ["patch", ["$", "/state"], ["$", "/patch"]]
  ],
  ["car", ["$inputs"]]                     // Initial state (first input)
]
```

**Benefits of the functional approach:**
- Works with any number of patches (not just 2)
- More readable and declarative
- Follows functional programming principles
- Easier to test and reason about

#### Example: Processing Conversation Updates

```json
// Process conversation updates using functional list operations
["let", [
    ["initial_conversation", ["car", ["$inputs"]]],     // First input
    ["all_patches", ["cdr", ["$inputs"]]],              // Remaining inputs
    ["final_state", ["reduce",
      ["$", "/all_patches"],
      ["lambda", ["conversation", "patch"],
        ["patch", ["$", "/conversation"], ["$", "/patch"]]
      ],
      ["$", "/initial_conversation"]
    ]],
    ["patch_count", ["count", ["$", "/all_patches"]]]
  ],
  ["obj",
    ["conversation_id", ["get", ["$", "/final_state"], "/id"]],
    ["message_count", ["count", ["get", ["$", "/final_state"], "/messages"]]],
    ["patches_applied", ["$", "/patch_count"]],
    ["final_conversation", ["$", "/final_state"]]
  ]
]
```

**Usage:**
```bash
computo --pretty=2 conversation_processor.json initial_conversation.json patch1.json patch2.json patch3.json
```

## Advanced List Building and Manipulation Operations

Beyond basic list processing, Computo provides powerful operators for constructing and manipulating arrays in sophisticated ways. These operations complement the functional `car` and `cdr` operators.

### The `cons` Operator: List Building

The `cons` operator prepends an item to the beginning of an array, following functional programming conventions:

```json
["cons", <item>, <array>]
```

**Basic usage:**
```json
["cons", "first", {"array": [2, 3, 4]}]
// Result: ["first", 2, 3, 4]
```

**Building lists incrementally:**
```json
// Start with empty array and build a list
["cons", 1, 
  ["cons", 2, 
    ["cons", 3, {"array": []}]
  ]
]
// Result: [1, 2, 3]
```

**Practical example - Adding metadata to processing results:**
```json
["let", [
    ["processing_results", ["map", 
      ["get", ["$input"], "/user_data"],
      ["lambda", ["user"], ["obj", 
        ["id", ["get", ["$", "/user"], "/id"]], 
        ["processed", true]
      ]]
    ]],
    ["timestamp", "2024-01-15T12:00:00Z"]
  ],
  ["cons", 
    ["obj", ["processing_metadata", ["$", "/timestamp"]]],
    ["$", "/processing_results"]
  ]
]
```

### The `append` Operator: Array Concatenation

The `append` operator concatenates multiple arrays into a single array:

```json
["append", <array1>, <array2>, <array3>, ...]
```

**Basic concatenation:**
```json
["append", 
  {"array": [1, 2]}, 
  {"array": [3, 4]}, 
  {"array": [5]}
]
// Result: [1, 2, 3, 4, 5]
```

**Combining data from multiple sources:**
```json
["let", [
    ["primary_users", ["get", ["$inputs"], "/0/users"]],
    ["backup_users", ["get", ["$inputs"], "/1/users"]],
    ["temp_users", ["get", ["$inputs"], "/2/users"]]
  ],
  ["obj",
    ["all_users", ["append", 
      ["$", "/primary_users"],
      ["$", "/backup_users"], 
      ["$", "/temp_users"]
    ]],
    ["total_count", ["count", ["append",
      ["$", "/primary_users"],
      ["$", "/backup_users"],
      ["$", "/temp_users"]
    ]]]
  ]
]
```

**Real-world example - Aggregating log entries:**
```json
// Combine log entries from multiple services
["let", [
    ["web_logs", ["get", ["$inputs"], "/0/entries"]],
    ["api_logs", ["get", ["$inputs"], "/1/entries"]],
    ["db_logs", ["get", ["$inputs"], "/2/entries"]]
  ],
  ["obj",
    ["combined_logs", ["append", 
      ["$", "/web_logs"], 
      ["$", "/api_logs"], 
      ["$", "/db_logs"]
    ]],
    ["log_sources", {"array": ["web", "api", "database"]}],
    ["total_entries", ["count", ["append",
      ["$", "/web_logs"],
      ["$", "/api_logs"], 
      ["$", "/db_logs"]
    ]]]
  ]
]
```

### The `chunk` Operator: Batch Processing

The `chunk` operator splits an array into smaller arrays of a specified size, perfect for batch processing:

```json
["chunk", <array>, <size>]
```

**Basic chunking:**
```json
["chunk", {"array": [1, 2, 3, 4, 5, 6, 7]}, 3]
// Result: [[1, 2, 3], [4, 5, 6], [7]]
```

**Processing data in batches:**
```json
["let", [
    ["all_users", ["get", ["$input"], "/users"]],
    ["batch_size", 50],
    ["user_batches", ["chunk", ["$", "/all_users"], ["$", "/batch_size"]]]
  ],
  ["obj",
    ["total_users", ["count", ["$", "/all_users"]]],
    ["batch_count", ["count", ["$", "/user_batches"]]],
    ["batch_size", ["$", "/batch_size"]],
    ["batches", ["$", "/user_batches"]]
  ]
]
```

**Real-world example - Email campaign processing:**
```json
// Prepare email lists for batch sending
["let", [
    ["subscriber_list", ["get", ["$input"], "/subscribers"]],
    ["batch_size", 100],
    ["email_batches", ["chunk", ["$", "/subscriber_list"], ["$", "/batch_size"]]]
  ],
  ["obj",
    ["campaign_id", ["get", ["$input"], "/campaign_id"]],
    ["total_subscribers", ["count", ["$", "/subscriber_list"]]],
    ["email_batches", ["map", 
      ["$", "/email_batches"],
      ["lambda", ["batch"], ["obj",
        ["batch_size", ["count", ["$", "/batch"]]],
        ["recipients", ["$", "/batch"]]
      ]]
    ]],
    ["estimated_send_time_minutes", ["/", 
      ["count", ["$", "/email_batches"]], 
      2
    ]]
  ]
]
```

### The `partition` Operator: Conditional Splitting

The `partition` operator splits an array into two groups based on a predicate function:

```json
["partition", <array>, <lambda_predicate>]
```

**Returns:** `[<truthy_items>, <falsy_items>]`

**Basic partitioning:**
```json
["partition", 
  {"array": [1, 2, 3, 4, 5, 6]},
  ["lambda", ["x"], [">", ["$", "/x"], 3]]
]
// Result: [[4, 5, 6], [1, 2, 3]]
```

**Separating valid and invalid records:**
```json
["let", [
    ["user_records", ["get", ["$input"], "/users"]],
    ["partitioned", ["partition", 
      ["$", "/user_records"],
      ["lambda", ["user"], ["&&",
        ["!=", ["get", ["$", "/user"], "/email"], null],
        ["!=", ["get", ["$", "/user"], "/name"], ""]
      ]]
    ]]
  ],
  ["obj",
    ["valid_users", ["car", ["$", "/partitioned"]]],
    ["invalid_users", ["car", ["cdr", ["$", "/partitioned"]]]],
    ["valid_count", ["count", ["car", ["$", "/partitioned"]]]],
    ["invalid_count", ["count", ["car", ["cdr", ["$", "/partitioned"]]]]],
    ["validation_summary", ["obj",
      ["total_processed", ["count", ["$", "/user_records"]]],
      ["pass_rate", ["/", 
        ["count", ["car", ["$", "/partitioned"]]], 
        ["count", ["$", "/user_records"]]
      ]]
    ]]
  ]
]
```

**Real-world example - Order processing:**
```json
// Separate urgent and standard orders for different processing queues
["let", [
    ["all_orders", ["get", ["$input"], "/orders"]],
    ["partitioned_orders", ["partition",
      ["$", "/all_orders"],
      ["lambda", ["order"], ["||",
        ["==", ["get", ["$", "/order"], "/priority"], "urgent"],
        [">", ["get", ["$", "/order"], "/amount"], 1000]
      ]]
    ]]
  ],
  ["obj",
    ["urgent_orders", ["car", ["$", "/partitioned_orders"]]],
    ["standard_orders", ["car", ["cdr", ["$", "/partitioned_orders"]]]],
    ["processing_queues", ["obj",
      ["urgent_queue", ["obj",
        ["orders", ["car", ["$", "/partitioned_orders"]]],
        ["count", ["count", ["car", ["$", "/partitioned_orders"]]]],
        ["estimated_processing_hours", 2]
      ]],
      ["standard_queue", ["obj",
        ["orders", ["car", ["cdr", ["$", "/partitioned_orders"]]]],
        ["count", ["count", ["car", ["cdr", ["$", "/partitioned_orders"]]]]],
        ["estimated_processing_hours", 24]
      ]]
    ]]
  ]
]
```

### Combining List Operations for Complex Processing

These operators work beautifully together for sophisticated data processing workflows:

**Example: Processing survey responses in batches by category:**
```json
["let", [
    ["all_responses", ["get", ["$input"], "/survey_responses"]],
    // First partition by satisfaction level
    ["satisfaction_split", ["partition",
      ["$", "/all_responses"],
      ["lambda", ["response"], [">", ["get", ["$", "/response"], "/satisfaction"], 7]]
    ]],
    ["positive_responses", ["car", ["$", "/satisfaction_split"]]],
    ["negative_responses", ["car", ["cdr", ["$", "/satisfaction_split"]]]],
    // Then chunk positive responses for follow-up campaigns
    ["positive_batches", ["chunk", ["$", "/positive_responses"], 25]],
    // And chunk negative responses for support outreach
    ["negative_batches", ["chunk", ["$", "/negative_responses"], 10]]
  ],
  ["obj",
    ["processing_summary", ["obj",
      ["total_responses", ["count", ["$", "/all_responses"]]],
      ["positive_count", ["count", ["$", "/positive_responses"]]],
      ["negative_count", ["count", ["$", "/negative_responses"]]]
    ]],
    ["follow_up_campaigns", ["map",
      ["$", "/positive_batches"],
      ["lambda", ["batch"], ["obj",
        ["type", "testimonial_request"],
        ["recipients", ["$", "/batch"]],
        ["batch_size", ["count", ["$", "/batch"]]]
      ]]
    ]],
    ["support_outreach", ["map",
      ["$", "/negative_batches"],
      ["lambda", ["batch"], ["obj",
        ["type", "customer_support"],
        ["priority", "high"],
        ["recipients", ["$", "/batch"]],
        ["batch_size", ["count", ["$", "/batch"]]]
      ]]
    ]]
  ]
]
```

### Best Practices for Multiple Input Processing

1. **Use descriptive variable names** when working with `let` bindings
2. **Validate input count** using `["count", ["$inputs"]]` when expected
3. **Handle missing inputs gracefully** with conditional logic
4. **Document input order requirements** in your scripts
5. **Use patch operations for incremental updates** rather than full replacements
6. **Consider car/cdr for functional processing** when dealing with variable numbers of inputs
7. **Use car/cdr with reduce** for applying operations across multiple inputs
8. **Use cons for building lists incrementally** rather than complex array construction
9. **Use append for combining multiple data sources** efficiently
10. **Use chunk for batch processing** large datasets
11. **Use partition for conditional data splitting** instead of multiple filter operations

### Chapter Summary

In this chapter, you learned:

- How to process multiple input documents using the `$inputs` system variable
- The difference between `$input` (first document) and `$inputs` (all documents)
- How to generate standardized JSON patches using the `diff` operator
- How to apply patches using the `patch` operator  
- **Functional list processing** with `car` and `cdr` operators for elegant array manipulation
- **Advanced list building** with `cons` for prepending items to arrays
- **Array concatenation** with `append` for combining multiple data sources
- **Batch processing** with `chunk` for splitting arrays into manageable sizes
- **Conditional splitting** with `partition` for separating data based on predicates
- **Functional patterns** for processing variable numbers of inputs
- Complete workflows for document versioning and change management
- Advanced patterns for multi-document processing
- Error handling strategies for patch operations
- CLI features for streamlined diff/patch workflows

These features enable Computo to handle complex scenarios involving document comparison, versioning, configuration management, and multi-source data processing while maintaining RFC 6902 compliance for interoperability with other JSON Patch tools.

In the next chapter, we'll explore performance optimization techniques and best practices for production deployments.