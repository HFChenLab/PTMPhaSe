# PTMint
A website (PTMint) for **Post Translational Modification (PTM) associated with Protein-Protein Interactions** created by *Xiaokun Hong, Ningshan Li, Jiyang Lv*

Citation: Hong X, Li N, Lv J, Zhang Y, Li J*, Zhang J*, Chen HF*. PTMint database of experimentally verified PTM regulation on protein-protein interaction. Bioinformatics. 2023 Jan 1;39(1):btac823. doi: 10.1093/bioinformatics/btac823. PMID: 36548389; PMCID: PMC9848059.

## Set up environment

1. Install [Anaconda](https://www.anaconda.com/), and create a environment based on **Python 3.9.7**
2. Install Python packages (*latest version up to 2022-02-16*)
   * [Flask](https://palletsprojects.com/p/flask/): 2.0.3 (latest version in *conda* is 2.0.2)
   * [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.0.x/): 1.0.0
   * [WTForms](https://wtforms.readthedocs.io/en/3.0.x/): 3.0.1
   * [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/): 3.3.7.1
   * [Jinja2](https://palletsprojects.com/p/jinja/): 3.0.3
   * [pandas](https://pandas.pydata.org/): 1.4.1
   * [gunicorn](https://gunicorn.org/): 20.1.0plotnine
   * [plotnine](https://github.com/has2k1/plotnine.git): 0.8.0

```bash
conda install -c conda-forge -c anaconda Flask=2.0.2 Flask-WTF=1.0.0 WTForms=3.0.1 Flask-Bootstrap=3.3.7.1 Jinja2=3.0.3 pandas=1.4.1 gunicorn=20.1.0 plotnine=0.8.0
```

3. Other packages no need to install (*latest version up to 2022-02-16*; best to install them as network connection from China may fail)
   * [Bootstrap](https://getbootstrap.com/): v5.1.3
   * [jQuery](https://jquery.com/): v3.6.0
   * [jQuery UI](https://jqueryui.com/): v1.13.1
