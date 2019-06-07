# Graphs for multi-day cycling races.
This project makes it possible to scrape ProCyclingStats and uses and displays the obained data in a graph.
<br>
Like this:<br>
![Alt text](/tour-de-france2018.png?raw=true "graph")
To use:<br>
```
>python main.py <race-name> year
```
e.g.<br>
```
>python main.py tour-de-france 2018
```
```
>python main.py giro-d-italia 2017
```

To test:<br>
```
~\TdFgraph>python -m pytest tests
```
The program creates subfolders in the directory to store data.<br>
