from interactions import *
from bson import ObjectId
from datetime import *
from pymongo.errors import PyMongoError

class homework_view(Extension):
    def __init__(self, bot, db):
        super().__init__()
        self.bot = bot
        self.db = db
        self.homework_db = db["homework"]

        class_data = self.db["data"].find_one({"id":"class"})["list"]
        class_list = [item["name"] for item in class_data if "name" in item]
        self.choice_class = [SlashCommandChoice(name=i, value=i) for i in class_list]

        self.setup_view_homework()
        self.setup_view_all_homework()

    def setup_view_homework(self):
        @slash_command(
            name="mesdevoirs",
            description="Permet de voir les devoirs me concernant")
        async def view_homework(ctx: SlashContext):
            try:
                await ctx.send(ctx.user.id) # trouver le user sur la db pour son groupe puis faut taffer maintenant et penser à rajouter un tag sur chaque devoir pour savoir qui a finis le devoirs (à l'aide)
                if ObjectId.is_valid(id):
                    result = self.homework_db.delete_one({"_id": ObjectId(id)})
                    if result.deleted_count > 0:
                        await ctx.send(f"Devoir {id} supprimé")
                    else:
                        await ctx.send(f"Aucun devoir trouvé avec l'ID {id}")
                else:
                    await ctx.send(f"l'ID: {id} n'est pas un ObjectId")
            except PyMongoError as e:
                await ctx.send(f"Une erreur s'est produite lors de la suppression du devoir : {str(e)}")

        self.bot.add_command(view_homework)

    def setup_view_all_homework(self):
        @slash_command(
            name="toutlesdevoirs",
            description="Permet de voir tout les devoirs de la bdd")
        @slash_option(
            name="catégorie",
            description="Choisir la catégorie des devoirs que tu veux trouver",
            required=True,
            opt_type=OptionType.STRING,
            choices=self.choice_class,
            )
        @slash_option(
            name="passed",
            description="veux tu voir les devoirs d'actualité / dépassé sinon ne rien mettre ici pour les deux",
            required=False,
            opt_type=OptionType.BOOLEAN,
            )
        async def view_all_homework(ctx: SlashContext, nom):
            homework_items = self.homework_db.find({"name": nom})
            count = self.homework_db.count_documents({"name": nom})
            
            if count == 0:
                await ctx.send(f"Aucun devoir trouvé avec le nom {nom}.")
            else:
                message = f"Devoirs trouvés avec le nom {nom}:\n"
                for homework in homework_items:
                    homework_id = homework["_id"]
                    start_date = homework.get("start_date", "Date non trouvée !")
                    start_dated = start_date.strftime("%d %m %Y")
                    message += f"L'ID du devoir est : {homework_id} date de début le {start_dated}\n" 
                message += f"\nUtilise /removebyid <ID> pour supprimer un devoir."
                await ctx.send(message)

        self.bot.add_command(view_all_homework)