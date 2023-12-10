from interactions import *
from datetime import *

class User_add(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db

        class_data = self.db["data"].find_one({"id":"class"})["list"]
        class_list = [item["name"] for item in class_data if "name" in item]
        class_other_data = self.db["data"].find_one({"id":"class"})["otherList"]
        class_other_list = [item["name"] for item in class_other_data if "name" in item]
        self.choice_group = [SlashCommandChoice(name=i, value=i) for i in class_list + class_other_list]
        
        self.setup_user()

    def setup_user(self):
        @slash_command(
            name="jesuis",
            description="Créer ou modifier votre profil (penser à mettre tout les paramètres pour la création)")
        @slash_option(
            name = "name",
            description = "Entre ton prénom",
            required = False,
            opt_type = OptionType.STRING,
            )
        @slash_option(
            name = "lastname",
            description = "Entre ton nom de famille (à cause des mi(ch/k)ael)",
            required = False,
            opt_type = OptionType.STRING,
            )
        @slash_option(
            name = "group",
            description = "Groupe concernée",
            required = False,
            opt_type = OptionType.STRING,
            choices = self.choice_group
            )
        @slash_option(
            name = "birthday",
            description = "Entre ta date d'anniversaire (année-mois-jour / YYYY-MM-DD)",
            required = False,
            opt_type = OptionType.STRING,
            )
        async def user_add(ctx: SlashContext, name=None, lastname=None, group=None, birthday=None):
            res = self.db["user"].find_one({"userid": str(ctx.user.id)})
            print(res)
            if res is not None:
                print("yes")
                if birthday:
                    try:
                        birthday = datetime.strptime(birthday, "%Y-%m-%d")
                        await ctx.send("ouioui")
                    except ValueError:
                        await ctx.send("Erreur de format de date. Utilisez le format YYYY-MM-DD.")
            else:
                await ctx.send("logic of user creation")

            await ctx.send(f"Devoir ajouté: {birthday}")

        self.bot.add_command(user_add)