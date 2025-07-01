## **Chapter 2: Setting Up Your Environment**

### Prerequisites

You will need a C++17 compatible compiler, CMake, and Git. The development headers for the `nlohmann/json` library are also required.

- **Compiler:** GCC, Clang, or MSVC.
- **CMake:** Version 3.15 or later.
- **Git:** For cloning the repositories.
- **Dependencies:** `nlohmann/json` development files.

On a Debian/Ubuntu-based system, you can install the necessary dependencies with:

```bash
sudo apt-get update
sudo apt-get install build-essential cmake git nlohmann-json3-dev
```


### Step 1: Build and Install Permuto

Computo uses Permuto for its powerful templating capabilities, so we must install it first.

**1a. Clone the Permuto Repository**
```bash
git clone https://github.com/HarryPehkonen/Permuto.git
cd Permuto
```

**1b. Configure and Build**
We'll create a `Release` build for optimal performance.

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```
This will compile the Permuto library and its own CLI tool.

**1c. Install Permuto**
Now, install the library to a standard system location (typically `/usr/local/lib` and `/usr/local/include`). This step makes it discoverable by other projects, like Computo.

```bash
# From within the 'Permuto' directory
sudo cmake --install build
```
With Permuto installed, your system is now ready to build Computo.


### Step 2: Build Computo

Now we'll repeat a similar process for the `computo` project.

**2a. Clone the Computo Repository**
If you are still in the `Permuto` directory, navigate out of it first (`cd ..`).

```bash
git clone https://github.com/HarryPehkonen/Computo.git
cd Computo
```

**2b. Configure and Build**
CMake will now automatically find the Permuto library and headers you installed in the previous step.

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```
This command compiles the Computo library and the `computo` CLI tool. The final executable will be placed in the `build/` directory.

**2c. Install Computo**
For convenience, install the `computo` CLI tool to a standard system location so you can run it from anywhere without specifying the full path.

```bash
# From within the 'Computo' directory
sudo cmake --install build
```

Alternatively, for a stripped (smaller) binary:
```bash
sudo cmake --install build --strip
```

This installs the `computo` executable to `/usr/local/bin` (or your system's standard binary location), making it available system-wide.


### Step 3: Verify the Installation

You can verify that everything works by running the CLI tool or its test suite.

**To check the CLI:**
If you installed computo system-wide, you can now run it from anywhere. Try running it with no arguments to see the usage message.

If you haven't installed it yet, you can still test it from the build directory.

**To run the test suite:**
The project includes a comprehensive set of tests. Running them confirms that Computo, Permuto, and all operators are working correctly together on your system.

```bash
# From within the 'Computo' directory
cd build
ctest --verbose
```
You should see output indicating that all tests have passed.


### Your Workspace

You are now ready to start writing transformations. Your typical workflow will involve:

1. Creating a `script.json` file containing your Computo logic.
2. Creating an `input.json` file with the data you want to transform.
3. Running the transformation from anywhere on your system (assuming you installed computo).

In the next chapter, we will write our first Computo script and explore its fundamental concepts.


## 💻 Hands-On Examples

These examples demonstrate the debugging concepts covered in this chapter. Each example includes the complete script, expected output, and instructions for running it yourself.

### 🔧 Help Command

**Purpose**: Display help information to verify CLI is working

**Computo Script**:
```json
[
  "obj",
  [
    "message",
    "Hello World"
  ]
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch02_setting_up_your_environment/general/help_command/

# Run the example
computo --help script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
{
  "message": "Hello World"
}
```

**💡 What to Learn**: This example tests basic CLI functionality by showing help output

**🛠️ CLI Flags Used**:
- `--help`: --help

**📁 Download**:
- [📂 This example's files](code/ch02_setting_up_your_environment/general/help_command/)
- [📦 Chapter 2 examples](code/ch02_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---

### 🔧 Version Check

**Purpose**: Check Computo version to verify installation

**Computo Script**:
```json
[
  "obj",
  [
    "status",
    "installed"
  ]
]
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch02_setting_up_your_environment/general/version_check/

# Run the example
computo --version script.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
{
  "status": "installed"
}
```

**💡 What to Learn**: Verifies that computo command is available and shows version

**🛠️ CLI Flags Used**:
- `--version`: --version

**📁 Download**:
- [📂 This example's files](code/ch02_setting_up_your_environment/general/version_check/)
- [📦 Chapter 2 examples](code/ch02_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---

### 🔧 Basic Usage

**Purpose**: Basic script execution to verify end-to-end functionality

**Computo Script**:
```json
[
  "obj",
  [
    "result",
    "success"
  ],
  [
    "timestamp",
    [
      "get",
      [
        "$input"
      ],
      "/when"
    ]
  ]
]
```

**Input Data** (`input.json`):
```json
{
  "when": "2024-01-01"
}
```

**How to Run**:
```bash
# Navigate to the example directory
cd code/ch02_setting_up_your_environment/general/basic_usage/

# Run the example
computo --pretty=2 script.json input.json

# Or use the provided script
./run.sh    # Linux/Mac
run.bat     # Windows
```

**Expected Output**:
```json
"success"
```

**💡 What to Learn**: Tests basic script execution with pretty-printed output

**🛠️ CLI Flags Used**:
- `--pretty=2`: Formats output with proper indentation for readability

**📁 Download**:
- [📂 This example's files](code/ch02_setting_up_your_environment/general/basic_usage/)
- [📦 Chapter 2 examples](code/ch02_examples.zip)
- [📚 All book examples](download_all_examples.zip)

---
