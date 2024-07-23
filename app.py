# -*- coding: utf-8 -*-
"""
Created on July 2024

@author: Xiaokun Hong, Jiyang Lv
"""

'''
main program for hosting the website PTMPhaSe
'''


import json
import zipfile
import pandas as pd
import os
from wtforms.validators import DataRequired
from wtforms import SelectField, SubmitField, RadioField, StringField, BooleanField
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, send_from_directory, jsonify, make_response
COUNT = int(open('static/count.txt').read())
##################### 网页相关####################################################
# 载入main csv文件
df1 = pd.read_csv(r'./data/protein_basic_info.csv')
df2 = pd.read_csv(r'./data/Iupred2.csv')

df3 = pd.read_csv(r'./data/ptm_info.csv')
df3['PMID'] = df3['PMID'].astype(str)

df4 = pd.read_csv(r'./data/structure_atom.csv')
df5 = pd.read_csv(r'./data/aa_markpoint.csv')
df6 = pd.read_csv(r'./data/interactions.csv')
df7 = pd.read_csv(r'./data/search_summary.csv')

df8 = pd.read_csv(r'./data/plddt.csv')
df9 = pd.read_csv(r'./data/aa_plddt.csv')

df100 = pd.read_csv(r'./data/PMID.csv')


class Config:
    SECRET_KEY = 'hard to guess string'
    SSL_DISABLE = False
    WTF_CSRF_ENABLED = False
    DEBUG = False


class NonValidatingSelectField(SelectField):
    # Skip the pre-validation, otherwise it will raise the "Not a valid choice" error
    def pre_validate(self, form):
        pass


class QueryForm(FlaskForm):

    # 基因
    keyword2 = StringField()

    # 物种
    search_organism = SelectField('Organism',
                                  choices=[['H. sapiens', 'H. sapiens'],
                                           ['A. thaliana', 'A. thaliana'],
                                           ['C. elegans', 'C. elegans'],
                                           ['D. melanogaster', 'D. melanogaster'],
                                           ['S. cerevisiae', 'S. cerevisiae'],
                                           ['S. pombe', 'S. pombe'],
                                           ['M. musculus', 'M. musculus'],
                                           ['R. norvegicus', 'R. norvegicus'],
                                           ['S. scrofa', 'S. scrofa'],
                                           ['M. tuberculosis', 'M. tuberculosis'],
                                           ['SARS-COV2', 'SARS-COV2'],
                                           ['Bluetongue virus 2',
                                               'Bluetongue virus 2'],
                                           ['Measles virus', 'Measles virus'],
                                           ['C. hordei', 'C. hordei']],
                                  validators=[DataRequired()],
                                  default='H. sapiens')

    # PTM
    Phos = BooleanField("Phos", default=True,
                        false_values=('False', 'false', ''))
    Me = BooleanField("Me", default=True, false_values=('False', 'false', ''))
    Ace = BooleanField("Ace", default=True,
                       false_values=('False', 'false', ''))
    SUMO = BooleanField("SUMO", default=True,
                        false_values=('False', 'false', ''))
    ADPr = BooleanField("ADPr", default=True,
                        false_values=('False', 'false', ''))
    Ub = BooleanField("Ub", default=True, false_values=('False', 'false', ''))
    Citru = BooleanField("Citru", default=True,
                         false_values=('False', 'false', ''))
    Glyco = BooleanField("Glyco", default=True,
                         false_values=('False', 'false', ''))
    Gluta = BooleanField("Gluta", default=True,
                         false_values=('False', 'false', ''))
    Hypu = BooleanField("Hypu", default=True,
                        false_values=('False', 'false', ''))
    NEDDy = BooleanField("NEDDy", default=True,
                         false_values=('False', 'false', ''))
    Myris = BooleanField("Myris", default=True,
                         false_values=('False', 'false', ''))
    Nitro = BooleanField("Nitro", default=True,
                         false_values=('False', 'false', ''))
    Hydro = BooleanField("Hydro", default=True,
                         false_values=('False', 'false', ''))

    submit = SubmitField('Search')


class QForm(FlaskForm):
    keyword = StringField()
    submit = SubmitField('Search')


