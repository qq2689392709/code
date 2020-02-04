
import xlrd
import xlsxwriter

# 创建工作簿
def filewriting(file_name = "D:\\book.xlsx"):

    workbook = xlsxwriter.Workbook(file_name)

    # 创建工作表
    worksheet = workbook.add_worksheet('first_sheet')

    # 写单元格
    worksheet.write(0, 0, 'Hello')
    worksheet.write('A2', 'wold')

    # 写行
    worksheet.write_row(2, 0, [1, 2, 3, 4, 5, 6])
    # 写列,其中列F需要大写
    worksheet.write_column('F2', ['a', 'b', 'c', 'd'])

    # 关闭工作簿
    workbook.close()

# 读取
def fileload(filename = '待读取.xlsx'):
    dataset = []
    workbook = xlrd.open_workbook(filename)
    table = workbook.sheets()[0]  # 获取一个工作表
    # table.row_values(i)  # 获取整行的值
    # table.col_values(i)  # 获取整列的值

    # 通过上方获取的工作表的内存对象，来获取行数和列数
    # nrows = table.nrows
    # ncols = table.ncols

    # 获取单元格
    # cell_A1 = table.cell(0, 0).value
    # cell_C4 = table.cell(2, 3).value

    # 使用行列索引获取单元格
    # cell_A1 = table.row(0)[0].value
    # cell_A2 = table.col(1)[0].value

    # 循环获取行
    for row in range(table.nrows):
        dataset.append(table.row_values(row))
    return dataset

print(fileload('D:\\book.xlsx'))
