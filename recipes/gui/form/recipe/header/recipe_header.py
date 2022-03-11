from recipes.gui.form.framework import RowWiseForm
from recipes.gui.form.recipe.header import RecipeHeaderRowFactory

class RecipeHeader:
    def __init__(self, parent, title, meta = {}):
        self.form = RowWiseForm(parent, RecipeHeaderRowFactory)
        self.form.append_attribute('Title', title)

        # label and input for all other meta fields
        for key in meta:
            label = meta[key]['label']
            value = meta[key].get('value', '')
            self.form.append_attribute(label, value)

        choices = ['blue', 'yellow', 'green', 'very long option']
        self.form.append_combo(choices, self.onAddMeta)

        parent.SetSizer(self.form.create_box())

    def onAddMeta(self, event, combobox):
        self.form.insert_attribute(-1, combobox.GetValue(), combobox.GetValue())
