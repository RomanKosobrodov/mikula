# Building and deploying

If your system is configured for multiple PyPI repositories and users include the valid name from `~/.pypirc`.

```bash
python -m build --wheel --sdist
twine upload dist/* --repository <repository-name>
```