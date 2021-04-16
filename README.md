# github-commits-visualizer
Command line tool to visualize commits of a repo for a given time

## Installing dependencies
```
pip install -r requirements.txt
```

You may need Python 3.8 to generate graph and latest browser to see the graph. Additionally to make it executable the following may be used.
```
chmod +x main.py
```

## Usage
To get help
```
./main.py
```
All the parameters are optional. By default It will show commits of `tiangolo/fastapi` for 30 days.

The following gets commits of `Abduvakilov/github-commits-visualizer` for 300 days
```
./main.py -r Abduvakilov/github-commits-visualizer -d 300
```
