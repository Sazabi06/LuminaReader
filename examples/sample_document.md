# LuminaReader Test Document

This is a comprehensive test document to demonstrate LuminaReader's capabilities.

---

## Table of Contents

1. [Typography](#typography)
2. [Code Blocks](#code-blocks)
3. [Mathematical Equations](#mathematical-equations)
4. [Tables](#tables)
5. [Lists](#lists)
6. [Blockquotes](#blockquotes)
7. [Images](#images)

---

## Typography

LuminaReader supports all standard Markdown formatting:

**Bold text** and *italic text* and ~~strikethrough~~

You can also use __underscores__ for emphasis.

### Headers

# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header

### Links

[Visit GitHub](https://github.com)

[Internal link to Typography](#typography)

### Horizontal Rules

---

***

---

## Code Blocks

### Inline Code

Use `print("Hello World")` for inline code.

### Python

```python
def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    fib_sequence = [0, 1]
    for i in range(2, n):
        next_val = fib_sequence[i-1] + fib_sequence[i-2]
        fib_sequence.append(next_val)
    
    return fib_sequence

# Example usage
print(fibonacci(10))
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <cmath>

class Point {
private:
    double x, y;
    
public:
    Point(double x_val, double y_val) : x(x_val), y(y_val) {}
    
    double distanceToOrigin() const {
        return std::sqrt(x*x + y*y);
    }
    
    void print() const {
        std::cout << "Point(" << x << ", " << y << ")" << std::endl;
    }
};

int main() {
    Point p(3.0, 4.0);
    p.print();
    std::cout << "Distance: " << p.distanceToOrigin() << std::endl;
    return 0;
}
```

### JavaScript

```javascript
// Async function example
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return processUserData(data);
    } catch (error) {
        console.error('Failed to fetch user:', error);
        throw error;
    }
}

const processUserData = (user) => ({
    ...user,
    fullName: `${user.firstName} ${user.lastName}`,
    isActive: user.lastLogin > Date.now() - 7 * 24 * 60 * 60 * 1000
});
```

### Bash

```bash
#!/bin/bash

# System information script
echo "=== System Information ==="
echo "Hostname: $(hostname)"
echo "OS: $(uname -o)"
echo "Kernel: $(uname -r)"
echo "Architecture: $(uname -m)"
echo ""
echo "=== Memory Usage ==="
free -h
echo ""
echo "=== Disk Usage ==="
df -h | grep -E '^/dev/'
```

---

## Mathematical Equations

LuminaReader uses MathJax for rendering LaTeX equations.

### Inline Math

The famous mass-energy equivalence: $E = mc^2$

The quadratic formula: $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

Euler's identity: $e^{i\pi} + 1 = 0$

### Block Equations

#### Maxwell's Equations

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0\mathbf{J} + \mu_0\varepsilon_0\frac{\partial \mathbf{E}}{\partial t}
\end{aligned}
$$

#### Schrödinger Equation

$$
i\hbar\frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat{H}\Psi(\mathbf{r},t)
$$

#### Fourier Transform

$$
F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt
$$

#### Gaussian Integral

$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

#### Matrix Example

$$
\mathbf{A} = \begin{bmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{bmatrix}
$$

#### Summation and Products

$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2} \quad \text{and} \quad \prod_{i=1}^{n} i = n!
$$

---

## Tables

### Simple Table

| Feature | Status | Priority |
|---------|--------|----------|
| Markdown Rendering | ✅ Complete | High |
| PDF Support | ✅ Complete | High |
| Math Equations | ✅ Complete | High |
| Syntax Highlighting | ✅ Complete | Medium |
| Dark Theme | ✅ Complete | Medium |
| Search | ✅ Complete | Medium |

### Aligned Table

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Row 1        |      Data      |         $1000 |
| Row 2        |      Data      |          $500 |
| Row 3        |      Data      |          $250 |

---

## Lists

### Unordered Lists

- First item
- Second item
  - Nested item 1
  - Nested item 2
    - Deeply nested item
- Third item

### Ordered Lists

1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step

### Task Lists

- [x] Implement frameless window
- [x] Add custom title bar
- [x] Support Markdown rendering
- [x] Support PDF rendering
- [x] Add math equation support
- [ ] Add print functionality
- [ ] Add export to HTML

### Mixed Lists

1. Programming Languages
   - Python
     - Easy to learn
     - Great for data science
   - JavaScript
     - Web development
     - Full-stack capabilities
   - C++
     - High performance
     - System programming

2. Frameworks
   - Qt/PySide6
   - React
   - Vue.js

---

## Blockquotes

> "The only way to do great work is to love what you do."
> 
> — Steve Jobs

> ### Note on Scientific Computing
> 
> Scientific computing requires both **accuracy** and **performance**.
> 
> Key principles:
> > 1. Validate your results
> > 2. Document your methods
> > 3. Share your code

---

## Images

Since this is a standalone document, image references would work like this:

```markdown
![Local Image](./assets/screenshot.png)
![External Image](https://example.com/image.png)
```

---

## Advanced Markdown

### Definition Lists

Term 1
: Definition 1

Term 2
: Definition 2a
: Definition 2b

### Footnotes

Here's a sentence with a footnote[^1].

[^1]: This is the footnote content.

### Strikethrough and Subscript/Superscript

~~Deleted text~~

H~2~O is water

x^2^ + y^2^ = r^2^

---

## Conclusion

This document demonstrates LuminaReader's comprehensive Markdown support including:

- ✅ Full typography control
- ✅ Syntax-highlighted code blocks
- ✅ Beautiful math rendering
- ✅ Flexible tables
- ✅ Nested lists
- ✅ Blockquotes and callouts

**Try dragging this file into LuminaReader to see it rendered!**

---

*Document version: 1.0.0*
*Last updated: 2024*
