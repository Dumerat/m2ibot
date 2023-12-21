from interactions import *
from datetime import *

class Homework_add(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db
        self.homework_db = db["homework"]
        self.user_db = db["user"]
        
        self.subject_data = self.db["data"].find_one({"id":"subject"})["list"]
        subject_list = [item["name"] for item in self.subject_data if "name" in item]
        self.choice_subject = [SlashCommandChoice(name=i, value=i) for i in subject_list]

        class_data = self.db["data"].find_one({"id":"class"})["list"]
        class_list = [item["name"] for item in class_data if "name" in item]
        self.choice_class = [SlashCommandChoice(name=i, value=i) for i in class_list]
        
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
            description = "Date de début du devoir (année-mois-jour)",
            required = True,
            opt_type = OptionType.STRING,
            )
        @slash_option(
            name = "date_end",
            description = "Date de fin du devoir (année-mois-jour)",
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
            try:
                date_start = datetime.strptime(date_start, "%Y-%m-%d")
                date_end = datetime.strptime(date_end, "%Y-%m-%d")
            except ValueError:
                await ctx.send("Erreur de format de date. Utilisez le format YYYY-MM-DD.")
            
            prof = [item.get("prof") for item in self.subject_data if "name" in item and item["name"] == matière]
            # student = user_db
            self.homework_db.insert_one({
                "name": nom,
                "prof": prof[0],
                "subject": matière,
                "class": classe,
                "start_date": date_start,
                "end_date": date_end,
                "link": link,
                "completed": {}
                })
            await ctx.send(f"Devoir ajouté: {nom} - Matière : {matière} - Classe : {classe} - Début : {date_start} - Fin : {date_end} - Lien : {link}")

        self.bot.add_command(message_add)