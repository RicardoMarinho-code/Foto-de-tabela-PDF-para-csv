import win32com.client
excel = win32com.client.Dispatch("Excel.Application")
print(dir(excel))