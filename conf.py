import os
from typing import TypeVar

import pandas as pd
import seaborn as sns

from classificators import BMI_ranges, age_binding
from custom import fix_places

sns.set_theme(style="whitegrid", rc={"figure.figsize": (14, 8), "axes.labelsize": 15})
sns_api = {"height": 6, "aspect": 1.75}
pic_path = "report/assets"
pic_ext = "pdf"
tab_path = "report/tabs"
pval = 0.05


templates_folder = "views/"


def template(x):
    abs_path = os.path.abspath(templates_folder)
    return os.path.join(abs_path, x)


tex_config = {
    "folder" : "output/report",
    "filename" : "report",
    "ext" : ".tex",
    "responses" : "responses.csv",
    "preload_alias" : "%%PRELOAD%%",
    "payload_alias" : "\\iffalse PAYLOAD \\fi",
    "postload_alias" : "%%POSTLOAD%%",
    "decorator" : None,
    "lock" : False,
    "watermark" : True,
    "assets_folder" : os.path.abspath("data/static"),
    "templates_folder" : os.path.abspath(templates_folder),
    "templates" : {
        "scheme" : template("document.tex"),
        "table" : template("table.tex"),
        "plot" : template("graphic.tex"),
        "text" : template("text.tex"),
        "desc" : template("text.tex"),
    },
    "constants" : {
        "%%LANGUAGE%%" : "polish",
        "%%DOCUMENT_CLASS%%" : "article",
        "%%MARIGIN_TOP%%" : "2cm",
        "%%MARIGIN_BOTTOM%%" : "2cm",
        "%%MARIGIN_LEFT%%" : "3cm",
        "%%MARIGIN_RIGHT%%" : "3cm",
        "%%FONT%%" : "lmodern",  # examples https://www.overleaf.com/learn/latex/Font_typefaces

        "%%TITLE%%" : "Badanie wpływu bólu kręgosłupa na jakość życia wśród personelu pielęgniarskiego",
        "%%AUTHOR%%" : "Aleksandra Żaba",
    },
    "latex" : {
        "executable" : "pdflatex",
        "options" : "-interaction=indent",
    }

}

stat_tests = {
    "qq" : "pass"
}

crv = {
    "Very weak": 0,
    "Weak": 0.05,
    "Moderate": 0.1,
    "Strong": 0.15,
    "Very Strong": 0.25,
}

multiple_col = [
    "Aktywności poza pracą",
    "Utrudnienia w ruchu podczas bólu w czynnościach:",
    "Rodzaj aktywności fizycznej",
    "Charakter bólu",
    "Kiedy ból mija",
]

nominal_data = [
    "Płeć",
    "Stan cywilny",
    "Oddział",
    "Rodzaj oddziału",
    "Dodatkowa praca",
    "Udogodnienia (w miejscu pracy)",
    "Prawidłowa postawa ciała w pracy",
    "Możliwość planowania przerw",
    "Czy przerwy są wystarczające? (opinia)",
    "Czy środowisko pracy jest zdrowe? (opinia)",
    "Praca pod presją czasu",
    "Czy praca jest wyczerpująca fizycznie? (opinia)",
    "Czy praca jest wyczerpująca psychicznie? (opinia)",
    "Czy praca jest wyczerpująca fizycznie? (opinia)",
    "Czy praca jest wyczerpująca psychicznie? (opinia)",
    "Aktywności poza pracą",
    "Utrudnienia w ruchu podczas bólu w czynnościach:",
    "Obowiązki domowe podczas bólu (czy jest w stanie)",
    "Praca zawodowa podczas bólu (czy jest w stanie)",
    "Rodzaj aktywności fizycznej",
    "Czy unika akt. fiz. z obawy przed bólem",
    "Problemy ze snem podczas wyst. bólu",
    "Czy ból uniemożliwiał spotkania towarzyskie",
    "Czy ból powodował obniżenie nastroju",
    "Czy ból pogarsza jakość życia? (opinia)",
    "Charakter bólu",
    "Kiedy ból mija",
]

ordinal_data = [
    "Miejsce zamieszkania",
    "BMI",
    "Kategoria wiekowa",
    "Staż pracy",
    "Godziny przepracowane w tygodniu",
    "Od jak dawna wyst. epizody bólowe",
    "Częstotliwość bólu",
    "Aktywność fizyczna",
    "Ile minut aktywności fiz. w tyg.",
    "Ból VAS",
]

quantitative_data = [
    "Wiek",
    "Wzrost [cm]",
    "Masa ciała [kg]",
    "Wartość BMI",
]

metric_col = [
    "Płeć",
    "Wiek",
    "Kategoria wiekowa",
    "Wzrost [cm]",
    "Masa ciała [kg]",
    "Wartość BMI",
    "BMI",
    "Miejsce zamieszkania",
    "Stan cywilny",
]


inpact_col = [
    "Utrudnienia w ruchu podczas bólu w czynnościach:",
    "Obowiązki domowe podczas bólu (czy jest w stanie)",
    "Praca zawodowa podczas bólu (czy jest w stanie)",
    "Czy unika akt. fiz. z obawy przed bólem",
    "Problemy ze snem podczas wyst. bólu",
    "Czy ból uniemożliwiał spotkania towarzyskie",
    "Czy ból powodował obniżenie nastroju",
    "Czy ból pogarsza jakość życia? (opinia)",]

