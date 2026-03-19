from fpdf import Align
from fpdf import FPDF


def create_blank_pdf() -> FPDF:
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    return pdf


def add_header(pdf) -> None:
    # Font and color
    pdf.set_font("helvetica", style="B", size=43)
    pdf.set_text_color(0, 0, 0)

    # Content
    header = "CS50 Shirtificate"

    # Add header
    pdf.cell(
        190,
        52,
        header,
        new_x="LMARGIN",
        new_y="NEXT",
        align="C",
    )


def add_shirt(pdf) -> None:
    pdf.image("shirt/shirtificate.png", Align.C, w=190, keep_aspect_ratio=True)


def add_title_on_shirt(pdf, user_name) -> None:
    # Font + color
    pdf.set_font("helvetica", style="B", size=20)
    pdf.set_text_color(255, 255, 255)

    # Content
    title = f"{user_name} took CS50"

    # Add title
    pdf.text(x=(210 - pdf.get_string_width(title)) // 2, y=125, text=title)


def main() -> None:
    # User's name
    user_name = input("Name: ").title()

    # Blank pdf
    pdf = create_blank_pdf()

    # Add parts
    add_header(pdf)
    add_shirt(pdf)
    add_title_on_shirt(pdf, user_name)

    # Save pdf
    pdf.output("shirt/shirtificate.pdf")


if __name__ == "__main__":
    main()
