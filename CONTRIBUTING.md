# Contributing to InkPen

First off, thanks for considering contributing to InkPen! It's people like you that make InkPen such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your OS version and Python version**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* End all files with a newline
* Avoid platform-dependent code

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
  * 🎨 `:art:` when improving the format/structure of the code
  * 🚀 `:rocket:` when improving performance
  * 📝 `:memo:` when writing docs
  * 🐛 `:bug:` when fixing a bug
  * ✨ `:sparkles:` when adding a new feature
  * ⚡ `:zap:` when removing code/files
  * 🔒 `:lock:` when dealing with security
  * ⬆️ `:arrow_up:` when upgrading dependencies
  * ⬇️ `:arrow_down:` when downgrading dependencies

### Python Styleguide

All Python code should adhere to PEP 8:

```python
# Good
def draw_stroke(self, painter: QPainter, stroke: Stroke):
    """Draw a stroke on the canvas."""
    if stroke.tool == Tool.PEN:
        painter.drawPath(stroke.get_path())

# Bad
def drawStroke(self,painter,stroke):
    if stroke.tool==Tool.PEN:
        painter.drawPath(stroke.getPath())
```

* Use 4 spaces for indentation
* Maximum line length is 100 characters
* Use type hints for function arguments and returns
* Write docstrings for all public functions and classes

### Documentation Styleguide

* Use [Markdown](https://daringfireball.net/projects/markdown) for documentation
* Reference method and class names in backticks: `` `some_method()` ``
* Reference external links with proper markdown syntax

## Development Setup

1. **Fork and clone the repository:**
```bash
git clone https://github.com/your-username/inkpen.git
cd inkpen
```

2. **Create a virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. **Install development dependencies:**
```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8
```

4. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

5. **Make your changes and test:**
```bash
# Run the application
python main.py

# Run code quality checks
black *.py
flake8 *.py
```

6. **Commit and push:**
```bash
git add .
git commit -m "🎨 Add your feature description"
git push origin feature/your-feature-name
```

7. **Open a Pull Request** on GitHub

## Testing

While InkPen doesn't currently have automated tests, please:

* Test your changes thoroughly on Windows 10/11
* Test with different screen resolutions
* Test with multiple monitors if possible
* Verify existing features still work

## Additional Notes

### Issue and Pull Request Labels

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good first issue` - Good for newcomers
* `help wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - This will not be worked on

## Versioning

InkPen follows semantic versioning (MAJOR.MINOR.PATCH) in the format `YYYY.MM.DD.HHMM` for automatic versioning via GitHub Actions.

---

Thank you for your contributions! 🎉
