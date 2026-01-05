
Contributing Guidelines

We welcome contributions to the Medical MOF Prediction project!

How to Contribute

1. Reporting Issues

· Use GitHub Issues to report bugs or request features
· Include reproducible examples when reporting bugs
· Clearly describe the expected vs actual behavior

2. Code Contributions

1. Fork the repository
2. Create a feature branch: git checkout -b feature-name
3. Make your changes
4. Add tests for new functionality
5. Run existing tests: pytest
6. Ensure code style consistency
7. Submit a pull request

3. Code Style

· Follow PEP 8 guidelines
· Use meaningful variable names
· Add docstrings to functions and classes
· Write comprehensive comments for complex logic

4. Testing

· All new code must include tests
· Maintain >90% test coverage
· Use pytest for testing

5. Documentation

· Update relevant documentation
· Add examples for new features
· Update API reference if needed

Development Setup

```bash
# Clone and setup
git clone https://github.com/emerladcompass/medical-mof-prediction.git
cd medical-mof-prediction
pip install -e .[dev]

# Run tests
pytest

# Run linting
flake8 src/ tests/
```

Contact

For questions: emerladcompass@gmail.com
