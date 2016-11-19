# monero-ticker

A status bar Monero ticker for OS X.

# Development

monero-ticker was written using Python 2.7.10. You can run it with:

```
pip install -r requirements.txt
python main.py
```

To re-build the Mac application, run:

```
rm -rf dist/ build/
python setup.py py2app
```
