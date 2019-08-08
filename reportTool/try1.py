import platform
print(platform.architecture())
import json
import os
import cx_Oracle
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import create_engine
from datetime import datetime
import pdfkit 

username = 'tripoahlg2'
password = 'tripoahlg2'

time =datetime.now().time().microsecond 

con = cx_Oracle.connect('tripoahlg2','tripoahlg2','192.168.3.70:1521/TRIPOAHLG')
nmrcCon = cx_Oracle.connect('nmrc','nmrc#1244','tripoadb-scan.tripoa.net.br/TRIPOA')

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("myreport.html")
template = env.get_template("myreport.html")

sql= '''select * from rcreportdemand where created >= sysdate -1'''

relatorios = pd.read_sql_query(sql,nmrcCon)
items=[]
for index, row in relatorios.iterrows():
    anItem = dict(demandId=row['RCREPORTDEMANDID'],reportid=row['RCREPORTID'],filename=row['RCFILENAME'])
    items.append(anItem)

header=[]
header.append(dict(nome='DemandId'))
header.append(dict(nome='ReportId'))
header.append(dict(nome='File Name'))

headerTemplate = """
<!doctype html>
  <html>
    <head>        
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <script>
        function subst() {
          
          var vars={};
          var x=document.location.search.substring(1).split('&');
          for (var i in x) {var z=x[i].split('=',2);vars[z[0]] = unescape(z[1]);}
          var x=['frompage','topage','page','webpage','section','subsection','subsubsection'];
            for (var i in x) {
                var y = document.getElementsByClassName(x[i]);
                for (var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]]; 

                //document.getElementById("teste").innerHTML = "testeaa";

                if(vars['page'] > 1){
                    document.getElementById("FakeHeaders").style.display = 'none';
                }
                else{          
                    document.getElementById("FakeHeaders").style.display = 'block';
                }
            }
        }
        </script>
    </head>
    <body style="border:0;margin:0;" onload="subst()">
        <span id="FakeHeaders">{{nome}} - {{versao}}</span>
        <span id="teste"></span>
    </body>
</html>
"""
headerTemplate = headerTemplate.replace("{{nome}}","Relatório Novo - R20")
headerTemplate = headerTemplate.replace("{{versao}}",str(time))


#for header in list(relatorios):
#    print(header)

template_vars = {"title" : "Teste para novo MRC",
                 "national_pivot_table": relatorios.to_html(),
                 "header":header,
                 "rows":items,
                 "teste":'testestestesteste'}

html_out = template.render(template_vars)
options = {
            'footer-html':  "C:\\MEUGIT\\estudos\\python\\reportTool\\htmlCommon\\footer.html",            
            'footer-right': 'Página [page] de [topage]',
            'header-html': 'C:\\MEUGIT\\estudos\\python\\reportTool\\htmlCommon\\header.html',
            'header-right': '[page]',
        }



print(headerTemplate)



f= open("htmlCommon\\header.html","w+")
f.write(headerTemplate)
f.close();
#print(t.render(c))

#import time
#time.sleep(4) # Delay for 5 seconds.

print(time)
pdfkit.from_string(html_out,'relatorio'+str(time)+'.pdf', options=options)  


#from weasyprint import HTML
#HTML(string=html_out).write_pdf("report.pdf")


#print(relatoriosErros)