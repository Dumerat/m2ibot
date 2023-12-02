from interactions import *

class Dashboard(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db

    @slash_command(name="modal_test", description="Modals test")
    async def my_command_function(self, ctx: SlashContext):
        my_modal = Modal(
            ShortText(label="Short Input Text", custom_id="short_text"),
            ParagraphText(label="Long Input Text", custom_id="long_text"),
            title="My Modal",
        )
        await ctx.send_modal(modal=my_modal)