##################### 主函数####################################################
app = Flask(__name__)
app.config.from_object(Config)
Bootstrap(app)


def global_count():
    global COUNT
    return COUNT


app.add_template_global(global_count, 'global_count')

# Extra redirect request for "/favicon.ico"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.before_request
def count():
    global COUNT
    import re
    if not re.match(r'^.*\.\w{1,6}$', request.path):
        COUNT += 1
    if COUNT % 10 == 0:
        open('static/count.txt', 'w').write(str(COUNT))

# Home page


@app.route('/')
def index():
    return render_template('index.html')


# Other pages
@app.route('/<string:page>')
def show(page):
    if str(page) == "Statistics":
        gg = df100.reset_index(drop=True)
        gg1 = gg.to_json(orient='records')
        query_list = json.loads(gg1)
        return render_template('Statistics.html', list=query_list)

    else:
        return render_template('{}.html'.format(page))


# data
@app.route('/data/<string:page>')
def data(page):
    return send_from_directory('data/', page)


# Search database
@app.route('/Search', methods=['GET', 'POST'])
def search():
    form = QueryForm(data=request.form)
    organism = form.search_organism.data
    gene = form.keyword2.data

    AA = form.Phos.data  # Boolean 类型
    BB = form.Me.data  # Boolean 类型
    CC = form.Ace.data  # Boolean 类型
    DD = form.SUMO.data  # Boolean 类型
    EE = form.ADPr.data  # Boolean 类型
    FF = form.Ub.data  # Boolean 类型
    GG = form.Citru.data  # Boolean 类型
    HH = form.Glyco.data  # Boolean 类型
    II = form.Gluta.data  # Boolean 类型
    JJ = form.Hypu.data  # Boolean 类型
    KK = form.NEDDy.data  # Boolean 类型
    LL = form.Myris.data  # Boolean 类型
    MM = form.Nitro.data  # Boolean 类型
    NN = form.Hydro.data  # Boolean 类型

    if request.method == 'GET':
        return render_template('Search.html')
    elif request.method == 'POST':
        if str(gene) == "":

            if str(AA) == "True":
                yy1 = df7[(df7.PTM == "Phosphorylation")
                          & (df7.Organism == organism)]
            else:
                yy1 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(BB) == "True":
                yy2 = df7[(df7.PTM == "Methylation") &
                          (df7.Organism == organism)]
            else:
                yy2 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(CC) == "True":
                yy3 = df7[(df7.PTM == "Acetylation") &
                          (df7.Organism == organism)]
            else:
                yy3 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(DD) == "True":
                yy4 = df7[(df7.PTM == "SUMOylation") &
                          (df7.Organism == organism)]
            else:
                yy4 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(EE) == "True":
                yy5 = df7[(df7.PTM == "ADP-ribosylation")
                          & (df7.Organism == organism)]
            else:
                yy5 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(FF) == "True":
                yy6 = df7[(df7.PTM == "Ubiquitination")
                          & (df7.Organism == organism)]
            else:
                yy6 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(GG) == "True":
                yy7 = df7[(df7.PTM == "Citrullination")
                          & (df7.Organism == organism)]
            else:
                yy7 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(HH) == "True":
                yy8 = df7[(df7.PTM == "Glycosylation")
                          & (df7.Organism == organism)]
            else:
                yy8 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(II) == "True":
                yy9 = df7[(df7.PTM == "Glutathionylation")
                          & (df7.Organism == organism)]
            else:
                yy9 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(JJ) == "True":
                yy10 = df7[(df7.PTM == "Hypusination") &
                           (df7.Organism == organism)]
            else:
                yy10 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(KK) == "True":
                yy11 = df7[(df7.PTM == "NEDDylation") &
                           (df7.Organism == organism)]
            else:
                yy11 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(LL) == "True":
                yy12 = df7[(df7.PTM == "N-myristoylation")
                           & (df7.Organism == organism)]
            else:
                yy12 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(MM) == "True":
                yy13 = df7[(df7.PTM == "S-nitrosylation")
                           & (df7.Organism == organism)]
            else:
                yy13 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            if str(NN) == "True":
                yy14 = df7[(df7.PTM == "Hydroxylation")
                           & (df7.Organism == organism)]
            else:
                yy14 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            yy15 = pd.concat([yy1, yy2, yy3, yy4, yy5, yy6, yy7, yy8, yy9, yy10, yy11, yy12, yy13, yy14]).drop(
                'MLO', axis=1).drop_duplicates().reset_index(drop=True)

            if len(yy15) == 0:
                yy15 = df7[(df7.Organism == organism)].drop(
                    'MLO', axis=1).drop_duplicates().reset_index(drop=True)
                yy16 = yy15.to_json(orient='records')
                query_list = json.loads(yy16)
                return render_template('search_result_test.html', browse_list=query_list)
            else:
                yy16 = yy15.to_json(orient='records')
                query_list = json.loads(yy16)
                return render_template('search_result_test.html', browse_list=query_list)

        else:
            uu1 = df7[df7["Gene"].str.contains(gene, case=False)]
            uu1 = uu1[(uu1.Organism == organism)]

            uu3 = df7[df7["Uniprot"].str.contains(gene, case=False)]
            uu3 = uu3[(uu3.Organism == organism)]

            if len(uu1) == 0:
                uu1 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
            if len(uu3) == 0:
                uu3 = pd.DataFrame(
                    columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

            uu2 = pd.concat(
                [uu1, uu3]).drop_duplicates().reset_index(drop=True)

            if len(uu2) == 0:
                X10 = "No matching records found!"
                return render_template('Search.html', X10=X10)

            else:
                if str(AA) == "True":
                    yy1 = uu2[(uu2.PTM == "Phosphorylation")]
                    if len(yy1) == 0:
                        yy1 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy1 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(BB) == "True":
                    yy2 = uu2[(uu2.PTM == "Methylation")]
                    if len(yy2) == 0:
                        yy2 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy2 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(CC) == "True":
                    yy3 = uu2[(uu2.PTM == "Acetylation")]
                    if len(yy3) == 0:
                        yy3 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy3 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(DD) == "True":
                    yy4 = uu2[(uu2.PTM == "SUMOylation")]
                    if len(yy4) == 0:
                        yy4 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy4 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(EE) == "True":
                    yy5 = uu2[(uu2.PTM == "ADP-ribosylation")]
                    if len(yy5) == 0:
                        yy5 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy5 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(FF) == "True":
                    yy6 = uu2[(uu2.PTM == "Ubiquitination")]
                    if len(yy6) == 0:
                        yy6 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy6 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(GG) == "True":
                    yy7 = uu2[(uu2.PTM == "Citrullination")]
                    if len(yy7) == 0:
                        yy7 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy7 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(HH) == "True":
                    yy8 = uu2[(uu2.PTM == "Glycosylation")]
                    if len(yy8) == 0:
                        yy8 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy8 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(II) == "True":
                    yy9 = uu2[(uu2.PTM == "Glutathionylation")]
                    if len(yy9) == 0:
                        yy9 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy9 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(JJ) == "True":
                    yy10 = uu2[(uu2.PTM == "Hypusination")]
                    if len(yy10) == 0:
                        yy10 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy10 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(KK) == "True":
                    yy11 = uu2[(uu2.PTM == "NEDDylation")]
                    if len(yy11) == 0:
                        yy11 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy11 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(LL) == "True":
                    yy12 = uu2[(uu2.PTM == "N-myristoylation")]
                    if len(yy12) == 0:
                        yy12 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy12 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(MM) == "True":
                    yy13 = uu2[(uu2.PTM == "S-nitrosylation")]
                    if len(yy13) == 0:
                        yy13 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy13 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                if str(NN) == "True":
                    yy14 = uu2[(uu2.PTM == "Hydroxylation")]
                    if len(yy14) == 0:
                        yy14 = pd.DataFrame(
                            columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])
                else:
                    yy14 = pd.DataFrame(
                        columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

                yy15 = pd.concat([yy1, yy2, yy3, yy4, yy5, yy6, yy7, yy8, yy9, yy10, yy11, yy12, yy13, yy14]).drop(
                    'MLO', axis=1).drop_duplicates().reset_index(drop=True)

                if len(yy15) == 0:
                    X10 = "No matching records found!"
                    return render_template('Search.html', X10=X10)
                else:
                    yy16 = yy15.to_json(orient='records')
                    query_list = json.loads(yy16)
                    return render_template('search_result_test.html', browse_list=query_list)


@app.route('/Home', methods=['GET', 'POST'])
def index2():
    form = QForm(data=request.form)
    AAAA = form.keyword.data

    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        ww1 = df7[df7["Organism"].str.contains(AAAA, case=False)]
        if len(ww1) == 0:
            ww1 = pd.DataFrame(
                columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

        ww2 = df7[df7["Gene"].str.contains(AAAA, case=False)]
        if len(ww2) == 0:
            ww2 = pd.DataFrame(
                columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

        ww3 = df7[df7["Uniprot"].str.contains(AAAA, case=False)]
        if len(ww3) == 0:
            ww3 = pd.DataFrame(
                columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

        ww4 = df7[df7["PTM"].str.contains(AAAA, case=False)]
        if len(ww4) == 0:
            ww4 = pd.DataFrame(
                columns=["Organism", "Gene", "Uniprot", "PTM", "PMID", "MLO"])

        ww8 = pd.concat([ww1, ww2, ww3, ww4]).drop(
            'MLO', axis=1).drop_duplicates().reset_index(drop=True)

        if len(ww8) == 0:
            X10 = "No matching records found!"
            return render_template('index.html', X10=X10)
        else:
            ww9 = ww8.to_json(orient='records')
            query_list = json.loads(ww9)
            return render_template('search_result_test.html', browse_list=query_list)


# Result page1
@app.route('/Search/<string:uniprot>')
def result(uniprot):
    C1 = uniprot  # uniprot
    basic = df1[(df1.Uniprot == C1)]
    A1 = basic.iat[0, 1]  # 基因名
    B1 = basic.iat[0, 3]  # 蛋白名
    D1 = basic.iat[0, 0]  # 物种名

    Iu_hydro = df2[(df2.Uniprot == C1)]
    E1 = Iu_hydro['Site'].to_list()
    F1 = Iu_hydro['Iupred2'].to_list()
	
    Iu_plddt = df8[(df8.Uniprot == C1)]
    H1 = Iu_plddt['Site'].to_list()
    I1 = Iu_plddt['plddt'].to_list()	
	
	
	

    # markpoint

    mark = df5[df5.Uniprot == C1]
    mark1 = mark[['Label', 'Site', 'Iupred2']]
    mark1.columns = ['value', 'xAxis', 'yAxis']
    mm2 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in mark1.iterrows()]


    markk = df9[df9.Uniprot == C1]
    markk1 = markk[['Label', 'Site', 'plddt']]
    markk1.columns = ['value', 'xAxis', 'yAxis']
    mm3 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in markk1.iterrows()]

    Y1 = C1 + "_iupred2_features.csv"
    Y2 = './data/' + Y1
    Iu_hydro.to_csv(Y2, index=False)

    Z1 = C1 + "_plddt_features.csv"
    Z2 = './data/' + Z1
    Iu_plddt.to_csv(Z2, index=False)



    gg = df3[(df3.Uniprot == C1)].reset_index(drop=True)

    # 获得uniprot对应的interaction表格

    gg1 = gg.to_json(orient='records')
    int_list = json.loads(gg1)

    # 获得uniprot对应的ppi表格
    hh = df6[(df6.Uniprot1 == C1)].reset_index(drop=True)
    hh1 = hh.to_json(orient='records')
    ppi_list = json.loads(hh1)

    # 获得uniprot对应的复合物信息(first)
    K1 = gg[['Structure']].iat[0, 0]  # 复合物名称

    # gg[['Complex','PDBRES']].drop_duplicates()

    complexList = gg['Structure'].drop_duplicates().to_list()
    labelList = df4[df4.Structure.isin(complexList)].to_json(orient="records")

    # 获得uniprot对应的复合物信息(first)对应的pdbres
    U1 = gg[['PDBRES']].iat[0, 0]  # pdbres
    U2 = gg[['PTM']].iat[0, 0]  # PTM
    U3 = gg[['Site']].iat[0, 0]  # Site

    U4 = df4[(df4.Structure == K1) & (df4.PDBRES == U1)
             & (df4.PTM == U2) & (df4.Site == U3)]
    xx = U4.iat[0, 6]
    yy = U4.iat[0, 7]
    zz = U4.iat[0, 8]
    label = U4.iat[0, 4]

    return render_template('result_page.html', A1=A1, B1=B1, C1=C1, D1=D1, E1=E1, F1=F1, mm2=mm2,H1=H1,I1=I1,mm3=mm3,Z1=Z1,
                           K1=K1, Y1=Y1, xx=xx, yy=yy, zz=zz, label=label, int=int_list, ppi=ppi_list,
                           complexList=complexList, labelList=labelList)


# Result page2
@app.route('/get_table_data/Search/<string:uniprot>')
def result2(uniprot):
    C1 = uniprot  # uniprot
    basic = df1[(df1.Uniprot == C1)]

    A1 = basic.iat[0, 1]  # 基因名
    B1 = basic.iat[0, 3]  # 蛋白名
    D1 = basic.iat[0, 0]  # 物种名

    Iu_hydro = df2[(df2.Uniprot == C1)]
    E1 = Iu_hydro['Site'].to_list()
    F1 = Iu_hydro['Iupred2'].to_list()
	
    Iu_plddt = df8[(df8.Uniprot == C1)]
    H1 = Iu_plddt['Site'].to_list()
    I1 = Iu_plddt['plddt'].to_list()	

    # markpoint

    mark = df5[df5.Uniprot == C1]
    mark1 = mark[['Label', 'Site', 'Iupred2']]
    mark1.columns = ['value', 'xAxis', 'yAxis']
    mm2 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in mark1.iterrows()]


    markk = df9[df9.Uniprot == C1]
    markk1 = markk[['Label', 'Site', 'plddt']]
    markk1.columns = ['value', 'xAxis', 'yAxis']
    mm3 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in markk1.iterrows()]

    Y1 = C1 + "_iupred2_features.csv"
    Y2 = './data/' + Y1
    Iu_hydro.to_csv(Y2, index=False)

    Z1 = C1 + "_plddt_features.csv"
    Z2 = './data/' + Z1
    Iu_plddt.to_csv(Z2, index=False)
	

    gg = df3[(df3.Uniprot == C1)].reset_index(drop=True)

    # 获得uniprot对应的interaction表格

    gg1 = gg.to_json(orient='records')
    int_list = json.loads(gg1)

    # 获得uniprot对应的ppi表格
    hh = df6[(df6.Uniprot1 == C1)].reset_index(drop=True)
    hh1 = hh.to_json(orient='records')
    ppi_list = json.loads(hh1)

    # 获得uniprot对应的复合物信息(first)
    K1 = gg[['Structure']].iat[0, 0]  # 复合物名称

    # gg[['Complex','PDBRES']].drop_duplicates()

    complexList = gg['Structure'].drop_duplicates().to_list()
    labelList = df4[df4.Structure.isin(complexList)].to_json(orient="records")

    # 获得uniprot对应的复合物信息(first)对应的pdbres
    U1 = gg[['PDBRES']].iat[0, 0]  # pdbres
    U2 = gg[['PTM']].iat[0, 0]  # PTM
    U3 = gg[['Site']].iat[0, 0]  # Site

    U4 = df4[(df4.Structure == K1) & (df4.PDBRES == U1)
             & (df4.PTM == U2) & (df4.Site == U3)]
    xx = U4.iat[0, 6]
    yy = U4.iat[0, 7]
    zz = U4.iat[0, 8]
    label = U4.iat[0, 4]

    return render_template('result_page.html', A1=A1, B1=B1, C1=C1, D1=D1, E1=E1, F1=F1, mm2=mm2,H1=H1,I1=I1,mm3=mm3,Z1=Z1,
                           K1=K1, Y1=Y1, xx=xx, yy=yy, zz=zz, label=label, int=int_list, ppi=ppi_list,
                           complexList=complexList, labelList=labelList)


