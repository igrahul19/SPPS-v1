import flet as ft
from Triage_system.AI_api_call import calculate_risk_score,calculate_token_reduction
from Database.Database import *
from random import randint

def main(page: ft.Page):
    page.title = "SPPS"
    # page.bgcolor = "#242424"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.fonts = {
        "Impact": "/fonts/impact.ttf"
    }
    
    logo = ft.Image(
        src="icon.png",
        width=150,
        offset=ft.Offset(0, 1.2),
        animate_offset=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT)
    )
    form_t = ft.Text("New Token", font_family="Impact", size=40, opacity=0, animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT))
    name = ft.TextField(label="Full Name", expand=4, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(1600, ft.AnimationCurve.EASE_IN_OUT))
    age = ft.TextField(hint_text="Age", expand=1, text_align=ft.MainAxisAlignment.CENTER, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(1600, ft.AnimationCurve.EASE_IN_OUT), keyboard_type=ft.KeyboardType.NUMBER)
    temp = ft.TextField(hint_text="°F", expand=1, text_align=ft.MainAxisAlignment.CENTER, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(1600, ft.AnimationCurve.EASE_IN_OUT), keyboard_type=ft.KeyboardType.NUMBER)
    sex = ft.Dropdown(label="Sex", options=[
        ft.DropdownOption(key="Male", text="Male"),
        ft.DropdownOption(key="Female", text="Female")
    ], expand=1, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(1900, ft.AnimationCurve.EASE_IN_OUT))
    blood = ft.DropdownM2(label="Blood Group", options=[
        ft.DropdownOption(key="A+", text="A+"),
        ft.DropdownOption(key="A-", text="A-"),
        ft.DropdownOption(key="B+", text="B+"),
        ft.DropdownOption(key="B-", text="B-"),
        ft.DropdownOption(key="AB+", text="AB+"),
        ft.DropdownOption(key="AB-", text="AB-"),
        ft.DropdownOption(key="O+", text="O+"),
        ft.DropdownOption(key="O-", text="O-")
    ], expand=1, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(1900, ft.AnimationCurve.EASE_IN_OUT))
    num = ft.TextField(label="Mobile Number", expand=1, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(1900, ft.AnimationCurve.EASE_IN_OUT), keyboard_type=ft.KeyboardType.NUMBER)
    pregnancy = ft.Checkbox(label="Pregnant", offset=ft.Offset(-0.1,0), opacity=0, animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT))
    pwd = ft.Checkbox(label="PwD", offset=ft.Offset(-0.1,0), opacity=0, animate_opacity=ft.Animation(1900, ft.AnimationCurve.EASE_IN_OUT))

    sy1 = ft.TextField(label="Symptom #1", expand=1, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(2100, ft.AnimationCurve.EASE_IN_OUT))
    sy2 = ft.TextField(label="Symptom #2", expand=1, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(2100, ft.AnimationCurve.EASE_IN_OUT))
    sy3 = ft.TextField(label="Symptom #3", expand=1, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(2100, ft.AnimationCurve.EASE_IN_OUT))
    sy4 = ft.TextField(label="Others", expand=1, border_color=ft.Colors.GREY, opacity=0, animate_opacity=ft.Animation(2100, ft.AnimationCurve.EASE_IN_OUT))

    submit = ft.Button("Submit", icon=ft.Icons.CLOUD_UPLOAD, expand=1, opacity=0, animate_opacity=ft.Animation(3000, ft.AnimationCurve.EASE_IN_OUT))
    warn = ft.AlertDialog(
        title=ft.Text("Empty fields"),
        content=ft.Text("Please sign in again to continue."),
        actions=[ft.TextButton("Dismiss", on_click=lambda e: page.pop_dialog())],
    )

    form_t.disabled = True
    name.disabled = True
    age.disabled = True
    temp.disabled = True
    sex.disabled = True
    blood.disabled = True
    num.disabled = True
    pwd.disabled = True
    sy1.disabled = True
    sy2.disabled = True
    sy3.disabled = True
    sy4.disabled = True
    submit.disabled = True

    def reveal(e):
        logo.offset = ft.Offset(0, -0.3)
        create.opacity = 0

        form_t.disabled = False
        name.disabled = False
        age.disabled = False
        temp.disabled = False
        sex.disabled = False
        blood.disabled = False
        num.disabled = False
        pwd.disabled = False
        sy1.disabled = False
        sy2.disabled = False
        sy3.disabled = False
        sy4.disabled = False
        submit.disabled = False

        form_t.opacity = 1
        name.opacity = 1
        age.opacity = 1
        temp.opacity = 1
        sex.opacity = 1
        blood.opacity = 1
        num.opacity = 1
        pwd.opacity = 1
        sy1.opacity = 1
        sy2.opacity = 1
        sy3.opacity = 1
        sy4.opacity = 1        
        submit.opacity = 1        
    create = ft.Button("Create a New Token", scale=1.1, on_click=reveal, animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_IN_OUT))

    def preg(e):
        if sex.text == "Male":
            pregnancy.opacity = 0
            pregnancy.value = False
        elif sex.text == "Female":
            pregnancy.opacity = 1
    sex.on_text_change = preg


    def sub(e):
        if name.value == "" or age.value =="" or sex.value =="" or num.value == "" or sy1.value == "":
            page.show_dialog(warn)
            return
        info = {
            "name": name.value,
            "age" : age.value,
            "blood" : blood.value,
            "sex" : sex.value,
            "temp" : temp.value,
            "num" : num.value,
            "pwd" : pwd.value,
            "pregnancy" : pregnancy.value,
            "symptoms" : [sy1.value, sy2.value, sy3.value, sy4.value]
        }

        # Loading Screen
        form_t.value = "Loading..."
        name.opacity = 0
        age.opacity = 0
        temp.opacity = 0
        sex.opacity = 0
        blood.opacity = 0
        num.opacity = 0
        pwd.opacity = 0
        sy1.opacity = 0
        sy2.opacity = 0
        sy3.opacity = 0
        sy4.opacity = 0   
        submit.opacity = 0  

        risk_score = calculate_risk_score(info)
        total_number_people = current_number_of_people()
        token_number_reduction = calculate_token_reduction(total_number_people, risk_score)
        random_id = randint(1111,9999)
        insert_patient(id = random_id,pname=name.value,age=age.value,blood_group=blood.value, sex=sex.value, 
                       temperature=temp.value, mNumber=num.value, pregnancy=pregnancy.value, 
                       pwd=pwd.value, symptom=f"{[sy1.value, sy2.value, sy3.value, sy4.value]}",token_reduction=token_number_reduction)
        
        

    submit.on_click = sub


    page.add(
        ft.Row([logo], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([create], alignment=ft.MainAxisAlignment.CENTER, offset=ft.Offset(0, 3.8)),
        ft.Row([form_t], offset=ft.Offset(0, -1)),
        ft.Row([name, age, temp], offset=ft.Offset(0,-1.2)),
        ft.Row([sex, blood, num], offset=ft.Offset(0,-1.2)),
        ft.Row([pregnancy, pwd], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, offset=ft.Offset(0,-1.6)),
        ft.Row([sy1, sy2], offset=ft.Offset(0,-1.5)),
        ft.Row([sy3, sy4], offset=ft.Offset(0,-1.5)),
        ft.Row([submit])
    )
    

if __name__ == "__main__":
    ft.run(main)