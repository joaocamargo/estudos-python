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
import sys

print(sys.argv)
print(sys.argv[1])

# configuracoes
idRelatorio ="384"
rcreportdemandid = str(sys.argv[1])
nomeHeader=['Data','Pedido','Código Transação','Tipo','Carga Paga R$','Taxa Paga R$','Total Valor Pedido R$','Taxa Cartão R$','Custo ATP R$','Total Pago R$','Data Previsão','Data Pagamento']
datasConversaoTruncada=['PREVISAO','DATAPAGAMENTO'] #tal comoo alias no select 
datasConversaoComHoraMinuto=[] #tal comoo alias no select 
tamanhoLetraCampos="14"
formatPdf="portrait" #landscape #portrait

#configuracoes

print('Executando rcreportdemandid  = ' + rcreportdemandid)
time =datetime.now().time().microsecond 

basePath="";
headerPath="";
headerPathDiscard="";
footerPath="";
pdfPath="";
generatedHtml="";

#CONFIGURACAO BANCO 
configFile = "..\\..\\report.config"
with open(configFile, 'r', encoding="ISO-8859-1") as f:
    content = f.readlines()
for line in content:
    if(line.find("userTripoa")==0):
        userTripoa = line.split('=')[1].strip()        
    if(line.find("passTripoa")==0):
        passTripoa = line.split('=')[1].strip()    
    if(line.find("dataTripoa")==0):
        dataTripoa = line.split('=')[1].strip()    
    if(line.find("userNMRC")==0):
        userNMRC = line.split('=')[1].strip()        
    if(line.find("passNMRC")==0):
        passNMRC = line.split('=')[1].strip()    
    if(line.find("dataNMRC")==0):
        dataNMRC = line.split('=')[1].strip()
    if(line.find("basePath")==0):
         basePath = line.split('=')[1].strip()
    if(line.find("headerPathTemplate")==0):
         headerPath = line.split('=')[1].strip()
    if(line.find("footerPath")==0):
         footerPath = line.split('=')[1].strip()
    if(line.find("pdfPath")==0):
         pdfPath = line.split('=')[1].strip()
    if(line.find("generatedHtml")==0):
         generatedHtml = line.split('=')[1].strip()
    if(line.find("headerPathDiscard")==0):
         headerPathDiscard = line.split('=')[1].strip()
         

nmrcCon = cx_Oracle.connect(userNMRC,passNMRC,dataNMRC)
con = cx_Oracle.connect(userTripoa,passTripoa,dataTripoa)

#CONFIGURACAO BANCO 

#TEMPLATES
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(idRelatorio+".html")

print(headerPath)
envHeader = Environment(loader=FileSystemLoader(headerPath))
templateHeader = envHeader.get_template("header.html")

#TEMPLATES

#QUERIES
#---------------------------------------------------------------------------------
headerSql= '''select * from rcreport where rcreportid = ''' + idRelatorio;
reportSelect = pd.read_sql_query(headerSql,nmrcCon)

#CONFIGURACAO DO HEADER
for index, row in reportSelect.iterrows():
    nomeRelatorio=row['TITLE']
    qualifier=row['QUALIFIER']  
    logo=row['RCLOGOID']  
    exportType=row['RCEXPORTTYPEID']  
    
#--------------------------------------------------------------------------------
#CONFIGURACAO DO DEMAND

headerSql= '''select * from rcreportdemand where rcreportdemandid = ''' + rcreportdemandid;
reportDemandSelect = pd.read_sql_query(headerSql,nmrcCon)

for index, row in reportDemandSelect.iterrows():
    #nomeFinalPDF=row['RCFILENAME']
    rcReportdemandStatusId=row['RCREPORTDEMANDSTATUSID']
    headerInfoParams=row['RCHEADERINFO']  
    exportType=row['RCEXPORTTYPEID']  
#--------------------------------------------------------------------------------


