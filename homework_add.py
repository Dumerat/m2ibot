from interactions import *

class Homework_add(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db
        
        subject = self.db["homework"].find().sort("subject") # to be changed by another collection containing all structural data cuz this is shit
        subject_list = set(",".join(sub["subject"] for sub in subject).split(",")) # create a set of unique subject in all homework
        self.choice_list =[SlashCommandChoice(name=i, value=i) for i in subject_list]
        self.setup_commands()

    def setup_commands(self):
        @slash_command(
            name="add",
            description="Permet d'ajouter un devoir pour tout le monde")
        @slash_option(
            name = "name",
            description= "nom du devoir",
            required=True,
            opt_type=OptionType.STRING,
            )
        @slash_option(
            name = "matière",
            description= "nom de la matière",
            required=True,
            opt_type=OptionType.STRING,
            choices=self.choice_list
            )
        @slash_option(
            name = "named",
            description= "nom du devoir",
            required=True,
            opt_type=OptionType.INTEGER,
            choices=[
                SlashCommandChoice(name="poulet", value=1),
                SlashCommandChoice(name="nuggets", value=2)
            ]
            )
        async def message_add(ctx: SlashContext):
            a = ctx.args[0] # 0 for name 1 for sub etcc
            await ctx.send(f"yo ça marche feur{ctx}{a}")

        self.bot.add_command(message_add)