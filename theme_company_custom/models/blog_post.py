from odoo import models, fields, api


class BlogPost(models.Model):
    _inherit = "blog.post"

    @api.depends('video_url')
    def _compute_url(self):
        for blog in self:
            if blog.video_url:
                if 'watch?v=' in blog.video_url:
                    blog.video_embed = "https://www.youtube.com/embed/" + blog.video_url.split("watch?v=", 1)[-1]

    video_url = fields.Char(string="Video URL")
    video_embed = fields.Char(string="Video Embed", compute='_compute_url')
