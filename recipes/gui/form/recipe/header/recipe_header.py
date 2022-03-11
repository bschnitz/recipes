from recipes.gui.form.framework import RowWiseForm
from recipes.gui.form.recipe.header import RecipeHeaderRowFactory

class RecipeHeader:
    def __init__(self, parent, title, meta = {}):
        self.form = RowWiseForm(parent, RecipeHeaderRowFactory)
        self.form.append_row(label = 'Title', value = title)

        # label and input for all other meta fields
        for key in meta:
            self.form.append_row(meta[key]['label'], meta[key].get('value', ''))

        choices = ['blue', 'yellow', 'green', 'very long option']
        self.form.append_row(choices = choices, callback = self.onAddMeta)

        parent.SetSizer(self.form.create_box())

    def onAddMeta(self, event, combobox):
        self.form.insert_row(-1, label = combobox.GetValue(), value = combobox.GetValue())
