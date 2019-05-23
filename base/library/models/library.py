# -*- coding: utf-8 -*-
"""Model file for Library module
"""

import logging
from datetime import timedelta, datetime
from openerp import models, fields, api

_LOGGER = logging.getLogger("name")


class Borrower(models.Model):
    """Model for borrower view
    """
    _name = "borrower"
    _rec_name = "full_name"
    first_name = fields.Char("First Name")
    last_name = fields.Char("Last Name")
    full_name = fields.Char("Full Name", compute="_compute_full_name")

    @api.depends("first_name", "last_name")
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name


class Book(models.Model):
    """Model for book view
    """
    _name = "book"
    _rec_name = "title"
    title = fields.Char("Book Title")
    author = fields.Char("Book Author")
    days_allowed = fields.Integer("Days allowed to be borrowed")
    year_published = fields.Integer("Year Published")


class Lending(models.Model):
    """Model for lending view
    """
    _name = "lending"
    _rec_name = "borrower"
    borrower = fields.Many2one("borrower", string="Borrower")
    first_name = fields.Char("First Name", related="borrower.first_name")
    last_name = fields.Char("Last Name", related="borrower.last_name")
    date = fields.Datetime("Date borrowed",
                           default=lambda self: fields.datetime.now())
    book = fields.One2many("process", "process_id", string="Borrowed books")
    book_count = fields.Integer("Count of borrowed books",
                                compute="_compute_book_count",
                                store=True)
    book_count_kanban = fields.Char(compute="_compute_book_count_kanban")
    kanban_state = fields.Selection(
        [('normal', 'In Progress'),
         ('blocked', 'Blocked'),
         ('done', 'Ready for next stage')],
        'Kanban State', default='normal')

    @api.depends("book")
    def _compute_book_count(self):
        for rec in self:
            rec.book_count = len(rec.book)

    @api.depends("book_count")
    def _compute_book_count_kanban(self):
        for rec in self:
            rec.book_count_kanban = str(rec.book_count) + ' book(s) borrowed'


class ProcessInfos(models.Model):
    """Model for lending view bottom group
    """
    _name = "process"
    process_id = fields.Many2one("lending")
    title = fields.Many2one("book")
    days_allowed = fields.Integer("Days allowed to be borrowed",
                                  related="title.days_allowed")
    expected_date = fields.Date("Expected date of return",
                                compute="_compute_expected_date")

    @api.depends("title", "process_id.date")
    def _compute_expected_date(self):
        for rec in self:
            rec.expected_date = (datetime.strptime(rec.process_id.date,
                                                   "%Y-%m-%d %H:%M:%S") +
                                 timedelta(days=rec.days_allowed))
