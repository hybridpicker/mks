import xlwt
import datetime

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from students.models import Student, Parent

# Create your views here.
@login_required(login_url='/team/login/')
@staff_member_required
def export_students_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="students.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Students')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Anmeldedatum', 'Eltern Vorname', 'Eltern Nachname', 
               'Vorname', 'Nachname', 'Email', 'Geburtstag', 'Instrument', 
               'Straße','Hausnummer', 'PLZ', 'Ort', 'Telefon',
               'Anmerkung']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    font_style.num_format_str = 'dd/mm/yyyy'

    rows = Student.objects.all().values_list('start_date', 'parent__first_name', 'parent__last_name', 'first_name', 
                                            'last_name', 'parent__email', 'birth_date', 'subject__subject',
                                            'parent__adress_line', 'parent__house_number', 'parent__postal_code', 
                                            'parent__city', 'parent__phone', 'note')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.datetime):
                ws.write(row_num, col_num, row[col_num], style1)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response