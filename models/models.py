# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dashboard_sale(models.Model):
	_inherit = 'sale.order'

	custom_order = fields.Char(compute="total_custom",store=True)

	def total_custom(self):
		a = self.env['sale.order'].search([])
		for x in a:
			x.custom_order = 'draft'