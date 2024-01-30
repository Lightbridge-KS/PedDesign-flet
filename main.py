import flet as ft
import pyperclip
from flet import (
    Container,
    Column,
    Row,
    ResponsiveRow,
    Page
)
import peddesign
from utils import attempt_float

# Lookup Dict
study_type_dict = {
    "CT Chest": "chest",
    "CTWA": "whole_abd",
    "CT Chest + WA": "chest_whole_abd",
    "CTA Liver": "cta_liver",
    "HRCT": "hrct"
}

is_first_study_dict = {"Not First Study": False, "First Study": True}

rate_formula_dict = {
    False: "no_delay",
    True: "delay"
}

# Input Component
class InputDesign(ft.UserControl):
    def __init__(self):
        super().__init__()
        ## Study Type
        self.input_study_type = ft.Dropdown(
            label="Study type", hint_text="Type of study",
            options= [ft.dropdown.Option(k) for k in study_type_dict.keys()],
            on_change= self.input_study_type_changed,
        )
        ## Is first study
        self.input_is_first_study = ft.Dropdown(
            label="Occasion", hint_text="Is this the 1st study?",
            options= [ft.dropdown.Option(k) for k in is_first_study_dict.keys()]
        )
        ## Weight 
        self.input_weight_kg = ft.TextField(label="Weight (kg)", hint_text="Body weight in kg")
        ## Custom Delayed Time (rate_formula) ?
        self.input_rate_formula = ft.Switch(label="Choose custom delayed time", value=False, disabled=True, 
                                            on_change=self.input_rate_formula_changed)
        ## Delayed Time (delay_sec)
        self.input_delay_sec = ft.TextField(label="Delayed time (sec)", hint_text="Delayed time in sec", disabled=True)
        
    def build(self):
        return Container(
            content=Column(
                [self.input_study_type,
                 self.input_is_first_study,
                 self.input_weight_kg,
                 self.input_rate_formula,
                 self.input_delay_sec]
            )
        )
        
    def _log(self):
        return f"get(): {self.get()}"
    
    ## If study type is "whole_abd", "chest_whole_abd" -> not disable `input_rate_formula`
    def input_study_type_changed(self, e):
        is_std_type_enable = self.get_study_type() in ["whole_abd", "chest_whole_abd"]
        self.input_rate_formula.disabled = False if is_std_type_enable else True
        self.input_rate_formula.update()
        
        ## Update `input_delay_sec` if not choosing "whole_abd", "chest_whole_abd"
        if not is_std_type_enable:
            self.input_delay_sec.disabled = True
            self.input_delay_sec.update()
        
    ## If `input_rate_formula` is `True` -> not disable `input_delay_sec`
    def input_rate_formula_changed(self, e):
        is_rf = self.input_rate_formula.value
        self.input_delay_sec.disabled = False if is_rf else True
        self.input_delay_sec.update()
    ## Get Study Type
    def get_study_type(self):
        return study_type_dict[self.input_study_type.value]
    ## Get All Selected Input Values
    def get(self):
        out = {
            "study_type": study_type_dict[self.input_study_type.value],
            "weight_kg": attempt_float(self.input_weight_kg.value),
            "is_first_study": is_first_study_dict[self.input_is_first_study.value],
            "rate_formula": rate_formula_dict[self.input_rate_formula.value],
            "delay_sec": attempt_float(self.input_delay_sec.value)
        }
        return out
    
def main(page: Page):
    # Input Group
    input_design = InputDesign()
    ## Calculation
    def get_text_output():
        input_dict = input_design.get()
        # Design CT as String
        text_output = peddesign.design_ct_str(**input_dict)
        return text_output
    def _log():
        print("Btn clicked")
        print(input_design._log())
        print(get_text_output())        
    ## Button Clicked 
    def button_gen_clicked(e):
        _log()
        output_text_field.value = get_text_output()
        output_text_field.focus()
        output_text_field.update()
    ## Copy Clicked 
    def button_cp_clicked(e):
        pyperclip.copy(output_text_field.value)
    ## Theme
    def theme_changed(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()
        
        
    # Title & App Bar
    page.title = "Design Pediatric CT Protocol"
    page.appbar = ft.CupertinoAppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        bgcolor=ft.colors.SURFACE_VARIANT,
        middle=ft.Text("Design Pediatric CT Protocol", weight=ft.FontWeight.BOLD),
        trailing=ft.IconButton(icon=ft.icons.BRIGHTNESS_2_OUTLINED,
                               tooltip="Toggle theme",
                               on_click=theme_changed)
    )
    
    page.window_min_width = 400
    page.window_width = 655
    page.window_min_height = 470
    page.window_height = 470
    # Button
    btn = ft.ElevatedButton(text="Generate", on_click=button_gen_clicked)
    
    # Output Text Field
    txt_size = 14 # 14
    output_text_field = ft.TextField(value="\n"*txt_size, multiline=True, read_only=False, text_size=txt_size,
                                     min_lines=txt_size+1, max_lines=txt_size+1) 
    # Copy Button
    btn_copy = ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    icon_size=20,
                    tooltip="Copy output",
                    on_click=button_cp_clicked
                    )
    
    # UI
    rr = ResponsiveRow(
            controls=[
                Column(col={"sm": 6},
                       controls=[
                        # ft.Text("Choose:", theme_style=ft.TextThemeStyle.HEADLINE_SMALL, weight=ft.FontWeight.NORMAL),
                        input_design,
                        Row([btn, btn_copy], alignment=ft.MainAxisAlignment.START)
                        ], 
                       alignment=ft.MainAxisAlignment.START
                ),
                Column(col={"sm": 6}, 
                       controls=[output_text_field],
                       alignment=ft.MainAxisAlignment.START
                )
            ]
        )
    lv = ft.ListView(controls=[rr], 
                     expand=1, spacing=5, padding=10, auto_scroll=False)
    
    page.add(lv)
    

if __name__ == "__main__":
    ft.app(target=main)