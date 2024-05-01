import os
from typing import TypeVar

import pandas as pd
import seaborn as sns

from alias import c
from classificators import BMI_ranges, age_binding
from custom import fix_places

sns.set_theme(style="whitegrid", rc={"figure.figsize": (14, 8), "axes.labelsize": 15})
sns_api = {"height": 6, "aspect": 1.75}
pic_path = "report/assets"
pic_ext = ".pdf"
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
    "responses_file" : "responses.csv",
    "preload_alias" : "%%PRELOAD%%",
    "payload_alias" : "\\iffalse PAYLOAD \\fi",
    "postload_alias" : "%%POSTLOAD%%",
    "decorator" : [],
    "lock" : False,
    "watermark" : True,
    "assets_folder" : os.path.abspath("data/static"),
    "templates_folder" : os.path.abspath(templates_folder),
    "templates" : {
        "scheme" : template("document.tex"),
        "table" : template("table.tex"),
        "desctable" : template("desctable.tex"),
        "powertable" : template("desctable.tex"),
        "counttable" : template("desctable.tex"),
        "expandtable" : template("desctable.tex"),
        "crosstable" : template("desctable.tex"),
        "plot" : template("graphic.tex"),
        "powerplot" : template("graphic.tex"),
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
    "compile" : {
        "method" : "latex",
        "executable" : "pdflatex",
        "options" : "",
    },
    "ai" : {
        'mode' : 'uniqe',
        'model' : "gpt-3.5-turbo-0125",
        # 'system': "Jesteś statystykiem który pisze raport statystyczny na temat występowaniu bólu kręgosłupa u pielegniarek i jak to wpływa na ich życie, tworzysz opisy do tabel i wykresów, nie przekraczaj 300 słów, nie sugeruj nic, ma być ściśle, po prostu opisuj to co widzisz w tabeli, np. dostajesz informacje że tabela to odpowiedzi na jakies pytanie i twoim zadaniem jest tylko opisać tą tabele np. średni wzrost w grupie to X, odchylenie Y, najszęsciej występuje odpowiedz C itp. NIE zaczynaj zdania od przykładowo 'w badaniiu przeprowadzonym na grupie pielegniarek...' odrazu pisz o wartosciach z tabeli, bez żadnych wstępów",
        'system': "Udawaj, że jesteś naukowcem, postaraj się parafrazować wysyłane ci zdania w bardziej profesjonalny styl, Odmieniaj odpowienio nazwy zmiennych np. 'tabela krzyżowa między wartością (Kategoria wiekowa) a (Czy przerwy w pracy są wystarczające) zawiera X'  na 'w tabeli krzyżowej zawierającej kategorie wiekową respondentów w stosunku do pytania o wystarczające przerwy w pracy znajduje się X' itp."
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
    "Obowiązki domowe podczas bólu (czy jest w stanie)",
    "Praca zawodowa podczas bólu (czy jest w stanie)",
    "Czy unika akt. fiz. z obawy przed bólem",
    "Problemy ze snem podczas wyst. bólu",
    "Czy ból uniemożliwiał spotkania towarzyskie",
    "Czy ból powodował obniżenie nastroju",
    "Czy ból pogarsza jakość życia? (opinia)",
]


ind_data = [
    "Płeć",
    "Stan cywilny",
    "Rodzaj oddziału",
    "Dodatkowa praca",
    "Udogodnienia (w miejscu pracy)",
    "Prawidłowa postawa ciała w pracy",
    "Możliwość planowania przerw",
    "Czy środowisko pracy jest zdrowe? (opinia)",

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
]

quantitative_data = [
    "Wiek",
    "Wzrost [cm]",
    "Masa ciała [kg]",
    "Wartość BMI",
    "Ból VAS",
]
############################################
zw_metric = [
    "Płeć",
    "Wiek",
    "Wzrost [cm]",
    "Wartość BMI",
    "BMI",
]

socjo_col = [
    "Miejsce zamieszkania",
    "Stan cywilny",
]

metric_col = [
    "Płeć",
    "Wiek",
    "Kategoria wiekowa",
    "Wzrost [cm]",
    "Masa ciała [kg]",
    "Wartość BMI",
    "BMI",
]

# metric - pain_col
# metric - inpact

# socjo - pain /inpact
# job_col - pain
# job_col - inpact
# activity - pain/inpact

# pain - inpact

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
    "Dodatkowa praca",
    #   "Oddział",
    "Rodzaj oddziału",
    "Godziny przepracowane w tygodniu",
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


tmp1 = [
    "Dodatkowa praca",
    "Udogodnienia (w miejscu pracy)",
    "Czy przerwy są wystarczające? (opinia)",
    "Czy środowisko pracy jest zdrowe? (opinia)",
    "Czy praca jest wyczerpująca fizycznie? (opinia)",
    "Czy praca jest wyczerpująca psychicznie? (opinia)",
]


tmp2 = [
    "Obowiązki domowe podczas bólu (czy jest w stanie)",
    "Praca zawodowa podczas bólu (czy jest w stanie)",
    "Czy unika akt. fiz. z obawy przed bólem",
    "Problemy ze snem podczas wyst. bólu",
    "Czy ból uniemożliwiał spotkania towarzyskie",
    "Czy ból powodował obniżenie nastroju",
    "Czy ból pogarsza jakość życia? (opinia)",
]

cross = []


def structure(comm : T):
    """Define report structure."""
    ff = "file"
    ll = "load"
    gg = "gen"
    gd = "gendesc"
    ss = "static"

    ta = "table"
    pl = "plot"
    de = "desc"
    det = "desctable"
    cot = "counttable"
    ext = "expandtable"
    crt = "crosstable"
    fp = 'prompt'

    xr = "random"       # choice randomly from database
    xu = "uniqe"        # always regenerate description
    xg = "global"       # use global setting
    xs = "static"       # AI support disabled, using default values
    xp = "paraphrase"   # paraphrase existing description

    tex_structure = {
        "Metodyka Badań" : {
            "Pytania badawcze" : [
                comm.register(ff, de, "methods.tex", loc='pre'),
                comm.register(ff, de, "questions.tex"),
            ],
            "Metoda statystyczna" : [
                comm.register(ff, de, "methods.tex"),  # TODO SUMMARY STAT
                comm.register(gg, 'powertable', "None", alias='powertab'),  # TODO SUMMARY STAT
                comm.register(gd, de, "powertab", mode=xg, alias='powertabD'),
                comm.register(gg, 'powerplot', "None"),  # TODO SUMMARY STAT
                comm.register(ss, de, '\\newpage'),
            ],
        },
        "Dane metryczne" : {
            "Metryka" : {
                "Płeć" : [
                    comm.register(ff, de, "metric.tex", loc='pre'),
                    comm.register(gg, det, metric_col, loc='pre', mode=xg, alias='metricN'),
                    comm.register(gd, de, "metricN", loc='pre', mode=xg, alias='metricND'),

                    comm.register(ss, de, '\\newpage'),
                    comm.register(gd, de, "Plec", mode=xg, alias='PlecD'),
                    comm.register(gg, cot, "Płeć", mode=xg, alias='Plec'),
                ],
                "Wiek" : [
                    comm.register(gg, pl, ["Wiek"], alias='Wiek', plot={'hue': "Płeć"}),
                    comm.register(ss, de, 'Na potrzeby analizy, ankieterzy podzieleni zostali na kilka grup wiekowych (co 10 lat):'),
                    comm.register(gg, cot, "Kategoria wiekowa", mode=xg, alias='CAge'),
                    comm.register(ss, de, '\\newpage'),
                    comm.register(gd, de, "CAge", mode=xg, alias='CAgeD'),
                ],
                "BMI" : [
                    comm.register(gg, det, ['Wzrost [cm]'], mode=xg, alias='WzrostN', silent=True),
                    comm.register(gd, de, "WzrostN", mode=xg, alias='WzrostND'),
                    comm.register(gg, cot, "BMI", mode=xg, alias='CBMI'),
                    comm.register(gd, de, "CBMI", mode=xg, alias='CBMID'),
                    comm.register(ss, de, '\\newpage'),
                    # comm.register(gg, pl, ["Wartość BMI", "Wzrost [cm]"], alias='wzrost-bmi'),
                    comm.register(ss, de, 'TODO'),
                    # comm.register(gg, pl, ["Masa ciała [kg]", "Wzrost [cm]"], alias='wzrost-waga'),
                    comm.register(ss, de, '\\newpage'),
                ],
            },
            "Warunki socjodemograficzne" : {
                "Miejsce zamieszkania" : [
                    comm.register(gg, cot, "Miejsce zamieszkania", mode=xg, alias='zamieszkanie'),
                    comm.register(gd, de, "zamieszkanie", mode=xg, alias='zamieszkanieD'),
                    comm.register(ss, de, '\\newpage'),
                ],
                "Stan cywilny" : [
                    comm.register(gg, cot, "Stan cywilny", mode=xg, alias='stanc'),
                    comm.register(gd, de, "stanc", mode=xg, alias='stancD'),
                    comm.register(ss, de, '\\newpage'),
                ],
            },
            "Aktywność fizyczna" : [
                comm.register(gg, cot, "Aktywność fizyczna", mode=xg, alias='aktf'),
                comm.register(gd, de, "aktf", mode=xg, alias='aktfD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Ile minut aktywności fiz. w tyg.", mode=xg, alias='aktfm'),
                comm.register(gd, de, "aktfm", mode=xg, alias='aktfmD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, ext, "Rodzaj aktywności fizycznej", mode=xg, alias='aktfrm'),
                comm.register(gd, de, "aktfrm", mode=xg, alias='aktfrD'),
                comm.register(ss, de, '\\newpage'),
            ],
        },
        "Przegląd wyników ankiety" : {
            "Występowanie bólu kręgosłupa" : [
                comm.register(gg, cot, "Od jak dawna wyst. epizody bólowe", mode=xg, alias='boldawno'),
                comm.register(gd, de, "boldawno", mode=xg, alias='boldawnoD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Częstotliwość bólu", mode=xg, alias='bolF'),
                comm.register(gd, de, "bolF", mode=xg, alias='bolFD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, pl, ["Ból VAS"], alias='VAS'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, ext, "Charakter bólu", mode=xg, alias='bolcharakter'),
                comm.register(gd, de, "bolcharakter", mode=xg, alias='bolcharakterD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, ext, "Kiedy ból mija", mode=xg, alias='kiedymija'),
                comm.register(gd, de, "kiedymija", mode=xg, alias='kiedymijaD'),
                comm.register(ss, de, '\\newpage'),
            ],
            "Zatrudnienie i warunki pracy" : [
                comm.register(gg, cot, "Staż pracy", mode=xg, alias='stazp'),
                comm.register(gd, de, "stazp", mode=xg, alias='stazpD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Oddział", mode=xg, alias='odd'),
                comm.register(gd, de, "odd", mode=xg, alias='oddD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Rodzaj oddziału", mode=xg, alias='oddR'),
                comm.register(gd, de, "oddR", mode=xg, alias='oddRD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Godziny przepracowane w tygodniu", mode=xg, alias='godzt'),
                comm.register(gd, de, "godzt", mode=xg, alias='godztD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Prawidłowa postawa ciała w pracy", mode=xg, alias='postawa'),
                comm.register(gd, de, "postawa", mode=xg, alias='postawaD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Możliwość planowania przerw", mode=xg, alias='planowanieprzerw'),
                comm.register(gd, de, "planowanieprzerw", mode=xg, alias='planowanieprzerwD'),
                comm.register(ss, de, '\\newpage'),


                comm.register(gg, cot, "Praca pod presją czasu", mode=xg, alias='presja'),
                comm.register(gd, de, "presja", mode=xg, alias='presjaD'),
                comm.register(ss, de, '\\newpage'),


                comm.register(gg, cot, tmp1, mode=xg, alias='tmp1'),
                comm.register(gd, de, "tmp1", mode=xg, alias='tmp1D'),
                comm.register(ss, de, '\\newpage'),


                comm.register(gg, ext, "Aktywności poza pracą", mode=xg, alias='aktywnoscpoza'),
                comm.register(gd, de, "aktywnoscpoza", mode=xg, alias='aktywnoscpozaD'),
                comm.register(ss, de, '\\newpage'),
            ],
            "Wpływ bólu na fizyczne i psychiczne aspekty życia" : [
                comm.register(gg, ext, "Utrudnienia w ruchu podczas bólu w czynnościach:", mode=xg, alias='utrudnieniaruchu'),
                comm.register(gd, de, "utrudnieniaruchu", mode=xg, alias='utrudnieniaruchuD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, tmp2, mode=xg, alias='tmp2'),
                comm.register(gd, de, "tmp2", mode=xg, alias='tmp2D'),
                comm.register(ss, de, '\\newpage'),

            ],
        },
        "Analiza danych" : {
            "Związek występowania bólu kręgosłupa z wskaźnikami antropometrycznymi" : {
                "Charakterystyka bólu" : [
                    comm.register(ff, de, "analysis.tex", loc='pre'),
                    comm.register(ss, de, '\\newpage'),
                ],
                'Wpływ na funkcje fizyczne i psychiczne': [
                    comm.register(ss, de, '\\newpage'),
                ]
            },
            "Znaczenie uwarunkowań socjo-demograficznych" : {
                'Warunki socjalne a ból' : [
                    comm.register(ss, de, '\\newpage'),
                ],
                'Znaczenie zatrudnienia' : [
                    comm.register(ss, de, '\\newpage'),
                ],
            },
            "Wpływ bólu kręgosłupa na upośledzenie funkcji fizycznych i psychicznych" : [
                comm.register(ss, de, '\\newpage'),
            ],
            "Rola aktywności fizycznej" : [
                comm.register(ss, de, '\\newpage'),
            ],
        },
        "Wnioski" : [
            comm.register(ss, de, 'TODO'),
        ],
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