# Result page3
@app.route('/get_table_data/Search/<string:ptm2>/<string:uniprot>')
def result3(ptm2, uniprot):
    ptm = ptm2  # uniprot
    C1 = uniprot  # uniprot

    basic = df1[(df1.Uniprot == C1)]
    A1 = basic.iat[0, 1]  # 基因名
    B1 = basic.iat[0, 3]  # 蛋白名
    D1 = basic.iat[0, 0]  # 物种名

    Iu_hydro = df2[(df2.Uniprot == C1)]
    E1 = Iu_hydro['Site'].to_list()
    F1 = Iu_hydro['Iupred2'].to_list()

    Iu_plddt = df8[(df8.Uniprot == C1)]
    H1 = Iu_plddt['Site'].to_list()
    I1 = Iu_plddt['plddt'].to_list()	




    # markpoint

    mark = df5[(df5.Uniprot == C1) & (df5.PTM == ptm)]
    mark1 = mark[['Label', 'Site', 'Iupred2']]
    mark1.columns = ['value', 'xAxis', 'yAxis']
    mm2 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in mark1.iterrows()]



    markk = df9[(df9.Uniprot == C1)& (df9.PTM == ptm)]
    markk1 = markk[['Label', 'Site', 'plddt']]
    markk1.columns = ['value', 'xAxis', 'yAxis']
    mm3 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in markk1.iterrows()]

    Y1 = C1 + "_iupred2_features.csv"
    Y2 = './data/' + Y1
    Iu_hydro.to_csv(Y2, index=False)

    Z1 = C1 + "_plddt_features.csv"
    Z2 = './data/' + Z1
    Iu_plddt.to_csv(Z2, index=False)



    gg = df3[(df3.Uniprot == C1) & (df3.PTM == ptm)].reset_index(drop=True)

    # 获得uniprot对应的interaction表格

    gg1 = gg.to_json(orient='records')
    int_list = json.loads(gg1)

    # 获得uniprot对应的ppi表格
    hh = df6[(df6.Uniprot1 == C1)].reset_index(drop=True)
    hh1 = hh.to_json(orient='records')
    ppi_list = json.loads(hh1)

    # 获得uniprot对应的复合物信息(first)
    K1 = gg[['Structure']].iat[0, 0]  # 复合物名称

    # gg[['Complex','PDBRES']].drop_duplicates()

    complexList = gg['Structure'].drop_duplicates().to_list()

    df10 = df4[(df4.PTM == ptm)]

    labelList = df10[df10.Structure.isin(
        complexList)].to_json(orient="records")

    # 获得uniprot对应的复合物信息(first)对应的pdbres
    U1 = gg[['PDBRES']].iat[0, 0]  # pdbres
    U2 = gg[['PTM']].iat[0, 0]  # PTM
    U3 = gg[['Site']].iat[0, 0]  # Site

    U4 = df4[(df4.Structure == K1) & (df4.PDBRES == U1)
             & (df4.PTM == U2) & (df4.Site == U3)]
    xx = U4.iat[0, 6]
    yy = U4.iat[0, 7]
    zz = U4.iat[0, 8]
    label = U4.iat[0, 4]

    return render_template('result_page2.html', A1=A1, B1=B1, C1=C1, D1=D1, E1=E1, F1=F1, mm2=mm2,H1=H1,I1=I1,mm3=mm3,Z1=Z1,
                           K1=K1, Y1=Y1, xx=xx, yy=yy, zz=zz, label=label, int=int_list, ppi=ppi_list,
                           complexList=complexList, labelList=labelList)


