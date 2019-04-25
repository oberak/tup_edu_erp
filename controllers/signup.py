# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import werkzeug
import re

from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import UserError
from odoo.http import request

_logger = logging.getLogger(__name__)


class TupAuthSignupHome(AuthSignupHome):
    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                    if user_sudo and template:
                        template.sudo().with_context(
                            lang=user_sudo.lang,
                            auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),
                        ).send_mail(user_sudo.id, force_send=True)
                return super(AuthSignupHome, self).web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('tup_edu_erp.login', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password', 'nrc_no') }
        nrc = qcontext.get('nrc_no')
        
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them!!."))
        supported_langs = [lang['code'] for lang in request.env['res.lang'].sudo().search_read([], ['code'])]
        if request.lang in supported_langs:
            values['lang'] = request.lang

        if not (len(values.get('nrc_no')) >= 17 and len(values.get('nrc_no')) <= 21) :
            raise UserError(_("Wrong NRC No. format!! Try again!!"))

        if not re.findall("\d{6}", nrc[len(nrc)-6:]) :
            raise UserError(_("Wrong Number format!! Try again!!"))

        if not re.findall("[(]{1}", nrc[len(nrc)-9:len(nrc)-8]) :
            raise UserError(_("Wrong parenthesis position!! Try again!!"))

        if not re.findall("[A-Z]{1}", nrc[len(nrc)-8:len(nrc)-7]) :
            raise UserError(_("Wrong citizenship character!! Try again!!"))

        if not re.findall("[)]{1}", nrc[len(nrc)-7:len(nrc)-6]) :
            raise UserError(_("Wrong parenthesis position!! Try again!!"))

        if nrc.find("/") == -1 :
            raise UserError(_("Use blackslash properly!! Try again!!"))
        
        if not (nrc.find("/") == 1 or nrc.find("/") == 2) :
            raise UserError(_("Wrong usage of blackslash!! Try again!!"))
        
        if not (len(nrc[nrc.find("/")+1:nrc.find("(")+1]) >= 6 and len(nrc[nrc.find("/")+1:nrc.find("(")]) <= 8) :
            raise UserError(_("Too many township characters!! Try again!!"))
        
        if not re.findall("^[a-zA-Z]{6,8}", nrc[nrc.find("/")+1:nrc.find("(")+1]) :
            raise UserError(_("Wrong township characters!! Try again!!"))
        
        if not re.findall("^[0-9]{1,2}", nrc[0:nrc.find("/")]) :
            raise UserError(_("Wrong township number!! Try again!!"))
        
        if not re.findall("^(1[0-5]|[1-9])$", nrc[0:nrc.find("/")]) :
            raise UserError(_("Invalid township number!! Try again!!"))
            
        if len(values.get('nrc_no')) >= 17 and len(values.get('nrc_no')) <= 21 :
            user_sudo = request.env['education.application'].sudo().search([('nrc_no', '=', qcontext.get('nrc_no'))])
            if not user_sudo:
                raise UserError(_("Your nrc no is not included in admission list!"))
                
        # TODO check NRC or ADM NO
                    # if NRC
                        # if New student : check in applicaions table
                        # else Old one: check in students table
                    # if Addmission No : new student

                    # if not exists return error
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

        