demandSqlFILTERS= '''
select rcreportdemandid,RCREPORTFILTERID,NVL(value,'') as VALUE,TITLE,RCREPORTFILTERDATATYPE from rcreportdemand
inner join rcreportfilterdemand using(rcreportdemandid)
inner join rcreportfilter using (rcreportfilterid)
 where rcreportdemandid =
 ''' + rcreportdemandid;

reportDemandSelectFilter = pd.read_sql_query(demandSqlFILTERS,nmrcCon)


filters=[]
for index, row in reportDemandSelectFilter.iterrows():
    typeFilter = row['RCREPORTFILTERDATATYPE'] 
    #print('typeFilter')
    #print(typeFilter)
    
    valor=str(row['VALUE']).strip()
    if(typeFilter == 3 or typeFilter == 8 or typeFilter == 4):
        valor = "'"+valor+"'"
    valor = valor.replace('None','')
    #print(valor)
    titulo= '{?' + str(row['TITLE']).strip()+'}'
    filterItem = dict(value=valor,filtroTrocar=titulo)
    #print('FILTROS RELATORIO')
    #print(filterItem)
    filters.append(filterItem)    
    
#--------------------------------------------------------------------------------



#CONFIGURACAO DE FILTROS

sql= '''
select rpad.rpad_date as datapagamento, 
       rmt.rom_receiptnbr as pedido, 
       rpt.rpt_acquirer_transaction_id as transacao,
       case when pm.pm_code = 2 then 'Cartao de Debito' when pm.pm_code =7 then 'Cartao de Credito' else pm.pm_desc end as tipo, 
       rpad.rpad_amount - (rmt.rom_admintax - rmt.rom_rettax) as totalprevisto, -- 
       case when rpt.rpt_depositdate <= sysdate then rpad.rpad_amount - (rmt.rom_admintax - rmt.rom_rettax) else 0 end totalPrevistoAteAgora,
       case when rpad_date is not null then rpad.rpad_amount - (rmt.rom_admintax - rmt.rom_rettax)  else 0 end totalpago,
       (select sum (rod.rod_amount)
        from rechargeorderdt rod 
        where rod.rom_tranid = rmt.rom_tranid and
              rod.rom_seqnbr = rmt.rom_seqnbr and
              rod.prv_id = rmt.prv_id) as valorPedido,
       rmt.rom_admintax as taxa,
       trunc(rpt_depositdate) as previsao,
       rpad.rpad_date,
       (rmt.rom_admintax - rmt.rom_rettax) as custo,
       rmt.rom_rettax as saldo,
       case when rpad_date is not null then (rmt.rom_admintax - rmt.rom_rettax) else 0 end as custoEfetivado,
       case when rpad_date is not null then rmt.rom_rettax else 0 end as saldoEfetivado,
       
       to_char(
           case when 2 = 1 then -- data movimentacao financeira
           coalesce(
                  -- select para caso tenha registro 'P'
                  (select rom_memodate from rechargeordermt 
                   where rom_tranid = rmt.Rom_Tranid and 
                         prv_id = rmt.Prv_Id and
                         rom_status = 'P' and
                         rownum <= 1     )                                     
                  ,
                  -- select para caso nao tenha registro 'P', mas tenha 'Q' direto (possibilidade futura)
                  (select rom_memodate from rechargeordermt 
                   where rom_tranid = rmt.Rom_Tranid and 
                         prv_id = rmt.Prv_Id and
                         rom_status = 'Q' )
               ) else 
               (select rom_memodate from rechargeordermt 
                   where rom_tranid = rmt.Rom_Tranid and 
                         prv_id = rmt.Prv_Id and
                         rom_status = 'Q')   end, 'DD/MM/yyyy'            
               ) movOuLib,
               (select sysdate from dual) datageracao,
             CASE WHEN PR.PRV_ID IN (99997,99998) THEN PR.PRV_DESC ELSE 'PEDIDOS VALE TRANSPORTE' END PRV_DESC,
             RPT_GET_ORDER_PAYLOAD(18001, RMT.ROM_RECEIPTNBR,RPAD.RPAD_TRANID) AS CARGAPAGA,
             RPT_GET_ORDER_TAXLOAD(18001, RMT.ROM_RECEIPTNBR,RPAD.RPAD_TRANID) AS TAXAPAGA
       
from rechargeordermt rmt
 INNER JOIN PROVIDERS PR ON 
             PR.PRV_ID = RMT.PRV_ID 
       INNER JOIN PROVIDERSXPROVIDERTYPES PXPT ON PXPT.PRV_ID = PR.PRV_ID AND PRVT_CODE IN ({?PRVXPRVTTYPE})
join rechargeprovideraccountdt rpad on
     (rpad.prv_id, rpad.rpad_tranid) in ( select prv_id, rpad_tranid
                                          from rechargeorderfinancial rofSub
                                          where rofSub.Rom_Tranid = rmt.rom_tranid and 
                                                rofSub.prv_id = rmt.prv_id)
join rechargeprovidertransaction rpt on
     rpt.rpad_tranid = rpad.rpad_tranid and
     rpt.prv_id = rpad.prv_id
join paymentmodes pm on
     pm.pm_code = rpt.pm_code

where 
     rmt.rom_recstat = 'A' and     
     ('{?ESCOLHEDATA3}' = '1' or -- filtro *** data movimentacao financeira              
              nvl(
                  -- select para caso tenha registro 'P'
                  (select trunc(max(rom_memodate)) from rechargeordermt 
                   where rom_tranid = rmt.Rom_Tranid and 
                         prv_id = rmt.Prv_Id and
                         rom_status = 'P')                                          
                  ,
                  -- select para caso nao tenha registro 'P', mas tenha 'Q' direto (possibilidade futura)
                  (select max(trunc(rom_memodate)) from rechargeordermt 
                   where rom_tranid = rmt.Rom_Tranid and 
                         prv_id = rmt.Prv_Id and
                         rom_status = 'Q')
               ) between {?DATAINICIAL} and {?DATAFINAL} ) and

      ('{?ESCOLHEDATA3}' = '2' or -- filtro *** data de liberacao  
                  -- select para caso nao tenha registro 'P', mas tenha 'Q' direto (possibilidade futura)
                  (select max(trunc(rom_memodate)) from rechargeordermt 
                   where rom_tranid = rmt.Rom_Tranid and 
                         prv_id = rmt.Prv_Id and
                         rom_status = 'Q')
                between {?DATAINICIAL} and {?DATAFINAL} ) and

                ({?DATAINICIAL2} is null or trunc(rpt.rpt_depositdate) >= {?DATAINICIAL2}) and -- filtro *** data de previsao
                ({?DATAINICIAL2} is null or trunc(rpt.rpt_depositdate) <= {?DATAFINAL2}) and                
                ({?DATAINICIAL3} is null or trunc(rpad.rpad_date) >= {?DATAINICIAL3}) and -- filtro *** data de pagamento
                ({?DATAINICIAL3} is null or trunc(rpad.rpad_date) <= {?DATAFINAL3}) and
                ('{?SITUACAO_CREDDEB}' = '-1' or (1 in ({?SITUACAO_CREDDEB}) and rpad.rpad_date is null) -- filtro *** a receber
                                            or (2 in ({?SITUACAO_CREDDEB}) and rpad.rpad_date is not null) ) and -- recebido
               ('{?FORMPAGTO_CREDDEB}' = '-1' or rpt.pm_code in ({?FORMPAGTO_CREDDEB}) ) -- filtro *** forma de pagamento   
'''

