# Solution EDA chalange

According to that all analysis were vizualaized with `Streamlit`, you need just build the Docker container and review this task in any browser as you want.


## Project tree

```
├── Dockerfile
├── README.md
├── requirements.txt
└── task_solution
    ├── MainPage.py
    ├── data_tools
    │   ├── __init__.py
    │   ├── charts_tools.py
    │   ├── data_prep.py
    │   ├── dictionaries.py
    │   └── model_tools.py
    └── pages
        ├── 1_DataPreProcessing.py
        ├── 2_EDA_YoY.py
        ├── 3_EDA_MoM.py
        ├── 4_Forecasting.py
        └── __init__.py
```

## How to run

1. Firstly you should build a container `docker build -t streamlit .`

2. After just run it `docker run -p 8501:8501 streamlit`

The port 8501 is a default streamlit port.

3. You will see the link after run command.

```
  You can now view your Streamlit app in your browser.

  URL: http://0.0.0.0:8501
```

That's it, then you can go page by page and review all my analysis.