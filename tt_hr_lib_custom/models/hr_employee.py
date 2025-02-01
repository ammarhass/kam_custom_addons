from odoo import models, fields, api, exceptions
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo.exceptions import UserError
from calendar import monthrange
import logging
global list_total_time
list_total_time = []
_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    hr_attendance_rule_id = fields.Many2one('hr.attendance.rule')

    @api.model
    def get_attendance_deduction(self, employee, payslip, gross):

        worked_days = payslip.worked_days
        partial_days = payslip.partial_days

        conf = self.env['ir.config_parameter'].sudo()
        if conf.get_param('tt_hr_lib.salary_base_duration') == 'fixed_duration' and \
                int(conf.get_param('tt_hr_lib.salary_base_duration_fix_days')) > 0 and not partial_days:
            days = int(conf.get_param('tt_hr_lib.salary_base_duration_fix_days'))
            day_salary = gross / days
        else:
            day_salary = gross / worked_days
        if conf.get_param('group_attendance_shifts'):
            res = self.get_attendance_deduction_on_shifts(employee, payslip, gross, day_salary)
            return res
        date_from = Date.from_string(payslip.date_from)
        date_to = Date.from_string(payslip.date_to)
        contract_id = payslip.contract_id
        contract_date_start = Date.from_string(contract_id.date_start)
        contract_date_end = Date.from_string(contract_id.date_end)
        if date_from < contract_date_start:
            date_from = contract_date_start
        if contract_date_end:
            if date_to > contract_date_end:
                date_to = contract_date_end
        current_date = date_from
        working_days = employee.resource_calendar_id

        if working_days:
            attendance_list = self.get_employee_attendance(employee, date_from, date_to)
            leave_list = self.get_employee_leaves(employee, date_from, date_to, working_days)
            official_holidays = self.get_official_holidays(date_from, date_to)
            attendance_rule = self.get_attendance_rule(employee)


            if attendance_rule:
                value = self.calculate_amount_of_attendance_delay(attendance_list,
                                                                  leave_list,
                                                                  official_holidays,
                                                                  attendance_rule,
                                                                  working_days,
                                                                  current_date,
                                                                  date_to, gross, day_salary)


                if value:
                    return -value
                else:
                    return 0


            else:
                print('There is no attendance for this Employee \n '
                      'OR There is no Attendance rule For this Employee')
                return 0

    # TODO Amount Of Attendance Delay
    def calculate_amount_of_attendance_delay(self, attendance_list, leave_list, official_holidays, attendance_rule,
                                             working_days,
                                             date_from, date_to,
                                             gross,day_salary):


        delay_occurrence = 0
        global delay_occurrence_shifts
        if date_from == date_to:
            delay_occurrence=delay_occurrence_shifts

        amount = 0
        d_to = self.increase_date(date_to)
        current_date = date_from
        total_time=0
        emp_work_minutes = 0
        month_work_minutes=0
        global list_total_time
        while current_date != d_to:

            day_name = current_date.strftime("%A")
            is_working_day = self.check_is_working_day(working_days, day_name)
            number_of_working_hours = self.get_number_of_working_hour(working_days, day_name)
            if number_of_working_hours:
                hour_salary = day_salary / number_of_working_hours - attendance_rule.break_time

            work_from_time = self.get_work_from_time(working_days, day_name) if is_working_day else timedelta(hours=0)
            leave_lines = self.check_is_leave_day(leave_list, current_date)
            is_official_holiday = self.check_is_official_holiday(official_holidays, current_date)
            first_check_in = self.get_first_check_in(attendance_list, current_date)
            if is_official_holiday:
                current_date = self.increase_date(current_date)
            elif is_working_day:

                if leave_lines:
                    if leave_lines['is_leave']:
                        current_date = self.increase_date(current_date)
                        continue
                    else:
                        work_from_time += timedelta(hours=leave_lines['hours'])

                if attendance_rule.flex_hours =='daily':
                        emp_work_minutes=0
                        day_att=attendance_list.filtered(lambda line :Datetime.from_string(line.check_in).date()==current_date)
                        day_number = self._get_day_number(day_name)
                        for xx in working_days.attendance_ids:
                            if int(xx.dayofweek)==day_number:
                                day_work_minutes = (xx.hour_to-xx.hour_from)*60
                                if day_work_minutes<0:
                                    day_work_minutes = day_work_minutes * -1
                        if day_att:
                            emp_work_minutes=((day_att.check_out - day_att.check_in).seconds)/60
                        diff =day_work_minutes-emp_work_minutes

                        if diff > 0:
                            attendance_rule_line = self.get_attendance_rule_line(attendance_rule,
                                                                                            timedelta(minutes=diff))

                            if attendance_rule_line:
                                if delay_occurrence == 0:

                                    amount += attendance_rule_line.one * day_salary

                                    delay_occurrence += 1
                                elif delay_occurrence == 1:
                                    amount += attendance_rule_line.two * day_salary

                                    delay_occurrence += 1
                                elif delay_occurrence > 1:
                                    amount += attendance_rule_line.three * day_salary

                                    delay_occurrence += 1

                        current_date = self.increase_date(current_date)

                elif attendance_rule.flex_hours =='monthly':

                    day_att = attendance_list.filtered(
                        lambda line: Datetime.from_string(line.check_in).date() == current_date)
                    day_number = self._get_day_number(day_name)
                    for xx in working_days.attendance_ids:
                        if int(xx.dayofweek) == day_number:
                            day_work_minutes = (xx.hour_to - xx.hour_from) * 60
                            if day_work_minutes < 0:
                                day_work_minutes = day_work_minutes * -1

                            month_work_minutes+=day_work_minutes
                    if day_att:
                        emp_work_minutes += ((day_att.check_out - day_att.check_in).seconds) / 60
                    current_date = self.increase_date(current_date)
                    if current_date == d_to:

                        diff = (attendance_rule.approved_month_work_minutes * 60)  - emp_work_minutes
                        hour_salary=gross/(month_work_minutes/60)

                        if diff > 0:
                            attendance_rule_line = self.get_attendance_rule_line(attendance_rule,
                                                                                            timedelta(minutes=diff))

                            if attendance_rule_line:
                                amount = attendance_rule_line.month_flex_deduction * hour_salary


                else:

                    if first_check_in:
                        grace_period = timedelta(minutes=attendance_rule.grace_period)
                        first_check_in = timedelta(hours=first_check_in.hour,
                                                   minutes=first_check_in.minute,
                                                   seconds=first_check_in.second)
                        if first_check_in <= work_from_time:
                            current_date = self.increase_date(current_date)

                            continue

                        else:

                            delay_time = first_check_in - work_from_time

                            if attendance_rule.type == 'daily':
                                if delay_time > grace_period:
                                    # global timeinmin
                                    # timeinmin += delay_time.seconds/60
                                    if not attendance_rule.hour_salary:
                                        attendance_rule_line = self.get_attendance_rule_line(attendance_rule, (delay_time - grace_period) * attendance_rule.number_of_minutes)
                                        if attendance_rule_line:
                                            if delay_occurrence == 0:
                                                amount += attendance_rule_line.one * day_salary
                                                delay_occurrence += 1
                                            elif delay_occurrence == 1:
                                                amount += attendance_rule_line.two * day_salary
                                                delay_occurrence += 1
                                            elif delay_occurrence > 1:
                                                amount += attendance_rule_line.three * day_salary
                                                delay_occurrence += 1
                                            current_date = self.increase_date(current_date)
                                        else:
                                            current_date = self.increase_date(current_date)
                                            print("No Matched Attendance Rule Line !")
                                    else:
                                        hours = (((delay_time - grace_period).seconds / 3600) * attendance_rule.number_of_minutes)
                                        if hours > number_of_working_hours:
                                            hours = number_of_working_hours
                                        amount += hour_salary * hours
                                        current_date = self.increase_date(current_date)
                                        print(amount)
                                else:
                                    current_date = self.increase_date(current_date)
                            elif attendance_rule.type == 'monthly':
                                total_time += delay_time.seconds/60
                                flag=True
                                for i,x in enumerate(list_total_time):
                                    if x[0] == attendance_rule:
                                        list_total_time[i] = (attendance_rule,x[1]+delay_time.seconds/60,x[2])
                                        flag=False
                                if flag==True:
                                    list_total_time.append((attendance_rule, delay_time.seconds/60,0))
                                for j,x in enumerate(list_total_time):
                                    if x[0] == attendance_rule:
                                        if x[1] > attendance_rule.max_period:
                                            del_time = x[1] - attendance_rule.max_period
                                            attendance_rule_line = self.get_attendance_rule_line(attendance_rule, timedelta(minutes=del_time))
                                            gg=0
                                            if attendance_rule_line:
                                                if x[2] == 0:
                                                    amount += attendance_rule_line.one * day_salary
                                                    list_total_time[j] = (x[0], x[1], x[2]+1)
                                                    gg=x[2]+1
                                                    # delay_occurrence += 1

                                                elif x[2] == 1:
                                                    amount += attendance_rule_line.two * day_salary
                                                    list_total_time[j] = (x[0], x[1], x[2] + 1)
                                                    gg=x[2] + 1

                                                    # delay_occurrence += 1
                                                elif x[2] > 1:
                                                    amount += attendance_rule_line.three * day_salary
                                                    list_total_time[j] = (x[0], x[1], x[2] + 1)
                                                    gg=x[2]+1
                                                    # delay_occurrence += 1
                                                current_date = self.increase_date(current_date)
                                            else:
                                                current_date = self.increase_date(current_date)
                                                print("No Matched Attendance Rule Line !")

                                            list_total_time[j] = (attendance_rule,x[1]-del_time,gg)

                                        else:
                                            current_date = self.increase_date(current_date)
                                            print("No Matched Attendance Rule Line !")
                    else:

                        attendance_rule_line = attendance_rule.line_ids[-1]
                        if attendance_rule_line:
                            if delay_occurrence == 0:
                                amount += attendance_rule_line.one * day_salary
                                delay_occurrence += 1
                            elif delay_occurrence == 1:
                                amount += attendance_rule_line.two * day_salary
                                delay_occurrence += 1
                            elif delay_occurrence > 1:
                                amount += attendance_rule_line.three * day_salary
                                delay_occurrence += 1
                            current_date = self.increase_date(current_date)
                        else:
                            current_date = self.increase_date(current_date)
                            print("No Matched Attendance Rule Line !")
            else:
                current_date = self.increase_date(current_date)

        delay_occurrence_shifts = delay_occurrence

        return amount

    # TODO Get Attendance Rule Line According Employee And Delay Time
    def get_attendance_rule_line(self, attendance_rule, delay_time):
        lines = attendance_rule.line_ids.filtered(lambda x: x.late == True)
        for line in lines:
            delay_from = timedelta(minutes=line.delay_from)
            delay_to = timedelta(minutes=line.delay_to)

            if delay_time > delay_from and delay_time <= delay_to:
                return line
        # if attendance_rule.line_ids:
        #     return attendance_rule.line_ids[-1]




    # TODO Get Attendance Rule According Employee
    def get_attendance_rule(self, employee):
        res = self.env['hr.attendance.rule'].search([('employee_ids', 'in', [employee.id])])
        if res:
            return res
        else:
            return False


    @api.model
    def get_overtime_hours(self, employee, ot_batch):

        date_from = Date.from_string(ot_batch.date_start)
        date_to = Date.from_string(ot_batch.date_end)
        working_days = employee.resource_calendar_id

        if working_days:
            attendance_list = self.get_employee_attendance_for_ot(employee, date_from, date_to)
            overtime_rule = self.get_overtime_rule(employee)
            official_holidays = self.get_official_holidays(date_from, date_to)

            if overtime_rule:

                hours = self.calculate_overtime_hours(attendance_list,
                                                       working_days,
                                                       overtime_rule,
                                                       official_holidays,
                                                       date_from,
                                                       date_to)

                if hours:
                    res={'hours':hours,'overtime_rule':overtime_rule}
                    attendance_list.set_overtime_checked()
                    return [res]
                else:
                    return False
            else:
                print('There is no attendance for this Employee \n '
                      'OR There is no Overtime rule For this Employee')
                return False


    def get_overtime_rule(self, employee):

        res = self.env['hr.overtime.rule'].search([('employee_ids', 'in', [employee.id])])

        if res:
            return res
        else:
            return False

