import flet as ft

def main(page: ft.Page):
    page.padding = 50

    # This function triggers when a user clicks a suggestion
    def item_selected(e):
        result_text.value = f"You selected: {e.selection.value}"
        page.update()

    # Create the AutoComplete control
    autocomplete_field = ft.AutoComplete(
        suggestions=[
            ft.AutoCompleteSuggestion(key="apple", value="Apple"),
            ft.AutoCompleteSuggestion(key="banana", value="Banana"),
            ft.AutoCompleteSuggestion(key="blueberry", value="Blueberry"),
            ft.AutoCompleteSuggestion(key="cherry", value="Cherry"),
            ft.AutoCompleteSuggestion(key="grape", value="Grape"),
            ft.AutoCompleteSuggestion(key="mango", value="Mango"),
        ],
        on_select=item_selected,
    )

    result_text = ft.Text(size=16)

    # Add it to the page
    page.add(
        ft.Text("Type a fruit:"),
        autocomplete_field,
        result_text
    )

ft.app(target=main)