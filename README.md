1) If these commands don't work in Windows, create folders manually.
```mkdir data```
```mkdir static/audio```
2) Create a conda environment with Python 3.6 preferably (open ananconda bash in this directory if windows)

```conda create -n allennlp python=3.6 allennlp```

3) Activate the environment
```conda activate allennlp```

4) Install other requirements
```pip install -r requirements.txt```

```python app.py```
