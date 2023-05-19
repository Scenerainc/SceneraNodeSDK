# Scenera Node SDK

Scenera Node SDK is a Python library for interacting with Scenera's Node API.

## Installation

You can install Scenera Node SDK from PyPI:

```bash
pip install scenera.node
```

Or you can get the dev version from TestPyPI:

```bash
pip install -i https://test.pypi.org/simple/ scenera.node
```

This package supports Python 3.6+.

## Usage

Here's a basic example of how to use Scenera Node SDK:

```python
from scenera_node_sdk import NodeClient

client = NodeClient(api_key="your-api-key")

# Get information about a node
node_info = client.get_node_info(node_id="your-node-id")
print(node_info)
```

## Features

- Feature 1
- Feature 2
- Feature 3
- ...

## Documentation

You can find the complete API documentation at (insert documentation URL).

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.

## Support

If you encounter any issues, please report them via the issue tracker on GitHub.

For more general questions or discussions, you can reach out to us at [dirk.meulenbelt@scenera.net](dirk.meulenbelt@scenera.net).
