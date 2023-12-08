from interactions import *

class Homework_add(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db
        
        subject_data = self.db["data"].find_one({"id":"subject"})["list"]
        subject_list = [item["name"] for item in subject_data if "name" in item]
        self.choice_subject = [SlashCommandChoice(name=i, value=i) for i in subject_list]

        class_data = self.db["data"].find_one({"id":"class"})["list"]
        class_list = [item["name"] for item in class_data if "name" in item]
        self.choice_class = [SlashCommandChoice(name=i, value=i) for i in class_list]
        print(class_list)
        self.setup_commands()

    def setup_commands(self):
        @slash_command(
            name="add",
            description="Permet d'ajouter un devoir")
        @slash_option(
            name = "nom",
            description= "Nom du devoir",
            required=True,
            opt_type=OptionType.STRING,
            )
        @slash_option(
            name = "matière",
            description = "Nom de la matière",
            required = True,
            opt_type = OptionType.STRING,
            choices = self.choice_subject
            )
        @slash_option(
            name = "classe",
            description = "Classe concernée",
            required = True,
            opt_type = OptionType.STRING,
            choices = self.choice_class
            )
        @slash_option(
            name = "date_start",
            description = "Date de début du devoir (jour-mois-année)",
            required = True,
            opt_type = OptionType.STRING,
            )
        @slash_option(
            name = "date_end",
            description = "Date de fin du devoir (jour-mois-année)",
            required = True,
            opt_type = OptionType.STRING,
            )
        @slash_option(
            name = "link",
            description = "Lien vers le devoir",
            required = True,
            opt_type = OptionType.STRING,
            )
        async def message_add(ctx: SlashContext, nom, matière, classe, date_start, date_end, link):
            await ctx.send(f"yo ça marche feur {nom} {matière, classe, date_start, date_end, link}")

        self.bot.add_command(message_add)