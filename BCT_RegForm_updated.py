import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import os


PER_UNIT = 459.54
LAB_FEE = 3429.30
HANDS_ON_FEE = 2341.86
ROWS = 10


BG = "#fdf5ec"         
CARD = "#ffffff"
ACCENT = "#d9570b"     
ACCENT_DARK = "#b04508"
GOLD = "#f5a45d"       
TEXT = "#26262b"
MUTED = "#80705f"
BORDER = "#efd9c3"
HEAD = "#fde6cf"
TINT = "#fff4e6"
ROW_ALT = "#fffaf3"
FOCUS = "#ffe8c7"
LIGHT_ON_ACCENT = "#ffe4cc"

SERIF = "Georgia"
SANS = "Segoe UI"
F_BODY = (SANS, 10)
F_BOLD = (SANS, 10, "bold")
F_CAP = (SANS, 7, "bold")
F_SMALL = (SANS, 8)


def num(text):
    """Convert text to float safely (handles commas / blanks)."""
    try:
        return float(str(text).replace(",", "").strip())
    except ValueError:
        return 0.0


def money(value):
    return f"{value:,.2f}"


class RegistrationForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baguio College of Technology — Preliminary Registration Form")
        self.configure(bg=BG)
        self.fees_filled = False
        self.vars = {}
        self.unit_vars = []

        self.build_header()
        self.build_footer()
        self.build_scroll_area()

        self.build_student_info()
        self.build_subjects()
        self.build_bottom()

        self.size_window()

    def card(self, parent, title):
        outer = tk.Frame(parent, bg=BORDER)
        inner = tk.Frame(outer, bg=CARD)
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        head = tk.Frame(inner, bg=CARD)
        head.pack(fill="x", padx=16, pady=(12, 0))
        tk.Label(head, text=title, bg=CARD, fg=ACCENT,
                 font=(SERIF, 11, "bold")).pack(side="left")
        tk.Frame(head, bg=GOLD, height=1).pack(side="left", fill="x",
                                               expand=True, padx=(12, 0), pady=(3, 0))
        body = tk.Frame(inner, bg=CARD)
        body.pack(fill="both", expand=True, padx=16, pady=(8, 14))
        return outer, body

    def field(self, parent, caption, key, readonly=False, justify="left"):
        """Caption above an entry that has only an underline (form-like)."""
        bg = parent.cget("bg")
        f = tk.Frame(parent, bg=bg)
        tk.Label(f, text=caption.upper(), bg=bg, fg=MUTED, font=F_CAP).pack(anchor="w")
        var = tk.StringVar()
        self.vars[key] = var
        e = tk.Entry(f, textvariable=var, relief="flat", bd=0, bg=bg,
                     readonlybackground=bg, fg=TEXT, insertbackground=ACCENT,
                     font=F_BODY, justify=justify,
                     state="readonly" if readonly else "normal")
        e.pack(fill="x", pady=(3, 0), ipady=2)
        line = tk.Frame(f, height=1, bg=BORDER)
        line.pack(fill="x")
        e.bind("<FocusIn>", lambda ev: line.config(bg=ACCENT))
        e.bind("<FocusOut>", lambda ev: line.config(bg=BORDER))
        return f

    def fee_row(self, parent, row, text, key, readonly=False, bold=False):
        tk.Label(parent, text=text, bg=CARD, fg=ACCENT if bold else TEXT,
                 font=F_BOLD if bold else F_BODY, anchor="w").grid(
            row=row, column=0, sticky="w", pady=3, padx=(0, 14))
        var = tk.StringVar()
        self.vars[key] = var
        bg = TINT if readonly else "#ffffff"
        e = tk.Entry(parent, textvariable=var, width=14, justify="right",
                     relief="flat", bg=bg, readonlybackground=bg, fg=TEXT,
                     insertbackground=ACCENT, font=F_BOLD if bold else F_BODY,
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT,
                     state="readonly" if readonly else "normal")
        e.grid(row=row, column=1, sticky="ew", pady=3, ipady=3)
        return e

    def divider(self, parent, row):
        tk.Frame(parent, bg=BORDER, height=1).grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=5)

    def button(self, parent, text, command, primary=False):
        if primary:
            b = tk.Button(parent, text=text, command=command, bg=ACCENT, fg="white",
                          activebackground=ACCENT_DARK, activeforeground="white",
                          relief="flat", bd=0, font=F_BOLD, padx=20, pady=7,
                          cursor="hand2")
            b.bind("<Enter>", lambda e: b.config(bg=ACCENT_DARK))
            b.bind("<Leave>", lambda e: b.config(bg=ACCENT))
        else:
            b = tk.Button(parent, text=text, command=command, bg=CARD, fg=ACCENT,
                          activebackground=HEAD, activeforeground=ACCENT,
                          relief="flat", bd=0, font=F_BOLD, padx=18, pady=7,
                          highlightthickness=1, highlightbackground=ACCENT,
                          cursor="hand2")
            b.bind("<Enter>", lambda e: b.config(bg=HEAD))
            b.bind("<Leave>", lambda e: b.config(bg=CARD))
        return b

    def build_header(self):
        band = tk.Frame(self, bg=ACCENT)
        band.pack(fill="x", side="top")

        inner = tk.Frame(band, bg=ACCENT)
        inner.pack(fill="x", padx=24, pady=14)

        logo = tk.Canvas(inner, width=70, height=70, bg=ACCENT, highlightthickness=0)
        logo.grid(row=0, column=0, rowspan=4, padx=(0, 16))
        self.logo_img = None
        try:
            from PIL import Image, ImageTk, ImageDraw
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bct.jpg")
            img = Image.open(path).convert("RGBA")
            resample = getattr(Image, "Resampling", Image).LANCZOS
            img = img.resize((70, 70), resample)
            mask = Image.new("L", (70, 70), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 69, 69), fill=255)
            img.putalpha(mask)
            self.logo_img = ImageTk.PhotoImage(img)
            logo.create_image(35, 35, image=self.logo_img)
        except Exception:
            logo.create_oval(3, 3, 67, 67, fill="white", outline=GOLD, width=2)
            logo.create_text(35, 35, text="BCT", fill=ACCENT, font=(SERIF, 14, "bold"))

        tk.Label(inner, text="BAGUIO COLLEGE OF TECHNOLOGY", bg=ACCENT, fg="white",
                 font=(SERIF, 19, "bold")).grid(row=0, column=1, sticky="w")
        tk.Label(inner, text="37 Harrison Rd., Baguio City, Philippines", bg=ACCENT,
                 fg=LIGHT_ON_ACCENT, font=F_SMALL).grid(row=1, column=1, sticky="w")
        tk.Label(inner, text="Tel. Nos.: (074) 442-3743 / 424-0859 / 424-2036",
                 bg=ACCENT, fg=LIGHT_ON_ACCENT, font=F_SMALL).grid(row=2, column=1, sticky="w")
        tk.Label(inner, text="www.bct.edu.ph", bg=ACCENT, fg=LIGHT_ON_ACCENT,
                 font=F_SMALL).grid(row=3, column=1, sticky="w")

        inner.columnconfigure(2, weight=1)
        right = tk.Frame(inner, bg=ACCENT)
        right.grid(row=0, column=2, rowspan=4, sticky="e")
        tk.Label(right, text="COLLEGE", bg=ACCENT, fg="white",
                 font=(SERIF, 16, "bold")).pack(anchor="e")
        tk.Label(right, text="PRELIMINARY REGISTRATION FORM", bg=ACCENT, fg="white",
                 font=(SERIF, 12, "bold")).pack(anchor="e")
        tk.Label(right, text="Student's Copy", bg=ACCENT,
                 fg=LIGHT_ON_ACCENT, font=F_SMALL).pack(anchor="e", pady=(2, 0))

        tk.Frame(self, bg=GOLD, height=3).pack(fill="x", side="top")

    def build_footer(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", side="bottom")
        tk.Frame(bar, bg=BORDER, height=1).pack(fill="x")
        row = tk.Frame(bar, bg=BG)
        row.pack(fill="x", padx=24, pady=10)

        tk.Label(row, text="Reg. Form 18  ·  Rev. 2  ·  2009", bg=BG, fg=MUTED,
                 font=F_SMALL).pack(side="left")
        self.button(row, "Compute Fees", self.compute_fees, primary=True).pack(side="right")
        self.button(row, "Recalculate", self.recalculate).pack(side="right", padx=8)
        self.button(row, "Clear Form", self.clear_all).pack(side="right")

    def build_scroll_area(self):
        mid = tk.Frame(self, bg=BG)
        mid.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(mid, bg=BG, highlightthickness=0)
        vsb = ttk.Scrollbar(mid, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.body = tk.Frame(self.canvas, bg=BG)
        win = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>",
                       lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(win, width=e.width))

        self.bind_all("<MouseWheel>", self.on_wheel)
        self.bind_all("<Button-4>", self.on_wheel)
        self.bind_all("<Button-5>", self.on_wheel)

    def on_wheel(self, e):
        if self.canvas.yview() == (0.0, 1.0):
            return
        if getattr(e, "num", None) == 4:
            step = -1
        elif getattr(e, "num", None) == 5:
            step = 1
        else:
            step = -1 if e.delta > 0 else 1
        self.canvas.yview_scroll(step, "units")

    def size_window(self):
        self.update_idletasks()
        w = max(self.body.winfo_reqwidth() + 24, 980)
        chrome = self.winfo_reqheight() - self.canvas.winfo_reqheight()
        h = min(self.body.winfo_reqheight() + chrome, self.winfo_screenheight() - 110)
        self.geometry(f"{w}x{h}+{max((self.winfo_screenwidth() - w) // 2, 0)}+20")
        self.minsize(820, 480)

    def build_student_info(self):
        outer, b = self.card(self.body, "Student Information")
        outer.pack(fill="x", padx=24, pady=(18, 10))

        for c in range(4):
            b.columnconfigure(c, weight=1, uniform="col")

        def place(widget, r, c, span=1):
            widget.grid(row=r, column=c, columnspan=span, sticky="ew", padx=8, pady=6)

        # Row 0: Date (top right)
        place(self.field(b, "Date", "date"), 0, 3)

        # Row 1: Semester / School Year / Summer
        place(self.field(b, "Semester", "sem"), 1, 0)
        place(self.field(b, "School Year", "sy"), 1, 1, 2)
        place(self.field(b, "Summer", "summer"), 1, 3)

        # Row 2: ID No. / Course / Major / Year Level
        place(self.field(b, "ID No.", "id"), 2, 0)
        place(self.field(b, "Course", "course"), 2, 1)
        place(self.field(b, "Major", "major"), 2, 2)
        place(self.field(b, "Year Level", "year"), 2, 3)

        # Row 3: Name (Family / First / Middle)
        place(self.field(b, "Family Name", "family"), 3, 0)
        place(self.field(b, "First Name", "first"), 3, 1)
        place(self.field(b, "Middle Name", "middle"), 3, 2)

        self.vars["date"].set(date.today().strftime("%m/%d/%Y"))

        # Row 4: enrollment status + scholarship
        st = tk.Frame(b, bg=CARD)
        st.grid(row=4, column=0, columnspan=2, sticky="w", padx=8, pady=(8, 2))
        tk.Label(st, text="ENROLLMENT STATUS", bg=CARD, fg=MUTED, font=F_CAP).grid(
            row=0, column=0, columnspan=4, sticky="w")
        self.status = {}
        for i, t in enumerate(["New", "Old", "Transferee", "Cross Enrollee"]):
            v = tk.BooleanVar()
            self.status[t] = v
            tk.Checkbutton(st, text=t, variable=v, bg=CARD, fg=TEXT,
                           activebackground=CARD, activeforeground=ACCENT,
                           selectcolor="white", font=F_BODY, bd=0,
                           highlightthickness=0).grid(row=1, column=i, sticky="w",
                                                      padx=(0, 12), pady=(3, 0))
        place(self.field(b, "Scholarship", "scholarship"), 4, 2, 2)

    def build_subjects(self):
        outer, b = self.card(self.body, "Enrolled Subjects")
        outer.pack(fill="x", padx=24, pady=10)

        wrapper = tk.Frame(b, bg=BORDER, padx=1, pady=1)
        wrapper.pack(fill="x")
        t = tk.Frame(wrapper, bg=BORDER)
        t.pack(fill="x")

        cols = [("Class Code", 12), ("Descriptive Title", 40), ("Time", 14),
                ("Day(s)", 9), ("Room", 9), ("Unit(s)", 7)]
        for c, (name, w) in enumerate(cols):
            tk.Label(t, text=name.upper(), bg=HEAD, fg=ACCENT, font=F_CAP,
                     pady=7).grid(row=0, column=c, sticky="nsew", padx=(0, 1), pady=(0, 1))
        t.columnconfigure(1, weight=1)

        self.table = []
        for r in range(1, ROWS + 1):
            rowbg = CARD if r % 2 else ROW_ALT
            row = []
            for c, (_, w) in enumerate(cols):
                var = tk.StringVar()
                e = tk.Entry(t, textvariable=var, width=w, relief="flat", bd=0,
                             bg=rowbg, fg=TEXT, insertbackground=ACCENT,
                             font=F_BODY, highlightthickness=0,
                             justify="left" if c == 1 else "center")
                e.grid(row=r, column=c, sticky="ew", padx=(0, 1), pady=(0, 1), ipady=4)
                e.bind("<FocusIn>", lambda ev, w_=e: w_.config(bg=FOCUS))
                e.bind("<FocusOut>", lambda ev, w_=e, bg_=rowbg: w_.config(bg=bg_))
                row.append(var)
                if c == 5:
                    self.unit_vars.append(var)
            self.table.append(row)

        tot = tk.Frame(b, bg=CARD)
        tot.pack(fill="x", pady=(10, 0))
        self.total_units = tk.StringVar(value="0")
        tk.Label(tot, textvariable=self.total_units, bg=ACCENT, fg="white",
                 font=(SERIF, 12, "bold"), width=6, pady=3).pack(side="right")
        tk.Label(tot, text="TOTAL UNIT(S)", bg=CARD, fg=ACCENT, font=F_CAP).pack(
            side="right", padx=10)

    def build_bottom(self):
        row = tk.Frame(self.body, bg=BG)
        row.pack(fill="x", padx=24, pady=(10, 20))
        row.columnconfigure(0, weight=2, uniform="b")
        row.columnconfigure(1, weight=3, uniform="b")

        # ---- Left: Assessment of Fees ----
        fo, fb = self.card(row, "Assessment of Fees")
        fo.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        fb.columnconfigure(1, weight=1)
        self.fee_row(fb, 0, "Tuition", "tuition", readonly=True)
        self.fee_row(fb, 1, "Laboratory Fee", "lab", readonly=True)
        self.fee_row(fb, 2, "Hands-on Fee", "hands", readonly=True)
        self.fee_row(fb, 3, "Miscellaneous Fee", "misc")
        self.divider(fb, 4)
        self.fee_row(fb, 5, "Total Assessed Fee", "assessed", readonly=True, bold=True)
        self.fee_row(fb, 6, "Less: Discount", "discount")
        self.fee_row(fb, 7, "Net Amount", "net", readonly=True)
        self.fee_row(fb, 8, "Previous Balance", "prev")
        self.divider(fb, 9)
        self.fee_row(fb, 10, "TOTAL", "total", readonly=True, bold=True)
        tk.Label(fb, text="All amounts in Philippine Peso (PHP)", bg=CARD, fg=MUTED,
                 font=F_SMALL).grid(row=11, column=0, columnspan=2, sticky="w", pady=(8, 0))
        self.field(fb, "Assessed by", "assessed_by").grid(
            row=12, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        # ---- Right: Initial Payment on top, Certification below ----
        right = tk.Frame(row, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right.columnconfigure(0, weight=1)

        po, pb = self.card(right, "Initial Payment")
        po.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        for c in range(3):
            pb.columnconfigure(c, weight=1, uniform="pay")
        self.field(pb, "O.R. No.", "or_no").grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=5)
        self.field(pb, "Amount", "initial", justify="right").grid(
            row=0, column=1, sticky="ew", padx=8, pady=5)
        self.field(pb, "Date", "pay_date").grid(row=0, column=2, sticky="ew", padx=(8, 0), pady=5)

        panel = tk.Frame(pb, bg=ACCENT)
        panel.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(12, 0))
        tk.Label(panel, text="REMAINING BALANCE", bg=ACCENT, fg=LIGHT_ON_ACCENT,
                 font=F_CAP).pack(side="left", padx=14, pady=10)
        self.vars["balance"] = tk.StringVar(value="—")
        tk.Label(panel, textvariable=self.vars["balance"], bg=ACCENT, fg="white",
                 font=(SERIF, 18, "bold")).pack(side="right", padx=14, pady=8)

        co, cb = self.card(right, "Certification")
        co.grid(row=1, column=0, sticky="nsew")
        right.rowconfigure(1, weight=1)
        cb.columnconfigure(0, weight=1, uniform="cert")
        cb.columnconfigure(1, weight=1, uniform="cert")

        note = tk.Frame(cb, bg=CARD)
        note.grid(row=0, column=0, sticky="nw", padx=(0, 12))
        tk.Label(note, text="PROMISSORY NOTE", bg=CARD, fg=MUTED, font=F_CAP).pack(anchor="w")
        tk.Label(note, bg=CARD, fg=TEXT, font=(SANS, 8, "italic"), justify="left",
                 wraplength=230,
                 text="I hereby agree to pay all the assessed fees, even if I stop "
                      "studying. I am fully aware that MISCELLANEOUS FEES and TUITION "
                      "FEES paid by installment are NOT REFUNDABLE.").pack(anchor="w", pady=(3, 0))

        sign = tk.Frame(cb, bg=CARD)
        sign.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        sign.columnconfigure(0, weight=1)
        self.field(sign, "Student's Signature", "signature").grid(row=0, column=0, sticky="ew", pady=5)
        self.field(sign, "Enrollment Adviser", "adviser").grid(row=1, column=0, sticky="ew", pady=5)
        tk.Label(sign, text="APPROVED BY", bg=CARD, fg=MUTED, font=F_CAP).grid(
            row=2, column=0, sticky="w", pady=(8, 0))
        tk.Label(sign, text="LIGAYA R. ABAD, MBA, MBE", bg=CARD, fg=ACCENT,
                 font=(SERIF, 10, "bold")).grid(row=3, column=0, sticky="w", pady=(2, 0))
        tk.Label(sign, text="Registrar", bg=CARD, fg=MUTED, font=F_SMALL).grid(
            row=4, column=0, sticky="w")

    def set(self, key, value):
        self.vars[key].set(value)

    def get_total_units(self):
        return sum(num(v.get()) for v in self.unit_vars)

    def compute_fees(self, silent=False):
        units = self.get_total_units()
        if units <= 0 and not silent:
            messagebox.showwarning("No units", "Enter the units of your subjects first.")
            return

        # Total units are only calculated when the button is clicked.
        self.total_units.set(f"{units:g}")

        self.set("tuition", money(units * PER_UNIT))
        self.set("lab", money(LAB_FEE))
        self.set("hands", money(HANDS_ON_FEE))

        for k in ("misc", "discount", "prev"):
            if not self.vars[k].get().strip():
                self.set(k, "0.00")

        self.fees_filled = True

        # Update the assessment totals, but DO NOT calculate the
        # remaining balance automatically.
        self.update_assessment()
        self.set("balance", "—")

    def update_assessment(self):
        assessed = (
            num(self.vars["tuition"].get())
            + num(self.vars["lab"].get())
            + num(self.vars["hands"].get())
            + num(self.vars["misc"].get())
        )
        net = assessed - num(self.vars["discount"].get())
        total = net + num(self.vars["prev"].get())

        self.set("assessed", money(assessed))
        self.set("net", money(net))
        self.set("total", money(total))

    def recalculate(self):
        if not self.fees_filled:
            messagebox.showwarning(
                "Compute Fees First",
                "Click 'Compute Fees' first before recalculating the remaining balance."
            )
            return

        # Recalculate all fee totals using the current entries.
        self.update_assessment()

        total = num(self.vars["total"].get())
        initial = num(self.vars["initial"].get())
        balance = total - initial

        # The remaining balance is shown/updated ONLY after
        # the user explicitly presses the Recalculate button.
        self.set("balance", money(balance))

    def clear_all(self):
        if not messagebox.askyesno("Clear form", "Clear the whole form?"):
            return
        self.fees_filled = False
        for v in self.vars.values():
            v.set("")
        self.set("date", date.today().strftime("%m/%d/%Y"))
        self.set("balance", "—")
        for row in self.table:
            for v in row:
                v.set("")
        for v in self.status.values():
            v.set(False)
        self.total_units.set("0")


if __name__ == "__main__":
    RegistrationForm().mainloop()