for filtro in filters:    
    sql = sql.replace(filtro['filtroTrocar'],filtro['value'])

#print(sql)

#print('NOVO SQL')
#print(sql)

relatorioPrincipal = pd.read_sql_query(sql,con)


#FORMATACAO DE DATAS
for filtro in datasConversaoTruncada:
    relatorioPrincipal[filtro] = relatorioPrincipal[filtro].dt.strftime('%m/%d/%Y')    

for filtro in datasConversaoComHoraMinuto:
    relatorioPrincipal[filtro] = pd.to_datetime(relatorioPrincipal[filtro])
    relatorioPrincipal[filtro] = relatorioPrincipal[filtro].dt.strftime('%m/%d/%Y %H:%M')    

#CONFIGURACAO DO SELECT PRINCIPAL

relatorioPrincipal = relatorioPrincipal.replace(np.nan, '', regex=True)
relatorioPrincipal = relatorioPrincipal.replace('NaT', '', regex=True)

headersNames=list(relatorioPrincipal)


items=[]
for index, row in relatorioPrincipal.iterrows():
    itemdict = {}
    for he in headersNames:        
        itemdict[he]=row[he]
    items.append(itemdict)

#print(items)
# for index, row in relatorioPrincipal.iterrows():
#     anItem = dict(
#     datapagamento=str(row['DATAPAGAMENTO']),
#     pedido=str(row['PEDIDO']),
#     transacao=row['transacao'],  
#     tipo=row['tipo'] ,
#     totalprevisto=row['totalprevisto'],     
#     totalPrevistoAteAgora=row['totalPrevistoAteAgora'],
#     totalpago=row['totalpago']  ,
#     valorPedido=row['valorPedido'],
#     taxa=row['taxa'],
#     previsao=row['previsao'],
#     rpad_date=row['rpad_date'],
#     custo=row['custo'],
#     saldo=row['saldo'],
#     custoEfetivado=row['custoEfetivado'],
#     saldoEfetivado=row['saldoEfetivado'],
#     movOuLib=row['movOuLib'],
#     datageracao=row['datageracao'],
#     PRV_DESC=row['PRV_DESC'],
#     CARGAPAGA=row['CARGAPAGA'],
#     TAXAPAGA=row['TAXAPAGA'],
#     )
# items.append(anItem)

