from odoo import fields, models
from odoo.exceptions import UserError

class Issue(models.Model):
    _name = "ca.support.issue"
    _description = "Ticket de problema"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Titulo", required=True)
    description = fields.Text(string="Descripcion", required=True)
    issue_type = fields.Selection([
        ("error", "Error/Bug"),
        ("ayuda", "Ayuda"),
        ("funcionalidad_adicional", "Funcionalidad Adicional"),
        ("otro", "Otro")
    ], required=True, string="Tipo de ticket")
    priority = fields.Selection([
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta")
    ], required=True, string="Prioridad")
    state = fields.Selection([
        ("nuevo", "Nuevo"),
        ("en_proceso", "En Proceso"),
        ("finalizado", "Finalizado"),
        ("cancelado", "Cancelado")
    ], required=True, default="nuevo", copy=False, string="Estado", tracking=True)
    attachment = fields.Binary(string="Capture o adjunto", copy=False)
    
    user_id = fields.Many2one("res.users", string="Solicitante", default=lambda self: self.env.user, readonly=True, required=True)
    assigned_developer_id = fields.Many2one("res.users", string="Soportista", copy=False, readonly=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.user.company_id.id, readonly=True, required=True) 

    def action_procesar(self):
        for issue in self:
            if issue.state in ("cancelado","finalizado"):
                raise UserError("No se puede cambiar el estado a En Proceso una vez cancelado o finalizado el ticket.")
            issue.state = "en_proceso"
            issue.assigned_developer_id = self.env.user
        return True

    def action_finalizar(self):
        for issue in self:
            if issue.state == "cancelado":
                raise UserError("No se pueden finalizar tickets cancelados.")
            issue.state = "finalizado"
            issue.assigned_developer_id = self.env.user
        return True

    def action_cancelar(self):
        for issue in self:
            if issue.state == "finalizado":
                raise UserError("No se pueden cancelar tickets finalizados.")
            issue.state = "cancelado"
            issue.assigned_developer_id = self.env.user
        return True

