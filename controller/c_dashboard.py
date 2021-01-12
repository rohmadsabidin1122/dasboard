# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import werkzeug.utils
from odoo.addons.sale.controllers.onboarding import OnboardingController  


class CustomOnboardingController(OnboardingController): 

    @http.route('/custom_sale_dashboard/dashboard_form_view', auth='user', type='json')
    def sale_dashboard(self):
       
        company = request.env.user.company_id
        
        return {
            'html': request.env.ref('custom_sale_dashboard.sale_quotation_notify').render({
                'company': company if company else True,
                'state': True
            })
        }
    
    @http.route('/sales/order/filter', auth='user', type='http')
    def sale_order_filter(self,**kw):
        record = request.env.ref('custom_sale_dashboard.action_orders2')
        key = kw.get('states')
        # record.write({
        # 				'domain' : [], 
        # 				'context': {}
        # 			})
        return werkzeug.utils.redirect('/web#action={0}&amp;model=sale.order&amp;view_type=list&amp;'.format(record.id))


    @http.route('/sales/quotation/filter', auth='user', type='http')
    def sale_quotation_filter(self,**kw):
        record = request.env.ref('custom_sale_dashboard.action_quotations_with_onboarding2')
        key = kw.get('states')
        # record.write({
        #                 'domain' : [("state","=","draft")], 
        #                 'context': {}
        #             })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=sale.order&amp;view_type=list&amp;'.format(record.id))


    @http.route('/sales/to_invoice/filter', auth='user', type='http')
    def sale_customer_filter(self,**kw):
        record = request.env.ref('custom_sale_dashboard.action_orders3')
        key = kw.get('states')
        # record.write({
        #                 'domain' : [("invoice_status","=","to invoice")], 
        #                 'context': {}
        #             })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=sale.order&amp;view_type=list&amp;'.format(record.id))

    @http.route('/sales/teams/filter', auth='user', type='http')
    def sale_team_filter(self,**kw):
        record = request.env.ref('sales_team.crm_team_salesteams_act')
        key = kw.get('states')
        record.write({
                        'domain' : [], 
                        'context': {'search_default_my_favorites': True if key == 'favorites' else False,}
                    })
        return werkzeug.utils.redirect('/web#action={0}&amp;model=crm.team&amp;view_type=kanban&amp;'.format(record.id))

    @http.route('/sales/sales_person/filter', auth='user', type='http')
    def sale_sales_person_filter(self,**kw):
        record = request.env.ref('custom_sale_dashboard.action_contacts')
        key = kw.get('person')
        record.write({
                        'domain' : [('id', '=', key)], 
                        'context': {}
                    })
        return werkzeug.utils.redirect('/web#id='+key+'&action={0}&amp;model=res.partner&amp;view_type=form&amp;'.format(record.id))

    @http.route('/sales/customer/filter', auth='user', type='http')
    def sale_quotation_filter1(self,**kw):
        record = request.env.ref('custom_sale_dashboard.action_partner_customer_formku')
        key = kw.get('customer')
        record.write({
                        'domain' : [("id","=",key)],
                        'context': {}
                    })
        return werkzeug.utils.redirect("/web#id="+key+"&action={0}&model=res.partner&view_type=form&menu_id=".format(record.id))
