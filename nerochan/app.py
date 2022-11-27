#!/usr/bin/env python3

from nerochan import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