job_col = [
    "Staż pracy",
    "Oddział",
    "Rodzaj oddziału",
    "Godziny przepracowane w tygodniu",
    "Dodatkowa praca",
    "Udogodnienia (w miejscu pracy)",
    "Prawidłowa postawa ciała w pracy",
    "Możliwość planowania przerw",
    "Czy przerwy są wystarczające? (opinia)",
    "Czy środowisko pracy jest zdrowe? (opinia)",
    "Praca pod presją czasu",
    "Czy praca jest wyczerpująca fizycznie? (opinia)",
    "Czy praca jest wyczerpująca psychicznie? (opinia)",
    "Aktywności poza pracą",
]

pain_col = [
    "Od jak dawna wyst. epizody bólowe",
    "Częstotliwość bólu",
    "Ból VAS",
    "Charakter bólu",
    "Kiedy ból mija",

]

activity_col = [
    "Aktywność fizyczna",
    "Ile minut aktywności fiz. w tyg.",
    "Rodzaj aktywności fizycznej",
]

T = TypeVar("T")


def structure(comm : T):
    """Define report structure."""
    ff = "file"
    ll = "load"
    gg = "gen"

    ta = "table"
    pl = "plot"
    de = "desc"

    xr = "random"       # choice randomly from database
    xu = "uniqe"        # always regenerate description
    xg = "global"       # use global setting
    xs = "static"       # AI support disabled, using default values
    xp = "paraphrase"   # paraphrase existing description

    tex_structure = {
        "Metodyka Badań" : {
            "Pytania badawcze" : [
                comm.register(ff, de, "methods.tex",loc='pre'),
                comm.register(ff, de, "questions.tex"),
            ],
            "Metoda statystyczna" : [
                comm.register(ff, de, "methods.tex"),
                comm.register(ff, de, "questions.tex"),
            ],
        },
        "Dane metryczne" : {
            "Metryka" : {
                "Płeć" : [
                    comm.register(ff, de, "methods.tex"),
                    comm.register(ff, de, "questions.tex"),
                    comm.register(ff, de, "questions.tex"),
                ],
                "Wiek" : [
                    comm.register(ff, de, "methods.tex"),
                    comm.register(ff, de, "questions.tex"),
                ],
                "BMI" : [
                    comm.register(ff, de, "methods.tex"),
                    comm.register(ff, de, "questions.tex"),
                    comm.register(ff, de, "methods.tex",),
                    comm.register(ff, de, "questions.tex"),

                ],
            },
            "Warunki socjodemograficzne" : {
                "Miejsce zamieszkania" : [
                    comm.register(ff, de, "methods.tex"),
                    comm.register(ff, de, "questions.tex"),

                ],
                "Stan cywilny" : None,
            },
            "Aktywność fizyczna" : None,
        },
        "Przegląd wyników ankieyty" : {
            "Występowanie bólu kręgosłupa" : None,
            "Zatrudnienie i warunki pracy" : None,
            "Wpływ bólu na fizyczne i psychiczne aspekty życia" : None,
        },
        "Analiza danych" : {
            "Znaczenie uwarunkowań socjo-demograficznych" : None,
            "Wpływ bólu kręgosłupa na jakość życia" : None,
            "Wpływ bólu kręgosłupa na upośledzenie funkcji fizycznych i psychicznych" : None,
            "Związek występowania bólu kręgosłupa z wskaźnikami antropometrycznymi" : None,
        },
        "Wnioski" : None,
    }
    return tex_structure


def data_loader(data):
    """Load and prepare data."""
    df = pd.read_excel(data)
    pre_n = len(df)
    print("Loaded {} entries".format(pre_n))
    print("- Clearing nan values")
    df.dropna(inplace=True)
    df.reset_index()
    df["Ból VAS"] = df["Ból VAS"].astype(int)
    n = pre_n - len(df)
    print("\t - Droped {} entries {}%".format(n, round(len(df) / pre_n * 100)))
    print("- fixing duty column")
    #   df["Godziny przepracowane w tygodniu"] = df["Godziny przepracowane w tygodniu"].apply(duty_clear)
    print("- Converting multiple choice columns to list")
    for col in multiple_col:
        df[col] = df[col].apply(lambda x: x.split(";")[:-1])
    print("- Calc BMI values")
    df["Wartość BMI"] = df["Masa ciała [kg]"] / (df["Wzrost [cm]"] / 100) ** 2
    df["BMI"] = df["Wartość BMI"].apply(BMI_ranges)
    df["Kategoria wiekowa"] = df["Wiek"].apply(age_binding)
    print("- Cleared, numerical values description:")
    print("- Fixing places")
    df["Rodzaj oddziału"] = df["Oddział"].apply(fix_places)
    df[["Wiek", "Masa ciała [kg]", "Wzrost [cm]", "Wartość BMI"]].describe().round()
    return df
