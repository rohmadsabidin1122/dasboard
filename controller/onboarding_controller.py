# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import werkzeug.utils
from odoo.addons.sale.controllers.onboarding import OnboardingController  


class CustomOnboardingController(OnboardingController): 

    @http.route('custom_sale_dashboard.sale_quotation_notify', auth='user', type='json')
    def sale_dashboard(self):
       
        company = request.env.user.company_id
        
        return {
            'html': request.env.ref('custom_sale_dashboard.sale_quotation_notify').render({
                'company': company if company else True,
                'state': True
            })
        }
    
    @http.route('/sales/sale_quotation_onboarding_panel/filter', auth='user', type='http')
    def sale_filter(self,**kw):
        record = request.env.ref('sale.action_quotations_with_onboarding')
        key = kw.get('states')
        record.write({
        				'domain' : [], 
        				'context': {'search_default_my_quotation':False, 
        							'search_default_quotation': True if key == 'quotation' else False,
        							'search_default_sales': True if key == 'sale' else False,
        							'search_default_sents': True if key == 'sent' else False,
        							'search_default_cancel': True if key == 'cancel' else False
        							}
        			})
        return werkzeug.utils.redirect('/web#action={0}&amp;model=sale.order&amp;view_type=list&amp;'.format(record.id))

      