# Result page4
@app.route('/Search/<string:ptm2>/<string:uniprot>')
def result4(ptm2, uniprot):
    ptm = ptm2  # uniprot
    C1 = uniprot  # uniprot

    basic = df1[(df1.Uniprot == C1)]
    A1 = basic.iat[0, 1]  # 基因名
    B1 = basic.iat[0, 3]  # 蛋白名
    D1 = basic.iat[0, 0]  # 物种名

    Iu_hydro = df2[(df2.Uniprot == C1)]
    E1 = Iu_hydro['Site'].to_list()
    F1 = Iu_hydro['Iupred2'].to_list()

    Iu_plddt = df8[(df8.Uniprot == C1)]
    H1 = Iu_plddt['Site'].to_list()
    I1 = Iu_plddt['plddt'].to_list()	


    # markpoint

    mark = df5[(df5.Uniprot == C1) & (df5.PTM == ptm)]
    mark1 = mark[['Label', 'Site', 'Iupred2']]
    mark1.columns = ['value', 'xAxis', 'yAxis']
    mm2 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in mark1.iterrows()]



    markk = df9[(df9.Uniprot == C1)& (df9.PTM == ptm)]
    markk1 = markk[['Label', 'Site', 'plddt']]
    markk1.columns = ['value', 'xAxis', 'yAxis']
    mm3 = [{'value': m['value'], 'xAxis': m['xAxis'], 'yAxis': m['yAxis'], 'itemStyle': {
        'color': "rgba(115, 159, 250, .8)"}} for u, m in markk1.iterrows()]

    Y1 = C1 + "_iupred2_features.csv"
    Y2 = './data/' + Y1
    Iu_hydro.to_csv(Y2, index=False)

    Z1 = C1 + "_plddt_features.csv"
    Z2 = './data/' + Z1
    Iu_plddt.to_csv(Z2, index=False)
	
	
	
	

    gg = df3[(df3.Uniprot == C1) & (df3.PTM == ptm)].reset_index(drop=True)

    # 获得uniprot对应的interaction表格

    gg1 = gg.to_json(orient='records')
    int_list = json.loads(gg1)

    # 获得uniprot对应的ppi表格
    hh = df6[(df6.Uniprot1 == C1)].reset_index(drop=True)
    hh1 = hh.to_json(orient='records')
    ppi_list = json.loads(hh1)

    # 获得uniprot对应的复合物信息(first)
    K1 = gg[['Structure']].iat[0, 0]  # 复合物名称

    # gg[['Complex','PDBRES']].drop_duplicates()

    complexList = gg['Structure'].drop_duplicates().to_list()

    df10 = df4[(df4.PTM == ptm)]

    labelList = df10[df10.Structure.isin(
        complexList)].to_json(orient="records")

    # 获得uniprot对应的复合物信息(first)对应的pdbres
    U1 = gg[['PDBRES']].iat[0, 0]  # pdbres
    U2 = gg[['PTM']].iat[0, 0]  # PTM
    U3 = gg[['Site']].iat[0, 0]  # Site

    U4 = df4[(df4.Structure == K1) & (df4.PDBRES == U1)
             & (df4.PTM == U2) & (df4.Site == U3)]
    xx = U4.iat[0, 6]
    yy = U4.iat[0, 7]
    zz = U4.iat[0, 8]
    label = U4.iat[0, 4]

    return render_template('result_page2.html', A1=A1, B1=B1, C1=C1, D1=D1, E1=E1, F1=F1, mm2=mm2,H1=H1,I1=I1,mm3=mm3,Z1=Z1,
                           K1=K1, Y1=Y1, xx=xx, yy=yy, zz=zz, label=label, int=int_list, ppi=ppi_list,
                           complexList=complexList, labelList=labelList)


