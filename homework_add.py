from interactions import *

class Homework_add(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db

    @slash_command(
            name="add",
            description="Permet d'ajouter un devoir pour tout le monde")
    @slash_option(
        name = "integer_option",
        description= "la desc 1",
        required=True,
        opt_type=OptionType.INTEGER,
        choices=[
            SlashCommandChoice(name="poulet", value=1),
            SlashCommandChoice(name="nuggets", value=2)
        ]
        )
    async def test(self, ctx: ComponentContext, integer_option: int = 1):
        await ctx.send(f"yo ça marche {integer_option}")