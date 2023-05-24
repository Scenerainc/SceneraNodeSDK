<div align="center">
    <img src="https://scenera.net/wp-content/uploads/2023/01/SMALL_SCENERA-1.png" alt="ScenerNodeSDK">
</div>

# Scenera Node SDK

Scenera Node SDK is a Python library intended to interact easily with the [SceneMark](https://docs.scenera.live/general#the-scenemark) and to build AI nodes easily according to the rules of the Scenera PaaS.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Example Node](#example-node)
- [Documentation](#documentation)
- [License](#license)
- [Support](#support)

## Installation

You can install Scenera Node SDK from PyPI:

```bash
pip install scenera.node
```

This package supports Python 3.6+.

## Usage

Here's a basic example of how to use Scenera Node SDK:

```python
import logging
from flask import Flask, request
from flask_cors import CORS
from scenera.node import SceneMark
from scenera.node.logger import configure_logger

## logger 
logger = logging.getLogger(__name__)
logger = configure_logger(logger, debug=True)

app = Flask(__name__)
CORS(app)

NODE_ID = "my_example_node"

@app.route(f'/{NODE_ID}/1.0', methods = ['POST'])
def node_endpoint():

    ## The first thing we do is load the request into the SceneMark object
    scenemark = SceneMark(
        request = request,
        node_id = NODE_ID,
        disable_linter = False
        )
        
    """
    Your node goes here
    """
   
    ## We automatically return the SceneMark back to the NodeSequencer
    scenemark.return_scenemark_to_ns()
    return "Success"
```

## Example Node

Coming soon.

## Documentation

You can find the complete API documentation at [our documentation website](https://docs.scenera.live/node-sdk).

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.

## Support

If you encounter any issues, please report them via the issue tracker on GitHub.

For more general questions or discussions, you can reach out to us at [dirk.meulenbelt@scenera.net](dirk.meulenbelt@scenera.net).
