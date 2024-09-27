import flet as ft
import lsb_steg


def main(page: ft.Page):
    def get_file(e: ft.FilePickerResultEvent):
        if e.files:
            nonlocal file_path
            file_path = e.files[0].path
            selected_file.value = e.files[0].name
            selected_file.update()
        else:
            "Cancelled"

    # input validation functions
    def dd_validation(dd, not_allowed):
        if dd.value == not_allowed:
            error = f"{dd.label} not selected."
            dlg_errors.content = ft.Text(f"{error}")
            open_dlg_errors()
            return False
        else:
            return True

    def text_validation(text, not_allowed):
        if text.value == not_allowed:
            error = f"{text.label} is empty."
            dlg_errors.content = ft.Text(f"{error}")
            open_dlg_errors()
            return False
        else:
            return True

    def number_validation(number, not_allowed):
        if not number.value.isnumeric() or int(number.value) < not_allowed:
            error = f"{number.label} must be a number greater than 0."
            dlg_errors.content = ft.Text(f"{error}")
            open_dlg_errors()
            return False
        else:
            return True

    def file_validation(file, not_allowed):
        if file == not_allowed:
            error = f"No file selected"
            dlg_errors.content = ft.Text(f"{error}")
            open_dlg_errors()
            return False
        else:
            return True

    def open_dlg_errors():
        page.dialog = dlg_errors
        dlg_errors.open = True
        page.update()

    def open_dlg_success():
        page.dialog = dlg_success
        dlg_success.open = True
        tb_encoded_message.value = ""
        tb_output_name.value = ""
        page.update()

    # encrypt/decrypt functions
    def steg_decrypt():
        if dd_validation(dd_bits, None) and dd_validation(tb_key, None) \
                and file_validation(file_path, "") and number_validation(tb_char, 1):
            tb1.value = lsb_steg.decrypt(dd_bits.value, tb_key.value, file_path, tb_char.value)
            tb1.update()

    def steg_encrypt():
        if dd_validation(dd_bits, None) and dd_validation(tb_key, None) \
                and file_validation(file_path, "") and text_validation(tb_encoded_message, "") \
                and text_validation(tb_output_name, ""):
            lsb_steg.encrypt(dd_bits.value, tb_key.value, file_path, tb_encoded_message.value, tb_output_name.value)
            open_dlg_success()

    def navigate(selection):
        nonlocal page_name
        page.clean()
        if selection == "Decoder":
            page_name = "Decoder"
            selected_file.value = ""
            nonlocal file_path
            file_path = ""
            decode(page)
        elif selection == "Encoder":
            page_name = "Encoder"
            selected_file.value = ""
            file_path = ""
            tb1.value = ""
            encode(page)
        page.update()

    # variables
    file_path = ''
    page_name = "Decoder"
    selected_file = ft.Text()
    pick_files_dialog = ft.FilePicker(on_result=get_file)  # initialize file picking object
    page.overlay.append(pick_files_dialog)  # appends the file picker over the page

    # text boxes
    tb1 = ft.TextField(label="Message Output", read_only=True, width=1000)
    tb_encoded_message = ft.TextField(label="Encoded Message", width=1000)
    tb_char = ft.TextField(label="Number of characters to read", value="0")
    tb_output_name = ft.TextField(label="Name of output file")
    tb_key = ft.TextField(label="Key")

    # dropdowns
    dd_selection = ft.Dropdown(
        label="Operation",
        width=150,
        options=[
            ft.dropdown.Option("Decoder"),
            ft.dropdown.Option("Encoder")
        ],
        value=page_name,
        on_change=lambda _: navigate(dd_selection.value)
    )

    dd_bits = ft.Dropdown(
        label="Bit-Encoding",
        width=150,
        options=[
            ft.dropdown.Option("7-bit"),
            ft.dropdown.Option("8-bit"),
        ]
    )

    # buttons
    b_file = ft.ElevatedButton(
        "Image to decode",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(file_type=ft.FilePickerFileType.IMAGE),
        height=50
    )

    b_file_encode = ft.ElevatedButton(
        "Image to encode",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_files_dialog.pick_files(file_type=ft.FilePickerFileType.IMAGE),
        height=50
    )

    b = ft.ElevatedButton(text="Decode",
                          on_click=lambda _: steg_decrypt(),
                          width=200, height=50)
    b_encode = ft.ElevatedButton(text="Encode",
                                 on_click=lambda _: steg_encrypt(),
                                 width=200, height=50)

    # dialog
    dlg_errors = ft.AlertDialog(title=ft.Text("Error"))
    dlg_success = ft.AlertDialog(content=ft.Text("Image successfully encoded"))

    # pages
    def decode(page: ft.Page):
        page.add(
            dd_selection,
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Decoder", size=50),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text("")]
                    ),
                    ft.Row(
                        [dd_bits, tb_key, tb_char, b_file, selected_file],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [tb1],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [b],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def encode(page: ft.Page):
        page.add(
            dd_selection,
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Encoder", size=50),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [ft.Text("")]
                    ),
                    ft.Row(
                        [dd_bits, tb_key, b_file_encode, selected_file],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [tb_encoded_message],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [tb_output_name],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [b_encode],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    # initialize route
    navigate("Decoder")

ft.app(target=main)
