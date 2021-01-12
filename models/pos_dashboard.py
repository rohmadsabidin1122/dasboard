from odoo import models, fields, api
from datetime import timedelta, datetime, date, time

class PosDashboard(models.Model):
    _inherit = 'sale.order'

    @api.model
    def get_orders_chart(self, option):
        docs = self.env['sale.order'].search([])
        apa = 0
        order = []
        today = []
        if option == 'pos_dayly_sales':
            name = 'DAYS'
            for record in docs:
                if record.date_order != False:
                    if str(record.date_order.strftime("%m/%d/%Y")) not in today:
                        if apa != 0:
                            order.append(apa)
                        apa = apa * 0
                        today.append(record.date_order.strftime("%m/%d/%Y"))
                        apa = apa + record.amount_total
                    else:
                        apa = apa + record.amount_total
                        if record.id == docs[-1].id:
                            order.append(apa)  

        elif option == 'pos_monthly_sales':
            name = 'MONTHS'
            for record in docs:
                if record.date_order != False:
                    if str(record.date_order.strftime("%m/%Y")) not in today:
                        if apa != 0:
                            order.append(apa)
                        apa = apa * 0 
                        today.append(record.date_order.strftime("%m/%Y"))
                        apa = apa + record.amount_total
                    else:
                        apa = apa + record.amount_total
                        if record.id == docs[-1].id:
                            order.append(apa)

        elif option == 'pos_year_sales':
            name = 'YEARS'
            for record in docs:
                if record.date_order != False:
                    if str(record.date_order.strftime("%Y")) not in today:
                        if apa != 0:
                            order.append(apa)
                        apa = apa * 0
                        today.append(record.date_order.strftime("%Y"))
                        apa = apa + record.amount_total
                    else:
                        apa = apa + record.amount_total
                        if record.id == docs[-1].id:
                            order.append(apa)

        final = [order, today, name]
        return final

    @api.model
    def get_product_chart(self, option):
        docs = self.env['product.template'].search([('type', '=', 'product')])
        order = []
        today = []
        name = "All Time"
        for x in docs:
            if x.sales_count != 0:
                today.append(x.name)
                order.append(x.sales_count)            
        final = [order, today, name]
        return final

    @api.model
    def get_top_product_list(self):
        docs = self.env['product.template'].search([('type', '=', 'product')],order="sales_count desc")
        order = []
        today = []
        name = "All Time"
        for x in docs:
            if x.sales_count != 0:
                today.append(x.name)
                order.append(x.sales_count)            
        final = [order, today, name]
        return final

    @api.model
    def get_teams_chart(self):
        docs = self.env['crm.team'].search([])
        order = []
        today = []
        name = 'DAYS'
        for record in docs:
            order.append(len(docs))
            today.append(record.name)
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
    def get_order(self):
        a = self.env['sale.order'].search([])
        order = len(a)
        return order

    @api.model
    def get_quotation(self):
        a = self.env['sale.order'].search([('state','=','draft')])
        order = len(a)
        return order
    

    @api.model
    def get_invoice(self):
        a = self.env['sale.order'].search([('invoice_status', '=', 'to invoice')])
        order = len(a)
        return order

    @api.model
    def get_teams(self):
        a = self.env['crm.team'].search([])
        order = str(len(a))
        return order

    @api.model
    def get_top_customers(self):
        a = self.env['res.partner'].search([('customer','=',True), ('parent_id', '=', False)], order="purchase_order_count asc")
        order = ""
        no = 0
        for x in a:
            no = no + 1
            order = order + "<tr><td width=\"30px\">"+str(no)+"</td><td>"+str(x.name)+"</td><td>"+str(x.purchase_order_count)+"</td></tr>"
        return order

    @api.model
    def get_top_sales(self):
        a = self.env['sale.order'].search([])
        order = ""
        no = 0
        count = 0
        apa = []
        apa2 = []
        for x in a:
            apa.append(x.user_id.name)
        for x in a:
            if x.user_id.name not in apa2:
                no = no + 1
                apa2.append(x.user_id.name)
                order = order + "<tr><td width=\"30px\">"+str(no)+"</td><td>"+str(x.user_id.name)+"</td><td>"+str(sum((itm.count(x.user_id.name) for itm in apa)))+"</td></tr>"
        return order

    @api.model
    def get_top_insales(self):
        b = 0
        a = self.env['sale.order'].search([])
        for x in a:
            if self.user_id == x.user_id:
                b += 1
        return b
