import pytz
from odoo import models, fields, api
from datetime import timedelta, datetime, date


class PosDashboard(models.AbstractModel):
    _inherit = 'board.board'

    apa = fields.Integer()