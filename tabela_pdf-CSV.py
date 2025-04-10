import pyautogui as pag
import time
import win32com.client

pdf_path = "C:/caminho/para/seu/Layout_novo__modelo_unipessoais_final.xlsx_Correção CPF Lote 35.pdf"

# abre o excel com Win + R
def abrir_excel():

    #hotkey aperta vários botões ao mesmo temopo
    pag.hotkey('win', 'r') #Abre o executar do windows
    time.sleep(1)
    
    pag.write('excel')
    pag.press('enter')
    time.sleep(3)

def imp_pdf():

    #conecta o excel
    excel = win32com.client.Dispatch("Excel.Application")
    
    #deixa o excel visívell
    excel.Visible = True 
    time.sleep(2)

    # Abre uma nova pasta de trabalho (workbook)
    workbook = excel.Workbooks.Add()

    # Usa o recurso "Obter Dados" para importar o PDF
    query = workbook.Queries.Add(Name="ImportacaoPDF", 
                                 Formula=f"let Fonte = Pdf.Tables(File.Contents(\"{pdf_path}\"), [Implementation=\"1.0\"]) in Fonte")
    
    # Cria uma nova planilha e conecta à consulta
    sheet = workbook.Sheets.Add()
    sheet.Name = "Dados do PDF"
    table = sheet.ListObjects.Add(SourceType=1, Source=query, Destination=sheet.Range("A1"))

    # Atualiza os dados (carrega o PDF)
    table.Refresh()

    # Salva o arquivo (opcional)
    workbook.SaveAs("C:/caminho/para/salvar/seu_arquivo.xlsx")  # Ajuste o caminho
    # workbook.Close()  # Fecha o workbook (descomente se quiser fechar)
    # excel.Quit()      # Fecha o Excel (descomente se quiser fechar)

# Executa as funções
if __name__ == "__main__":
    abrir_excel()         # Abre o Excel
    imp_pdf()  # Importa o PDF
    print("Automação concluída!")