# Table for browse


@app.route('/get_table_data/<string:table_id>')
def res(table_id):
    if table_id == "table1":
        ZZ = df7[(df7.Organism == "Homo sapiens")]
    elif table_id == "table2":
        ZZ = df7[(df7.Organism == "Arabidopsis thaliana")]
    elif table_id == "table3":
        ZZ = df7[(df7.Organism == "Caenorhabditis elegans")]
    elif table_id == "table4":
        ZZ = df7[(df7.Organism == "Drosophila melanogaster")]
    elif table_id == "table5":
        ZZ = df7[(df7.Organism == "Saccharomyces cerevisiae")]
    elif table_id == "table6":
        ZZ = df7[(df7.Organism == "Schizosaccharomyces pombe")]
    elif table_id == "table7":
        ZZ = df7[(df7.Organism == "Mus musculus")]
    elif table_id == "table8":
        ZZ = df7[(df7.Organism == "Rattus norvegicus")]
    elif table_id == "table9":
        ZZ = df7[(df7.Organism == "Sus scrofa")]
    elif table_id == "table10":
        ZZ = df7[(df7.Organism == "Mycobacterium tuberculosis")]
    elif table_id == "table11":
        ZZ = df7[(df7.Organism == "Severe acute respiratory syndrome coronavirus 2")]
    elif table_id == "table12":
        ZZ = df7[(df7.Organism == "Bluetongue virus 2")]
    elif table_id == "table13":
        ZZ = df7[(df7.Organism == "Measles virus")]
    elif table_id == "table14":
        ZZ = df7[(df7.Organism == "Cytorhabdovirus hordei")]

    elif table_id == "table15":
        ZZ = df7[(df7.PTM == "Phosphorylation")]
    elif table_id == "table16":
        ZZ = df7[(df7.PTM == "Methylation")]
    elif table_id == "table17":
        ZZ = df7[(df7.PTM == "Acetylation")]
    elif table_id == "table18":
        ZZ = df7[(df7.PTM == "SUMOylation")]
    elif table_id == "table19":
        ZZ = df7[(df7.PTM == "ADP-ribosylation")]
    elif table_id == "table20":
        ZZ = df7[(df7.PTM == "Ubiquitination")]
    elif table_id == "table21":
        ZZ = df7[(df7.PTM == "Citrullination")]
    elif table_id == "table22":
        ZZ = df7[(df7.PTM == "Glycosylation")]
    elif table_id == "table23":
        ZZ = df7[(df7.PTM == "Glutathionylation")]
    elif table_id == "table24":
        ZZ = df7[(df7.PTM == "Hypusination")]
    elif table_id == "table25":
        ZZ = df7[(df7.PTM == "NEDDylation")]
    elif table_id == "table26":
        ZZ = df7[(df7.PTM == "N-myristoylation")]
    elif table_id == "table27":
        ZZ = df7[(df7.PTM == "S-nitrosylation")]
    elif table_id == "table28":
        ZZ = df7[(df7.PTM == "Hydroxylation")]

    elif table_id == "table29":
        ZZ = df7[(df7.MLO == "Cajal body")]
    elif table_id == "table30":
        ZZ = df7[(df7.MLO == "Centrosome")]
    elif table_id == "table31":
        ZZ = df7[(df7.MLO == "Chromatin")]
    elif table_id == "table32":
        ZZ = df7[(df7.MLO == "Droplet")]
    elif table_id == "table33":
        ZZ = df7[(df7.MLO == "Insulator body")]
    elif table_id == "table34":
        ZZ = df7[(df7.MLO == "Microtubule")]
    elif table_id == "table35":
        ZZ = df7[(df7.MLO == "Nuage")]
    elif table_id == "table36":
        ZZ = df7[(df7.MLO == "Nuclear speckle")]
    elif table_id == "table37":
        ZZ = df7[(df7.MLO == "Nuclear Sress granule")]
    elif table_id == "table38":
        ZZ = df7[(df7.MLO == "Nucleolus")]
    elif table_id == "table39":
        ZZ = df7[(df7.MLO == "Others")]
    elif table_id == "table40":
        ZZ = df7[(df7.MLO == "P granule")]
    elif table_id == "table41":
        ZZ = df7[(df7.MLO == "Paraspeckle")]
    elif table_id == "table42":
        ZZ = df7[(df7.MLO == "P-body")]
    elif table_id == "table43":
        ZZ = df7[(df7.MLO == "PML nuclear body")]
    elif table_id == "table44":
        ZZ = df7[(df7.MLO == "Postsynaptic density")]
    elif table_id == "table45":
        ZZ = df7[(df7.MLO == "Spindle apparatus")]
    elif table_id == "table46":
        ZZ = df7[(df7.MLO == "Sress granule")]
    else:
        return jsonify({})

    ZZ1 = ZZ.drop('MLO', axis=1).drop_duplicates().reset_index(
        drop=True).to_json(orient='records')
    return jsonify(json.loads(ZZ1))


@app.route('/queryFilterdGene1/<string:ptmType1>')
def queryFilterdGene1(ptmType1):
    df10 = df3[(df3.PTM == ptmType1)]
    gene = df10[['Gene']].drop_duplicates()['Gene'].tolist()
    return jsonify(gene)


if __name__ == '__main__':
    # 对应intenal IP
    app.run(host='127.0.0.1', port=8010, debug=True)
