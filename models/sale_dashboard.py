from odoo import models, fields, api, _
from datetime import timedelta, datetime, date, time
from odoo.exceptions import AccessError
from dateutil.relativedelta import relativedelta
from odoo.http import request


menit = datetime.now().strftime("%H")
menit = int(menit) - 1

jam = datetime.now().strftime("%H")
jam = int(jam) + 7

tgl = datetime.now().strftime("%d")
tgl = int(tgl) - 1

bln = datetime.now().strftime("%m")
bln = int(bln) - 1

name_bulan = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
class SaleDashboard(models.Model):
    _inherit = 'sale.order'

    @api.model
    def get_orders_chart(self, option,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
        apa = 0
        order = []
        today = []
        jam1 = []
        hitung = 0
        if option == 'pos_dayly_sales':
            count = []
            name = 'Every DAYs'
            self._cr.execute("SELECT sale_order.date_order , sale_order.amount_total from sale_order WHERE sale_order.invoice_status = 'to invoice' AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ORDER BY sale_order.date_order, sale_order.amount_total")
            result = self._cr.dictfetchall()
            # raise AccessErro  r(str(result))
            for record in result:
                if record.get('date_order').strftime("%d/%m/%Y") not in jam1: 
                    if apa != 0:
                        order.append(apa)
                    apa = apa * 0 
                    today.append(record.get('date_order').strftime("%d/%m/%Y"))
                    jam1.append(record.get('date_order').strftime("%d/%m/%Y"))
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                        order.append(apa)
                else:
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                       order.append(apa)
        elif option == 'pos_monthly_sales' and date2:
            count = []
            name = 'Every MONTHs'
            self._cr.execute("SELECT extract(month from date_order) as date_order , extract(year from date_order) as year ,sale_order.amount_total from sale_order WHERE sale_order.invoice_status = 'to invoice' AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' ORDER BY sale_order.date_order, sale_order.amount_total")
            result = self._cr.dictfetchall()
            for record in result:
                if record.get('date_order') not in jam1: 
                    if apa != 0:
                        order.append(apa)
                    apa = apa * 0 
                    bulan = name_bulan[int(record.get('date_order')-1)]
                    today.append(str(bulan) + "-" +str(int(record.get("year"))))
                    jam1.append(record.get('date_order'))
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                        order.append(apa)
                else:
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                       order.append(apa) 

        elif option == 'pos_monthly_sales':
            count = []
            name = 'Every MONTHs'
            self._cr.execute("SELECT extract(month from date_order) as date_order , extract(year from date_order) as year, sale_order.amount_total from sale_order WHERE sale_order.invoice_status = 'to invoice' AND date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ORDER BY sale_order.date_order, sale_order.amount_total")
            result = self._cr.dictfetchall()
            for record in result:
                if record.get('date_order') not in jam1: 
                    if apa != 0:
                        order.append(apa)
                    apa = apa * 0 
                    bulan = name_bulan[int(record.get('date_order')-1)]
                    today.append(bulan)
                    jam1.append(record.get('date_order'))
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                        order.append(apa)
                else:
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                       order.append(apa) 

        elif option == 'pos_year_sales':
            count = []
            name = 'Every YEARs'
            self._cr.execute("SELECT sale_order.date_order , sale_order.amount_total from sale_order WHERE sale_order.invoice_status = 'to invoice' AND date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ORDER BY sale_order.date_order, sale_order.amount_total")
            result = self._cr.dictfetchall()
            # raise AccessError(str(result))
            for record in result:
                if record.get('date_order').strftime("%Y") not in jam1: 
                    if apa != 0:
                        order.append(apa)
                    apa = apa * 0 
                    today.append(record.get('date_order').strftime("%Y"))
                    jam1.append(record.get('date_order').strftime("%Y"))
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                        order.append(apa)
                else:
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                       order.append(apa)

        if date2 and not option:
            count = []
            name = 'Jumlah Order'
            self._cr.execute("SELECT sale_order.date_order , sale_order.amount_total from sale_order WHERE sale_order.invoice_status = 'to invoice' AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' ORDER BY sale_order.date_order, sale_order.amount_total")
            result = self._cr.dictfetchall()
            # raise AccessError(str(result))
            for record in result:
                if record.get('date_order').strftime("%d/%m/%Y") not in jam1: 
                    if apa != 0:
                        order.append(apa)
                    apa = apa * 0 
                    today.append(record.get('date_order').strftime("%d/%m/%Y"))
                    jam1.append(record.get('date_order').strftime("%d/%m/%Y"))
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                        order.append(apa)
                else:
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                       order.append(apa)

        elif date1 and not option:
            count = []
            name = 'Jumlah Order'
            self._cr.execute("SELECT sale_order.date_order , sale_order.amount_total from sale_order WHERE sale_order.invoice_status = 'to invoice' AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ORDER BY sale_order.date_order, sale_order.amount_total")
            result = self._cr.dictfetchall()
            # raise AccessError(str(result))
            for record in result:
                if record.get('date_order').strftime("%d/%m/%Y") not in jam1: 
                    if apa != 0:
                        order.append(apa)
                    apa = apa * 0 
                    today.append(record.get('date_order').strftime("%d/%m/%Y"))
                    jam1.append(record.get('date_order').strftime("%d/%m/%Y"))
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                        order.append(apa)
                else:
                    hitung += 1
                    apa += float(record.get('amount_total'))
                    if hitung == len(result):
                       order.append(apa)

        final = [order, today, name]
        return final

    @api.model
    def get_product_chart(self, option,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
        order = []
        today = []
        product = []
        count = 0
        hitung = 0
        jamku = []
        if option == 'pos_dayly_sales':
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'pos_monthly_sales':
            name = "monthly"
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'pos_year_sales':
            name = "yearly"
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        if date2:
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif date1:
            self._cr.execute("SELECT product_category.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                get_name = self.env['product.template'].search([('categ_id.id', '=', x.get('id'))])[-1]
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(str(get_name.categ_id.display_name)))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        final = [order, today, name]
        return final

    @api.model
    def get_top_product_list(self, option, date1, date2):
        order = []
        today = []
        product = []
        count = 0
        hitung = 0
        jamku = []
        name = ""
        if option == 'top_sales_product_today':
            self._cr.execute("SELECT product_template.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id,product_template.name ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            name = "dayly"
            for x in result: 
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(x.get('name')))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'top_sales_product_month':
            name = "monthly"
            self._cr.execute("SELECT product_template.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id,product_template.name ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(x.get('name')))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)

        elif option == 'top_sales_product_year':
            name = "year"
            self._cr.execute("SELECT product_template.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit))  +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id,product_template.name ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(x.get('name')))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)
        if date2:
            name = "year"
            self._cr.execute("SELECT product_template.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(date1)  +"' AND date_order < '"+str(date2)+"' GROUP BY product_category.id,product_template.name ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(x.get('name')))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)
        elif date1:
            name = "year"
            self._cr.execute("SELECT product_template.name , product_category.id , SUM(sale_order_line.product_uom_qty) as qty FROM sale_order_line JOIN sale_order ON sale_order_line.order_id = sale_order.id JOIN product_product ON sale_order_line.product_id = product_product.id JOIN product_template ON product_product.product_tmpl_id = product_template.id JOIN product_category ON product_category.id = product_template.categ_id WHERE sale_order.state != 'cancel' AND sale_order.date_order >= '"+ str(date1)  +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY product_category.id,product_template.name ORDER BY qty DESC LIMIT 5")
            result = self._cr.dictfetchall()
            for x in result: 
                if x.get('name') not in jamku:
                    if count != 0:
                        order.append(count)
                        count = 0
                    today.append(str(x.get('name')))
                    jamku.append(x.get('name'))
                    count += x.get('qty')
                    hitung += 1
                    if hitung == len(result):
                         order.append(count)
                else:
                    count += x.get('qty')
                    hitung +=1
                    if hitung == len(result):
                         order.append(count)
        final = [order, today, name]
        return final

    @api.model
    def get_teams_chart(self, option, date1, date2):
        order = []
        today = []
        count = 0
        name = 'Total Seller And opportunities Amount'
        if option == "pos_dayly_sales_team":
            self._cr.execute("SELECT crm_team.id,crm_team.name, crm_team.team_type, SUM(sale_order.amount_total) as amount_total FROM crm_team LEFT OUTER join sale_order on sale_order.team_id = crm_team.id AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND sale_order.date_order < '"+str(datetime.now() + timedelta(hours=7))+"' WHERE active = True GROUP BY crm_team.id, crm_team.name, crm_team.team_type ORDER BY crm_team.name")
            docs1 = self._cr.dictfetchall()
            self._cr.execute("SELECT crm_team.id, crm_team.name, SUM(pos_order.amount_total) as amount_total_pos FROM crm_team LEFT OUTER join pos_config on pos_config.crm_team_id = crm_team.id LEFT OUTER join pos_session on pos_session.config_id = pos_config.id LEFT OUTER join pos_order on pos_order.session_id = pos_session.id WHERE pos_order.date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND pos_order.date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY crm_team.id, crm_team.name")
            b1 = self._cr.dictfetchall()
            for x in docs1:
                if str(x.get('team_type')) != 'pos':
                    today.append(x.get('name'))
                    order.append(x.get('amount_total'))
                elif  str(x.get('team_type')) == 'pos':
                    for b in b1:
                        if b.get('id') == x.get('id'):
                            today.append(b.get('name'))
                            order.append(b.get('amount_total_pos'))
        elif option == "pos_monthly_sales_team":
            self._cr.execute("SELECT crm_team.id, crm_team.name, crm_team.team_type, SUM(sale_order.amount_total) as amount_total FROM crm_team LEFT OUTER join sale_order on sale_order.team_id = crm_team.id AND sale_order.date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' WHERE active = True GROUP BY crm_team.id, crm_team.name, crm_team.team_type ORDER BY crm_team.name")
            docs1 = self._cr.dictfetchall()
            self._cr.execute("SELECT crm_team.id, crm_team.name, SUM(pos_order.amount_total) as amount_total_pos FROM crm_team LEFT OUTER join pos_config on pos_config.crm_team_id = crm_team.id LEFT OUTER join pos_session on pos_session.config_id = pos_config.id LEFT OUTER join pos_order on pos_order.session_id = pos_session.id WHERE date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY crm_team.id, crm_team.name")
            b1 = self._cr.dictfetchall()
            for x in docs1:
                if str(x.get('team_type')) != 'pos':
                    today.append(x.get('name'))
                    order.append(x.get('amount_total'))
                elif  str(x.get('team_type')) == 'pos':
                    for b in b1:
                        if b.get('id') == x.get('id'):
                            today.append(b.get('name'))
                            order.append(b.get('amount_total_pos'))
        elif option == "pos_year_sales_team":
            self._cr.execute("SELECT crm_team.id, crm_team.name, crm_team.team_type, SUM(sale_order.amount_total) as amount_total FROM crm_team LEFT OUTER join sale_order on sale_order.team_id = crm_team.id AND sale_order.date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit))  +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' WHERE active = True GROUP BY crm_team.id, crm_team.name, crm_team.team_type ORDER BY crm_team.name")
            docs1 = self._cr.dictfetchall()
            self._cr.execute("SELECT crm_team.id, crm_team.name, SUM(pos_order.amount_total) as amount_total_pos FROM crm_team LEFT OUTER join pos_config on pos_config.crm_team_id = crm_team.id LEFT OUTER join pos_session on pos_session.config_id = pos_config.id LEFT OUTER join pos_order on pos_order.session_id = pos_session.id WHERE date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit))  +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY crm_team.id, crm_team.name")
            b1 = self._cr.dictfetchall()
            for x in docs1:
                if str( x.get('team_type')) != 'pos':
                    today.append(x.get('name'))
                    order.append(x.get('amount_total'))
                elif  str(x.get('team_type')) == 'pos':
                    for b in b1:
                        if b.get('id') == x.get('id'):
                            today.append(b.get('name'))
                            order.append(b.get('amount_total_pos'))
        if date2:
            self._cr.execute("SELECT crm_team.id, crm_team.name, crm_team.team_type, SUM(sale_order.amount_total) as amount_total FROM crm_team LEFT OUTER join sale_order on sale_order.team_id = crm_team.id AND sale_order.date_order >= '"+ str(date1)  +"' AND date_order < '"+str(date2)+"' WHERE active = True GROUP BY crm_team.id, crm_team.name, crm_team.team_type ORDER BY crm_team.name")
            docs1 = self._cr.dictfetchall()
            self._cr.execute("SELECT crm_team.id, crm_team.name, SUM(pos_order.amount_total) as amount_total_pos FROM crm_team LEFT OUTER join pos_config on pos_config.crm_team_id = crm_team.id LEFT OUTER join pos_session on pos_session.config_id = pos_config.id LEFT OUTER join pos_order on pos_order.session_id = pos_session.id WHERE date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY crm_team.id, crm_team.name")
            b1 = self._cr.dictfetchall()
            for x in docs1:
                if str(x.get('team_type')) != 'pos':
                    today.append(x.get('name'))
                    order.append(x.get('amount_total'))
                elif  str(x.get('team_type')) == 'pos':
                    for b in b1:
                        if b.get('id') == x.get('id'):
                            today.append(b.get('name'))
                            order.append(b.get('amount_total_pos'))
        elif date1:
            self._cr.execute("SELECT crm_team.id, crm_team.name, crm_team.team_type, SUM(sale_order.amount_total) as amount_total FROM crm_team LEFT OUTER join sale_order on sale_order.team_id = crm_team.id AND sale_order.date_order >= '"+ str(date1)  +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' WHERE active = True GROUP BY crm_team.id, crm_team.name, crm_team.team_type ORDER BY crm_team.name")
            docs1 = self._cr.dictfetchall()
            self._cr.execute("SELECT crm_team.id, crm_team.name, SUM(pos_order.amount_total) as amount_total_pos FROM crm_team LEFT OUTER join pos_config on pos_config.crm_team_id = crm_team.id LEFT OUTER join pos_session on pos_session.config_id = pos_config.id LEFT OUTER join pos_order on pos_order.session_id = pos_session.id WHERE date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY crm_team.id, crm_team.name")
            b1 = self._cr.dictfetchall()
            for x in docs1:
                if str(x.get('team_type')) != 'pos':
                    today.append(x.get('name'))
                    order.append(x.get('amount_total'))
                elif  str(x.get('team_type')) == 'pos':
                    for b in b1:
                        if b.get('id') == x.get('id'):
                            today.append(b.get('name'))
                            order.append(b.get('amount_total_pos'))
        final = [order, today, name]
        return final

    @api.model
    def get_customers_chart(self):
        docs = self.env['res.partner'].search([('customer','=',True), ('parent_id', '=', False)])
        order = []
        today = []
        name = 'SALES'
        for record in docs:
            order.append(record.sale_order_count)
            today.append(record.name)
        final = [order, today, name]
        return final

    @api.model
    def get_order(self,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
        if not date2:
            self._cr.execute("SELECT id FROM sale_order WHERE date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ;")
            result = self._cr.dictfetchall()
            order = len(result)
            record = request.env.ref('custom_sale_dashboard.action_orders2')
            record.write({
                    'domain' : [("date_order",">=",str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit))), ("date_order","<",str(datetime.now() + timedelta(hours=7)))], 
                    'context': {}
                    })
        elif date2:
            self._cr.execute("SELECT id FROM sale_order WHERE date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' ; ")
            result = self._cr.dictfetchall()
            order = len(result)
            record = request.env.ref('custom_sale_dashboard.action_orders2')
            record.write({
                    'domain' : [("date_order",">=",str(date1)), ("date_order","<",str(date2))], 
                    'context': {}
                    })
        return order

    @api.model
    def get_quotation(self,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
        if not date2:
            self._cr.execute("SELECT * FROM sale_order WHERE state = 'draft' AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ;")
            result = self._cr.dictfetchall()
            order = len(result)
            record = request.env.ref('custom_sale_dashboard.action_quotations_with_onboarding2')
            record.write({
                    'domain' : [("state","=","draft"),("date_order",">=",str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit))), ("date_order","<",str(datetime.now() + timedelta(hours=7)))], 
                    'context': {}
                    })
        elif date2:
            self._cr.execute("SELECT * FROM sale_order WHERE state = 'draft' AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"';")
            result = self._cr.dictfetchall()
            order = len(result)
            record = request.env.ref('custom_sale_dashboard.action_quotations_with_onboarding2')
            record.write({
                    'domain' : [("state","=","draft"),("date_order",">=",str(date1)), ("date_order","<",str(date2))], 
                    'context': {}
                    })
        return order

    @api.model
    def get_invoice(self,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
        if not date2:
            self._cr.execute("SELECT id FROM sale_order WHERE invoice_status = 'to invoice' AND date_order >= '"+ str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' ")
            result = self._cr.dictfetchall()
            order = len(result)
            record = request.env.ref('custom_sale_dashboard.action_orders3')
            record.write({
                    'domain' : [("invoice_status","=","to invoice"),("date_order",">=",str(datetime.now() + timedelta(days=-tgl, hours=-jam, minutes=-menit))), ("date_order","<",str(datetime.now() + timedelta(hours=7)))], 
                    'context': {}
                    })
        elif date2:
            self._cr.execute("SELECT id FROM sale_order WHERE invoice_status = 'to invoice' AND date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"'")
            result = self._cr.dictfetchall()
            order = len(result)
            record = request.env.ref('custom_sale_dashboard.action_orders3')
            record.write({
                    'domain' : [("invoice_status","=","to invoice"),("date_order",">=",str(date1)), ("date_order","<",str(date2))], 
                    'context': {}
                    })
        return order

    @api.model
    def get_teams(self):
        # a = self.env['crm.team'].search([])
        self._cr.execute("SELECT name FROM crm_team WHERE active = True")
        result = self._cr.dictfetchall()
        order = len(result)
        return order

    @api.model
    def get_top_customers(self, option,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f') 
        count = 0
        order = ""
        no = 0
        apa = []
        if option == 'top_customers_today':
            self._cr.execute("SELECT res_partner.id as id, sale_order.partner_id , res_partner.name ,COUNT(res_partner.name) as asmuni ,SUM(sale_order_line.product_uom_qty) as product_uom_qty From sale_order_line JOIN sale_order on sale_order_line.order_id = sale_order.id JOIN res_partner on sale_order.partner_id = res_partner.id WHERE date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.name, res_partner.id, sale_order.partner_id ORDER BY asmuni DESC;")
            result = self._cr.dictfetchall()
            for x in result:
                if x.get('partner_id') not in apa:
                    apa.append(x.get('partner_id'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/customer/filter?customer="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('product_uom_qty'))+"</td><td>"+"{:,}".format(x.get('asmuni'))+"</td></tr>"
                    if no == 10:
                        break

        elif option == 'top_customers_month':
            self._cr.execute("SELECT res_partner.id as id, sale_order.partner_id , res_partner.name ,COUNT(res_partner.name) as asmuni ,SUM(sale_order_line.product_uom_qty) as product_uom_qty From sale_order_line JOIN sale_order on sale_order_line.order_id = sale_order.id JOIN res_partner on sale_order.partner_id = res_partner.id WHERE date_order >= '"+ str(datetime.now() + timedelta(days=-tgl ,hours=7)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.name, res_partner.id, sale_order.partner_id ORDER BY asmuni DESC;")
            result = self._cr.dictfetchall()
            for x in result:
                if x.get('partner_id') not in apa:
                    apa.append(x.get('partner_id'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/customer/filter?customer="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('product_uom_qty'))+"</td><td>"+"{:,}".format(x.get('asmuni'))+"</td></tr>"
                    if no == 10 :
                        break

        elif option == 'top_customers_year':
            self._cr.execute("SELECT res_partner.id as id, sale_order.partner_id , res_partner.name ,COUNT(res_partner.name) as asmuni ,SUM(sale_order_line.product_uom_qty) as product_uom_qty From sale_order_line JOIN sale_order on sale_order_line.order_id = sale_order.id JOIN res_partner on sale_order.partner_id = res_partner.id WHERE date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.name, res_partner.id, sale_order.partner_id ORDER BY asmuni DESC;")
            result = self._cr.dictfetchall()
            for x in result:
                if x.get('partner_id') not in apa:
                    apa.append(x.get('partner_id'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/customer/filter?customer="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('product_uom_qty'))+"</td><td>"+"{:,}".format(x.get('asmuni'))+"</td></tr>"
                    if no == 10:  
                        break

        if date2:
            self._cr.execute("SELECT res_partner.id as id, sale_order.partner_id , res_partner.name ,COUNT(res_partner.name) as asmuni ,SUM(sale_order_line.product_uom_qty) as product_uom_qty From sale_order_line JOIN sale_order on sale_order_line.order_id = sale_order.id JOIN res_partner on sale_order.partner_id = res_partner.id WHERE date_order >= '"+ str(date1) +"' AND date_order < '"+str(date2)+"' GROUP BY res_partner.name, res_partner.id, sale_order.partner_id ORDER BY asmuni DESC;")
            result = self._cr.dictfetchall()
            for x in result:
                if x.get('partner_id') not in apa:
                    apa.append(x.get('partner_id'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/customer/filter?customer="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('product_uom_qty'))+"</td><td>"+"{:,}".format(x.get('asmuni'))+"</td></tr>"
                    if no == 10:
                        break

        elif date1:
            self._cr.execute("SELECT res_partner.id as id, sale_order.partner_id , res_partner.name ,COUNT(res_partner.name) as asmuni ,SUM(sale_order_line.product_uom_qty) as product_uom_qty From sale_order_line JOIN sale_order on sale_order_line.order_id = sale_order.id JOIN res_partner on sale_order.partner_id = res_partner.id WHERE date_order >= '"+ str(date1) +"' AND date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.name, res_partner.id, sale_order.partner_id ORDER BY asmuni DESC;")
            result = self._cr.dictfetchall()
            for x in result:
                if x.get('partner_id') not in apa:
                    apa.append(x.get('partner_id'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/customer/filter?customer="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('product_uom_qty'))+"</td><td>"+"{:,}".format(x.get('asmuni'))+"</td></tr>"
                    if no == 10:
                        break

        return order

    @api.model
    def get_top_sales(self, option,date1,date2):
        if date1:
            date1 = str(date1) + " " + "00:00:00.0"
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S.%f')
        if date2:
            date2 = str(date2) + " " + "00:00:00.0"
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S.%f')
        order = ""
        no = 0
        count = 0
        if option == 'top_sales_today':
            # a = self.env['sale.order'].search([('amount_total', '!=', 0)]).sorted(key = lambda rec: rec.get_top_insales_today()[1], reverse=True)
            self._cr.execute("SELECT res_partner.id, res_partner.name, sum(sale_order.amount_total) as total, count(sale_order.id) as sale FROM sale_order JOIN res_users on sale_order.user_id = res_users.id JOIN res_partner on res_partner.id = res_users.partner_id WHERE sale_order.date_order >= '"+ str(datetime.now() + timedelta(hours=-jam, minutes=-menit)) +"' AND sale_order.date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.id  ORDER BY total DESC")
            result2 = self._cr.dictfetchall()
            # raise AccessError(str(result2))
            apa2 = []
            for x in result2:
                if x.get('name') not in apa2:
                    apa2.append(x.get('name'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/sales_person/filter?person="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('sale'))+"</td><td>"+"{:,}".format(x.get('total'))+"</td></tr>"
                    if no == 10:
                        break

        elif option == 'top_sales_month':
            self._cr.execute("SELECT res_partner.id, res_partner.name, sum(sale_order.amount_total) as total, count(sale_order.id) as sale FROM sale_order JOIN res_users on sale_order.user_id = res_users.id JOIN res_partner on res_partner.id = res_users.partner_id WHERE sale_order.date_order >= '"+ str(datetime.now() + timedelta(days=-tgl ,hours=7)) +"' AND sale_order.date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.id  ORDER BY total DESC")
            result2 = self._cr.dictfetchall()
            # raise AccessError(str(result2))
            apa2 = []
            for x in result2:
                if x.get('name') not in apa2:
                    apa2.append(x.get('name'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/sales_person/filter?person="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('sale'))+"</td><td>"+"{:,}".format(x.get('total'))+"</td></tr>"
                    if no == 10:
                        break
        elif option == 'top_sales_year':
            self._cr.execute("SELECT res_partner.id, res_partner.name, sum(sale_order.amount_total) as total, count(sale_order.id) as sale FROM sale_order JOIN res_users on sale_order.user_id = res_users.id JOIN res_partner on res_partner.id = res_users.partner_id WHERE sale_order.date_order >= '"+ str(datetime.now() - relativedelta(months=bln) + timedelta(days=-tgl, hours=-jam, minutes=-menit)) +"' AND sale_order.date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.id  ORDER BY total DESC")
            result2 = self._cr.dictfetchall()
            # raise AccessError(str(result2))
            apa2 = []
            for x in result2:
                if x.get('name') not in apa2:
                    apa2.append(x.get('name'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/sales_person/filter?person="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('sale'))+"</td><td>"+"{:,}".format(x.get('total'))+"</td></tr>"
                    if no == 10:
                        break

        if date2:
            # a = self.env['sale.order'].search([('amount_total', '!=', 0)]).sorted(key = lambda rec: rec.get_top_insales_today()[1], reverse=True)
            self._cr.execute("SELECT res_partner.id, res_partner.name, sum(sale_order.amount_total) as total, count(sale_order.id) as sale FROM sale_order JOIN res_users on sale_order.user_id = res_users.id JOIN res_partner on res_partner.id = res_users.partner_id WHERE sale_order.date_order >= '"+ str(date1) +"' AND sale_order.date_order < '"+str(date2)+"' GROUP BY res_partner.id  ORDER BY total DESC")
            result2 = self._cr.dictfetchall()
            # raise AccessError(str(result2))
            apa2 = []
            for x in result2:
                if x.get('name') not in apa2:
                    apa2.append(x.get('name'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/sales_person/filter?person="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('sale'))+"</td><td>"+"{:,}".format(x.get('total'))+"</td></tr>"
                    if no == 10:
                        break
        
        elif date1:
            # a = self.env['sale.order'].search([('amount_total', '!=', 0)]).sorted(key = lambda rec: rec.get_top_insales_today()[1], reverse=True)
            self._cr.execute("SELECT res_partner.id, res_partner.name, sum(sale_order.amount_total) as total, count(sale_order.id) as sale FROM sale_order JOIN res_users on sale_order.user_id = res_users.id JOIN res_partner on res_partner.id = res_users.partner_id WHERE sale_order.date_order >= '"+ str(date1) +"' AND sale_order.date_order < '"+str(datetime.now() + timedelta(hours=7))+"' GROUP BY res_partner.id  ORDER BY total DESC")
            result2 = self._cr.dictfetchall()
            # raise AccessError(str(result2))
            apa2 = []
            for x in result2:
                if x.get('name') not in apa2:
                    apa2.append(x.get('name'))
                    no += 1
                    order = order + "<tr><td width=\"30px\" style=\"text-align: center;\">"+str(no)+"</td><td><a href='/sales/sales_person/filter?person="+str(x.get('id'))+"' target='_blank'>"+str(x.get('name'))+"</a></td><td>"+"{:,}".format(x.get('sale'))+"</td><td>"+"{:,}".format(x.get('total'))+"</td></tr>"
                    if no == 10:
                        break
                
        return order

    @api.model
    def get_date_now(self):
        first_date = (datetime.now() + timedelta(days=-tgl + 1, hours=-jam, minutes=-menit)).strftime('%Y-%m-%d')
        last_date = (datetime.now() + relativedelta(months=1) + timedelta(days=-tgl -1 , hours=-jam, minutes=-menit)).strftime('%Y-%m-%d')
        return [first_date, last_date]