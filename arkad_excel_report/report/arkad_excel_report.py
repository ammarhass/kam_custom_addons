from odoo import http
from odoo.http import request
from ast import literal_eval
from collections import defaultdict

from datetime import datetime
import io
import xlsxwriter

from odoo.exceptions import ValidationError


class XlsxAnalyticReprot(http.Controller):

    @http.route('/analytic/excel/report/<string:analytic_ids>', type='http', auth='user', csrf=False)
    def download_excel_report(self, analytic_ids):

        analytic_ids = request.env['account.analytic.account'].browse(literal_eval(analytic_ids))
        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', request.env['account.move'].get_purchase_types())])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids_all = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids = request.env['account.move'].browse(move_ids_all)
        accounts = move_ids.mapped("invoice_line_ids").mapped("account_id").filtered(lambda x: x.remove_from_report != True)
        grouped_records = {}
        amount_total = sum(move_ids.mapped('amount_total'))
        for account in accounts:
            rec = move_ids.filtered(lambda x: x.invoice_line_ids.filtered(lambda l: l.account_id == account))
            grouped_records[account] = (rec)
        moves = grouped_records

        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', ['entry']), ('move_id.is_item_expenses', '=', True)])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids_entry = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids_entry = request.env['account.move'].browse(move_ids_entry)
        accounts_entry = move_ids_entry.mapped("invoice_line_ids").mapped("account_id").filtered(lambda x: x.remove_from_report != True)
        grouped_records = {}
        amount_total += sum(move_ids_entry.mapped('amount_total'))
        for account in accounts_entry:
            rec = move_ids_entry.filtered(lambda x: x.invoice_line_ids.filtered(lambda l: l.account_id == account))
            grouped_records[account] = (rec)
        moves_entry = grouped_records
        for key in moves_entry:
            if key in moves:
                moves[key] += moves_entry[key]

        if len(analytic_ids) > 1:
            raise ValidationError("Please select only one analytic account")

        total_amount = 0.0
        total_amount_residual = 0.0
        total_paid = 0.0
        total_item_amount = 0.0

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Analytic')
        worksheet.set_column(0, 14, 26)
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 15, 'border': 1, 'bg_color': '#808080'})

        worksheet.merge_range('A1:F1', analytic_ids.name, head)
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        string_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center'})
        currency_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})

        headers = ['الاجمالي', 'مستلزمات البند', 'المستحق للمقاولين', 'المدفوع', 'المديونية', 'وصف البند']
        for col_num, header in enumerate(headers):
            worksheet.write(1, col_num, header, header_format)

        row_num = 2
        for key in moves:
            worksheet.write(row_num, 0, sum(
                moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_total')) + sum(
                moves[key].filtered(lambda move: move.is_item_expenses == True).mapped('amount_total')),
                            currency_format)
            worksheet.write(row_num, 1, sum(
                moves[key].filtered(lambda move: move.is_item_expenses == True).mapped('amount_total')),
                            currency_format)
            worksheet.write(row_num, 2, sum(
                moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_residual')),
                            currency_format)
            worksheet.write(row_num, 3, sum(
                moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_total')) - sum(
                moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_residual')),
                            currency_format)
            worksheet.write(row_num, 4,
                            sum(moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_total')),
                            currency_format)
            worksheet.write(row_num, 5, 'اسم مقاول الباطن: ' + moves[key][0].ref if moves[key][0].ref else ' ',
                            string_format)
            row_num += 1
        for key in moves:
            total_amount += sum(moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_total'))
            total_amount_residual += sum(
                moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_residual'))
            total_paid = total_amount - total_amount_residual
            total_item_amount += sum(
                moves[key].filtered(lambda move: move.is_item_expenses == True).mapped('amount_total'))

        worksheet.write(row_num, 5, "الاجمالي", total_format)
        worksheet.write(row_num, 4, total_amount,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 3, total_paid,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 2, total_amount_residual,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))

        worksheet.write(row_num, 1, total_item_amount,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 0, total_item_amount + total_amount,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 5, "مصروفات إضافية", head)
        row_num += 1

        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', ['entry']), ('move_id.is_item_expenses', '!=', True)])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids = request.env['account.move'].browse(move_ids)
        other_total_amount = sum(move_ids.mapped('amount_total'))

        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})
        headers = ['', '', '', 'المبلغ', 'التاريخ', 'البيان']
        for col_num, header in enumerate(headers):
            worksheet.write(row_num, col_num, header, header_format)

        row_num += 1

        for move in move_ids:
            worksheet.write(row_num, 0, '', string_format)
            worksheet.write(row_num, 1, '', string_format)
            worksheet.write(row_num, 2, '', string_format)
            worksheet.write(row_num, 3, move.amount_total, currency_format)
            worksheet.write_datetime(row_num, 4, move.date, date_format)
            worksheet.write(row_num, 5, move.ref, string_format)
            row_num += 1
        worksheet.write(row_num, 5, "إجمالي المصروفات اﻷضافية", total_format)
        worksheet.write(row_num, 4, "", total_format)
        worksheet.write(row_num, 3, other_total_amount,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 2, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 1, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 0, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        row_num += 1

        project_total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})

        worksheet.merge_range(row_num, 5, row_num + 1, 5, "إجمالي المنصرف على المشروع", project_total_format)
        worksheet.merge_range(row_num, 2, row_num, 4, 'إجمالي قيمة المشروع', workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
        worksheet.write(row_num, 1, 'المدفوع على المشروع', project_total_format)
        worksheet.write(row_num, 0, 'الملزم بالدفع', project_total_format)
        # worksheet.write(row_num, 0, 'الملزم بالدفع', project_total_format)

        row_num += 1
        worksheet.merge_range(row_num, 4, row_num, 2, amount_total + other_total_amount, workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        worksheet.write(row_num, 1, total_paid + other_total_amount + total_item_amount, workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        worksheet.write(row_num, 0, total_amount_residual, workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))

        workbook.close()
        output.seek(0)
        file_name = f'{analytic_ids[0].name}.xlsx'  # Ensure the file has .xlsx extension
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{file_name}"')
            ]
        )

    @http.route('/analytic/excel/report/vendor/<string:analytic_ids>', type='http', auth='user', csrf=False)
    def download_excel_report_vendor(self, analytic_ids):

        analytic_ids = request.env['account.analytic.account'].browse(literal_eval(analytic_ids))
        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', request.env['account.move'].get_purchase_types())])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids_all = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids = request.env['account.move'].browse(move_ids_all)
        accounts = move_ids.mapped("invoice_line_ids").mapped("account_id").filtered(lambda x: x.remove_from_report != True)
        grouped_records = {}
        amount_total = sum(move_ids.mapped('amount_total'))
        for account in accounts:
            rec = move_ids.filtered(lambda x: x.invoice_line_ids.filtered(lambda l: l.account_id == account))
            grouped_records[account] = (rec)
        moves = grouped_records

        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', ['entry']), ('move_id.is_item_expenses', '=', True)])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids_entry = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids_entry = request.env['account.move'].browse(move_ids_entry)
        accounts_entry = move_ids_entry.mapped("invoice_line_ids").mapped("account_id").filtered(lambda x: x.remove_from_report != True)
        grouped_records = {}
        amount_total += sum(move_ids_entry.mapped('amount_total'))
        for account in accounts_entry:
            rec = move_ids_entry.filtered(lambda x: x.invoice_line_ids.filtered(lambda l: l.account_id == account))
            grouped_records[account] = (rec)
        moves_entry = grouped_records
        for key in moves_entry:
            if key in moves:
                moves[key] += moves_entry[key]

        if len(analytic_ids) > 1:
            raise ValidationError("Please select only one analytic account")

        total_amount = 0.0
        total_amount_residual = 0.0
        total_paid = 0.0
        total_item_amount = 0.0
        total_is_expenses = 0.0

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Analytic')
        worksheet.set_column(0, 14, 26)
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 15, 'border': 1, 'bg_color': '#808080'})

        worksheet.merge_range('A1:H1', analytic_ids.name, head)
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        string_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center'})
        currency_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})
        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})

        headers = ['الإجمالي' ,'مستلزمات البند', 'المستحق للمقاولين', 'المدفوع', 'المديونية', 'التاريخ', 'المقاول', 'وصف البند']
        for col_num, header in enumerate(headers):
            worksheet.write(1, col_num, header, header_format)

        row_num = 2
        for key in moves.keys():
            worksheet.write(row_num, 7, key.name, string_format)
            for value in moves.get(key).filtered(lambda x: x.is_item_expenses != True):
                worksheet.write(row_num, 0, '',
                                currency_format)
                worksheet.write(row_num, 1, '',
                                currency_format)
                worksheet.write(row_num, 2, value.amount_residual, currency_format)
                worksheet.write(row_num, 3, value.amount_total - value.amount_residual, currency_format)

                worksheet.write(row_num, 4, value.amount_total, currency_format)
                worksheet.write(row_num, 5, value.invoice_date, date_format)
                worksheet.write(row_num, 6, value.partner_id.name, string_format)
                row_num += 1

            if not moves.get(key).filtered(lambda x: x.is_item_expenses != True):
                    worksheet.write(row_num, 0, '',
                                    currency_format)
                    worksheet.write(row_num, 1, '',
                                    currency_format)
                    worksheet.write(row_num, 2, '', currency_format)
                    worksheet.write(row_num, 3, '', currency_format)

                    worksheet.write(row_num, 4, '', currency_format)
                    worksheet.write(row_num, 5, '', date_format)
                    worksheet.write(row_num, 6, '', string_format)
                    worksheet.write(row_num, 7, key.name, string_format)
                    row_num += 1

            worksheet.write(row_num, 0, sum(moves.get(key).filtered(lambda x: x.is_item_expenses == True).mapped(
                'amount_total')) + sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total')),
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 1, sum(moves.get(key).filtered(lambda x: x.is_item_expenses == True).mapped(
                'amount_total')),
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 2, sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped(
                'amount_residual')),
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 3, sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped(
                'amount_total')) - sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_residual')),
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))

            worksheet.write(row_num, 4,
                            sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total')),
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 5, '',
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 6, '',
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 7, 'الإجمالي', total_format)
            row_num += 1
        for key in moves:
            total_amount += sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total'))
            total_paid += sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total')) - sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_residual'))
            total_amount_residual += sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_residual'))
            total_is_expenses += sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses == True).mapped('amount_total'))

        worksheet.write(row_num, 0, total_amount + total_is_expenses,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 1, total_is_expenses,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 2, total_amount_residual, workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 3, total_paid,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))

        worksheet.write(row_num, 4, total_amount,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 5, '',
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 6, '',
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 7, 'إجمالي البنود', total_format)
        row_num += 1

        worksheet.merge_range(row_num, 0, row_num, 7, "مصروفات إضافية", head)
        row_num += 1

        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', ['entry']), ('move_id.is_item_expenses', '!=', True)])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids = request.env['account.move'].browse(move_ids)
        other_total_amount = sum(move_ids.mapped('amount_total'))

        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})
        headers = ['' ,'', '', '', '', 'المبلغ', 'التاريخ', 'البيان']
        for col_num, header in enumerate(headers):
            worksheet.write(row_num, col_num, header, header_format)

        row_num += 1
        for move in move_ids:
            worksheet.write(row_num, 0, '', string_format)
            worksheet.write(row_num, 1, '', string_format)
            worksheet.write(row_num, 2, '', string_format)
            worksheet.write(row_num, 3, '', string_format)
            worksheet.write(row_num, 4, '', string_format)
            worksheet.write(row_num, 5, move.amount_total, currency_format)
            worksheet.write_datetime(row_num, 6, move.date, date_format)
            worksheet.write(row_num, 7, move.ref, string_format)
            row_num += 1
        worksheet.write(row_num, 7, "إجمالي المصروفات اﻷضافية", total_format)
        worksheet.write(row_num, 6, "", total_format)
        worksheet.write(row_num, 5, other_total_amount,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 4, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 3, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 2, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 1, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 0, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        row_num += 1

        project_total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})

        worksheet.merge_range(row_num, 7, row_num + 1, 7, "إجمالي المنصرف على المشروع", project_total_format)
        worksheet.merge_range(row_num, 4, row_num, 6, 'إجمالي قيمة المشروع', workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
        worksheet.merge_range(row_num, 2, row_num, 3, 'المدفوع على المشروع', workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
        worksheet.merge_range(row_num, 0, row_num, 1,'الملزم بالدفع', workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))

        row_num += 1
        worksheet.merge_range(row_num, 4, row_num, 6, amount_total + other_total_amount, workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        worksheet.merge_range(row_num, 2, row_num, 3, total_paid + other_total_amount + total_is_expenses, workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        worksheet.merge_range(row_num, 0, row_num, 1, total_amount_residual, workbook.add_format(
            {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))


        # for key in moves:
        #     total_amount += sum(moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_total'))
        #     total_amount_residual += sum(moves[key].filtered(lambda move: move.is_item_expenses != True).mapped('amount_residual'))
        #     total_paid = total_amount - total_amount_residual
        #     total_item_amount += sum(moves[key].filtered(lambda move: move.is_item_expenses == True).mapped('amount_total'))
        #
        # worksheet.write(row_num, 5, "الاجمالي", total_format)
        # worksheet.write(row_num, 4, total_amount, workbook.add_format({'num_format': '#,##0.00','border': 1, 'bg_color': '#D3D3D3'}))
        # worksheet.write(row_num, 3, total_paid,
        #                 workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        # worksheet.write(row_num, 2, total_amount_residual,
        #                 workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        #
        # worksheet.write(row_num, 1, total_item_amount,
        #                 workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        # worksheet.write(row_num, 0, total_item_amount + total_amount,
        #                 workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        # row_num += 1
        # worksheet.merge_range(row_num, 0, row_num, 5, "مصروفات إضافية", head)
        # row_num += 1
        #
        # query = request.env['account.move.line']._search([('move_id.move_type', 'in', ['entry']), ('move_id.is_item_expenses', '!=', True)])
        # query.order = None
        # query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        # query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        # request._cr.execute(query_string, query_param)
        # move_ids = [line.get('move_id') for line in request._cr.dictfetchall()]
        # move_ids = request.env['account.move'].browse(move_ids)
        # other_total_amount = sum(move_ids.mapped('amount_total'))
        #
        # date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})
        # headers = [ '','', '', 'المبلغ', 'التاريخ', 'البيان']
        # for col_num, header in enumerate(headers):
        #     worksheet.write(row_num, col_num, header, header_format)
        #
        # row_num += 1
        #
        # for move in move_ids:
        #     worksheet.write(row_num, 0, '', string_format)
        #     worksheet.write(row_num, 1, '', string_format)
        #     worksheet.write(row_num, 2, '', string_format)
        #     worksheet.write(row_num, 3, move.amount_total, currency_format)
        #     worksheet.write_datetime(row_num, 4, move.date, date_format)
        #     worksheet.write(row_num, 5, move.ref, string_format)
        #     row_num += 1
        # worksheet.write(row_num, 5, "إجمالي المصروفات اﻷضافية", total_format)
        # worksheet.write(row_num, 4, "", total_format)
        # worksheet.write(row_num, 3, other_total_amount,
        #                 workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        # worksheet.write(row_num, 2, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        # worksheet.write(row_num, 1, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        # worksheet.write(row_num, 0, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        # row_num += 1
        #
        # project_total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})
        #
        # worksheet.merge_range(row_num, 5, row_num + 1, 5, "إجمالي المنصرف على المشروع", project_total_format)
        # worksheet.merge_range(row_num, 2, row_num, 4, 'إجمالي قيمة المشروع', workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
        # worksheet.write(row_num, 1, 'المدفوع على المشروع', project_total_format)
        # worksheet.write(row_num, 0, 'الملزم بالدفع', project_total_format)
        # # worksheet.write(row_num, 0, 'الملزم بالدفع', project_total_format)
        #
        # row_num += 1
        # worksheet.merge_range(row_num, 4, row_num, 2, amount_total + other_total_amount, workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        # worksheet.write(row_num, 1, total_paid + other_total_amount + total_item_amount, workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        # worksheet.write(row_num, 0, total_amount_residual, workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))

        workbook.close()
        output.seek(0)
        file_name = f'{analytic_ids[0].name}.xlsx'  # Ensure the file has .xlsx extension
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{file_name}"')
            ]
        )

    @http.route('/analytic/excel/account/<string:analytic_ids>', type='http', auth='user', csrf=False)
    def download_excel_report_partner(self, analytic_ids, **kwargs):

        analytic_ids = request.env['account.analytic.account'].browse(literal_eval(analytic_ids))
        account_id = int(kwargs.get('account_id'))
        account_name = request.env['account.account'].browse(account_id).name

        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', request.env['account.move'].get_purchase_types()), ('account_id', '=', account_id)])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids_all = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids = request.env['account.move'].browse(move_ids_all)
        partners = move_ids.mapped("partner_id")
        grouped_records = {}
        amount_total = sum(move_ids.mapped('amount_total'))
        for partner in partners:
            rec = move_ids.filtered(lambda x: x.partner_id == partner)
            grouped_records[partner] = (rec)
        moves = grouped_records

        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', ['entry']), ('move_id.is_item_expenses', '=', True), ('account_id', '=', account_id)])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids_entry = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids_entry = request.env['account.move'].browse(move_ids_entry)
        accounts_entry = move_ids_entry.mapped("invoice_line_ids").mapped("account_id")
        grouped_records = {}
        amount_total += sum(move_ids_entry.mapped('amount_total'))
        for account in accounts_entry:
            rec = move_ids_entry.filtered(lambda x: x.invoice_line_ids.filtered(lambda l: l.account_id == account))
            grouped_records[account] = (rec)
        moves_entry = grouped_records
        for key in moves_entry:
            if key in moves:
                moves[key] += moves_entry[key]

        if len(analytic_ids) > 1:
            raise ValidationError("Please select only one analytic account")

        total_amount = 0.0
        total_amount_residual = 0.0
        total_paid = 0.0
        total_item_amount = 0.0
        total_is_expenses = 0.0

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Analytic')
        worksheet.set_column(0, 14, 26)
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 15, 'border': 1, 'bg_color': '#808080'})

        worksheet.merge_range('A1:H1', account_name, head)
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        string_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center'})
        currency_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})
        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})

        headers = ['الإجمالي' ,'مستلزمات البند', 'المستحق للمقاول', 'المدفوع', 'المديونية', 'التاريخ', 'الفاتورة', 'المقاول']

        for col_num, header in enumerate(headers):
            worksheet.write(1, col_num, header, header_format)

        row_num = 2
        for key in moves.keys():
            worksheet.write(row_num, 7, key.name, string_format)
            for value in moves.get(key).filtered(lambda x: x.is_item_expenses != True):
                worksheet.write(row_num, 0, '',
                                currency_format)
                worksheet.write(row_num, 1, '',
                                currency_format)
                worksheet.write(row_num, 2, value.amount_residual, currency_format)
                worksheet.write(row_num, 3, value.amount_total - value.amount_residual, currency_format)

                worksheet.write(row_num, 4, value.amount_total, currency_format)
                worksheet.write(row_num, 5, value.invoice_date, date_format)
                worksheet.write(row_num, 6, value.partner_id.name, string_format)
                row_num += 1
            if moves.get(key).filtered(lambda x: x.is_item_expenses != True):

                worksheet.write(row_num, 0, sum(moves.get(key).filtered(lambda x: x.is_item_expenses == True).mapped(
                    'amount_total')) + sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total')),
                                workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
                worksheet.write(row_num, 1, sum(moves.get(key).filtered(lambda x: x.is_item_expenses == True).mapped(
                    'amount_total')),
                                workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
                worksheet.write(row_num, 2, sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped(
                    'amount_residual')),
                                workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
                worksheet.write(row_num, 3, sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped(
                    'amount_total')) - sum(
                    moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_residual')),
                                workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))

                worksheet.write(row_num, 4,
                                sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total')),
                                workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
                worksheet.write(row_num, 5, '',
                                workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
                worksheet.write(row_num, 6, '',
                                workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
                worksheet.write(row_num, 7, 'الإجمالي', total_format)
                row_num += 1
        for key in moves:
            total_amount += sum(moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total'))
            total_paid += sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_total')) - sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_residual'))
            total_amount_residual += sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses != True).mapped('amount_residual'))
            total_is_expenses += sum(
                moves.get(key).filtered(lambda x: x.is_item_expenses == True).mapped('amount_total'))

        worksheet.write(row_num, 0, total_amount + total_is_expenses,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 1, total_is_expenses,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 2, total_amount_residual, workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 3, total_paid,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))

        worksheet.write(row_num, 4, total_amount,
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 5, '',
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 6, '',
                        workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
        worksheet.write(row_num, 7, 'إجمالي البند', total_format)
        row_num += 1



        query = request.env['account.move.line']._search(
            [('move_id.move_type', 'in', ['entry']), ('move_id.is_item_expenses', '!=', True), ('account_id', '=', account_id)])
        query.order = None
        query.add_where('analytic_distribution ? %s', [str(analytic_ids.id)])
        query_string, query_param = query.select('DISTINCT account_move_line.move_id')
        request._cr.execute(query_string, query_param)
        move_ids = [line.get('move_id') for line in request._cr.dictfetchall()]
        move_ids = request.env['account.move'].browse(move_ids)
        other_total_amount = sum(move_ids.mapped('amount_total'))

        if move_ids:
            worksheet.merge_range(row_num, 0, row_num, 7, "مصروفات إضافية", head)
            row_num += 1

            date_format = workbook.add_format({'num_format': 'yyyy/mm/dd'})
            headers = ['' ,'', '', '', '', 'المبلغ', 'التاريخ', 'البيان']
            for col_num, header in enumerate(headers):
                worksheet.write(row_num, col_num, header, header_format)

            row_num += 1
        for move in move_ids:
            worksheet.write(row_num, 0, '', string_format)
            worksheet.write(row_num, 1, '', string_format)
            worksheet.write(row_num, 2, '', string_format)
            worksheet.write(row_num, 3, '', string_format)
            worksheet.write(row_num, 4, '', string_format)
            worksheet.write(row_num, 5, move.amount_total, currency_format)
            worksheet.write_datetime(row_num, 6, move.date, date_format)
            worksheet.write(row_num, 7, move.ref, string_format)
            row_num += 1
        if move_ids:
            worksheet.write(row_num, 7, "إجمالي المصروفات اﻷضافية", total_format)
            worksheet.write(row_num, 6, "", total_format)
            worksheet.write(row_num, 5, other_total_amount,
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 4, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 3, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 2, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 1, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
            worksheet.write(row_num, 0, '', workbook.add_format({'border': 1, 'bg_color': '#D3D3D3'}))
        # row_num += 1
        #
        # project_total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3'})
        #
        # worksheet.merge_range(row_num, 7, row_num + 1, 7, "إجمالي المنصرف على المشروع", project_total_format)
        # worksheet.merge_range(row_num, 4, row_num, 6, 'إجمالي قيمة المشروع', workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
        # worksheet.merge_range(row_num, 2, row_num, 3, 'المدفوع على المشروع', workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
        # worksheet.merge_range(row_num, 0, row_num, 1,'الملزم بالدفع', workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
        #
        # row_num += 1
        # worksheet.merge_range(row_num, 4, row_num, 6, amount_total + other_total_amount, workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        # worksheet.merge_range(row_num, 2, row_num, 3, total_paid + other_total_amount + total_is_expenses, workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))
        # worksheet.merge_range(row_num, 0, row_num, 1, total_amount_residual, workbook.add_format(
        #     {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'num_format': '#,##0.00'}))

        workbook.close()
        output.seek(0)
        file_name = f'{analytic_ids[0].name}.xlsx'  # Ensure the file has .xlsx extension
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{file_name}"')
            ]
        )

    @http.route('/analytic/excel/report/vendor/details/<string:vendor_id>', type='http', auth='user', csrf=False)
    def download_excel_report_vendor_details(self, vendor_id, **kwargs):
        vendor_id = request.env['res.partner'].browse(literal_eval(vendor_id))
        analytics = request.env['account.analytic.account'].search([('company_id.id', '=', 110)])
        vendor_name = vendor_id.name
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Analytic')
        worksheet.set_column(0, 14, 26)
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': 15, 'border': 1, 'bg_color': '#808080'})

        worksheet.merge_range('A1:D1', vendor_name, head)
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center'})
        string_format = workbook.add_format({'bold': True, 'border': 1, 'align': 'center'})
        currency_format = workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'align': 'center'})
        total_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'})
        date_format = workbook.add_format({'num_format': 'yyyy/mm/dd', 'align': 'center'})

        headers = ['المديونية', 'المدفوع', 'إجمالي المستخلص', 'المشروع']
        for col_num, header in enumerate(headers):
            worksheet.write(1, col_num, header, header_format)
        row_num = 2
        total_amount = 0.0
        total_residual = 0.0
        total_paid = 0.0
        for analytic in analytics:
            query = request.env['account.move.line']._search(
                [('move_id.move_type', 'in', request.env['account.move'].get_purchase_types())])
            query.order = None
            query.add_where('analytic_distribution ? %s', [str(analytic.id)])
            query_string, query_param = query.select('DISTINCT account_move_line.move_id')
            request._cr.execute(query_string, query_param)
            move_ids = [line.get('move_id') for line in request._cr.dictfetchall()]
            move_ids = request.env['account.move'].browse(move_ids)
            move_ids = move_ids.filtered(lambda x: x.partner_id.id == vendor_id.id)
            amount_total = sum(move_ids.mapped('amount_total'))
            total_amount += amount_total
            amount_residual = sum(move_ids.mapped('amount_residual'))
            total_residual += amount_residual
            amount_paid = amount_total - amount_residual
            total_paid += amount_paid
            if amount_total > 0:
                worksheet.merge_range(row_num, 3, row_num + 1, 3, analytic.name, string_format)
                worksheet.merge_range(row_num, 2, row_num + 1, 2, amount_total, currency_format)
                worksheet.merge_range(row_num, 1, row_num + 1, 1, amount_paid, currency_format)
                worksheet.merge_range(row_num, 0, row_num + 1, 0, amount_residual, currency_format)
                row_num += 2
            worksheet.merge_range(row_num, 3, row_num + 1, 3, 'الإجمالي',
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
            worksheet.merge_range(row_num, 2, row_num + 1, 2, total_amount,
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
            worksheet.merge_range(row_num, 1, row_num + 1, 1, total_paid,
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))
            worksheet.merge_range(row_num, 0, row_num + 1, 0, total_residual,
                            workbook.add_format({'num_format': '#,##0.00', 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center'}))





        workbook.close()
        output.seek(0)
        file_name = 'vendor_report' + '.xls'
        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{file_name}"')
            ]
        )