#--------------------------------------------------------------------------------


#CONFIGURACAO DO SELECT PRINCIPAL


#CONFIGURACAO DOS PARAMETROS HEADER - PRINCIPAL - FOOTER
#HEADER
templateHeader_vars = {"title" : nomeRelatorio,"qualifier":qualifier}

#PRINCIPAL

if not nomeHeader:
    headersNames=list(relatorioPrincipal)
else:
    headersNames=nomeHeader


template_vars = {"title" : "Teste para novo MRC",
                 "national_pivot_table": relatorioPrincipal.to_html(),                 
                 "rows":items,
                 "headersNames":headersNames,
                 "tamanhoLetraCampos":tamanhoLetraCampos}                 
#FOOTER

#CONFIGURACAO DOS PARAMETROS HEADER - PRINCIPAL - FOOTER
html_out = template.render(template_vars)
htmlHeader_out = templateHeader.render(templateHeader_vars)
options = {
            'footer-html':  "C:\\MEUGIT\\estudos\\python\\reportTool\\htmlCommon\\footer.html",            
            'footer-right': 'Página [page] de [topage]',
            'footer-font-size' : '6',
            'footer-spacing':  '10',
            'header-html':  headerPathDiscard+rcreportdemandid+"-"+str(time)+".html",
            'orientation': formatPdf
            #'header-right': '[page]',
        }

#geracao do header a ser usado pelo relatorio
f= open(headerPathDiscard+rcreportdemandid+"-"+str(time)+".html","w+")
f.write(htmlHeader_out)
f.close();

f= open(generatedHtml+'HtmlFor_'+rcreportdemandid+"-"+str(time)+".html","w+",encoding="ISO-8859-1")
f.write(headerInfoParams + '' + html_out)
f.close();





print(time)

pdfkit.from_string(headerInfoParams + '</hr>' + html_out,pdfPath +'relatorio'+rcreportdemandid+"-"+str(time)+'.pdf', options=options)  