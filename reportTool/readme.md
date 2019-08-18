#ReportTool 
##Trata-se de uma ferramenta para substituição do Crystal Reports, utilizando apenas algumas linhas de Python e HTML.

Cada relatório precisa ser criado como um arquivo Python. (pasta: templateRelatorio/IdRelatorio) 
Dentro da pasta templateRelatorio/id - deverão existir dois arquivos: *.py e *.html 

O Arquivo html irá receber do arquivo *py* as váriaveis que irá apresentar no relatório final montado através do template. 


#Funcionamento:
*Todas as pastas mencionadas abaixo podem ser configuradas de maneira diferente no arquivo de configuração. 

O arquivo python contém a query e seleciona do banco os filtros que deverão ser substituidos ao executar o comando SQL. 

*importante que na query sejam utilizados os parâmetros à serem substituidos como {?PARAMETRO_NOME}, isso se deve por esse sistema ser uma substiuição do Crystal Reports em uma organização, deste modo todas as querys podem ser retiradas do Crystal Reports e coladas diretamente em um arquivo python. 

O comando é executado e gera um html utilizando um template (arquivo html da mesma pasta (Jinja2)) na pasta generatedHtml, este html gerado é utilizado para criar um pdf dentro da pasta "pdf" (com paginação e cabeçalho previamente definidos conforme explicado na seção anterior).

Pronto, com o relatório gerado o processo está terminado. 

#Melhorias - Fonte de dados
Precisa-se tornar o código mais genérico, fazendo com que ele possa receber os dados de multiplas fontes como arquivos csv.

#Melhorias - html style
Esta ferramenta foi feita basicamente utilizando bootstrap na sua versão mais simples. Mais styles poderiam ser criados para multipla escolha. 


