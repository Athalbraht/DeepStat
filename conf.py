import numpy as np
import os
from typing import TypeVar


import pandas as pd
import seaborn as sns

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
        "corrtable" : template("desctable.tex"),
        "autostatable" : template("desctable.tex"),
        "counttable" : template("desctable.tex"),
        "expandtable" : template("desctable.tex"),
        "crosstable" : template("desctable.tex"),
        "statcorr" : template("desctable.tex"),
        "stattest" : template("desctable.tex"),
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
        'mode' : 'static',
        'model' : "gpt-3.5-turbo-0125",
        # 'system': "Jesteś statystykiem który pisze raport statystyczny na temat występowaniu bólu kręgosłupa u pielegniarek i jak to wpływa na ich życie, tworzysz opisy do tabel i wykresów, nie przekraczaj 300 słów, nie sugeruj nic, ma być ściśle, po prostu opisuj to co widzisz w tabeli, np. dostajesz informacje że tabela to odpowiedzi na jakies pytanie i twoim zadaniem jest tylko opisać tą tabele np. średni wzrost w grupie to X, odchylenie Y, najszęsciej występuje odpowiedz C itp. NIE zaczynaj zdania od przykładowo 'w badaniiu przeprowadzonym na grupie pielegniarek...' odrazu pisz o wartosciach z tabeli, bez żadnych wstępów",
        'system': "Udawaj, że jesteś naukowcem, postaraj się parafrazować wysyłane ci zdania w bardziej profesjonalny styl, Odmieniaj odpowienio nazwy zmiennych np. 'tabela krzyżowa między wartością (Kategoria wiekowa) a (Czy przerwy w pracy są wystarczające) zawiera X'  na 'w tabeli krzyżowej zawierającej kategorie wiekową respondentów w stosunku do pytania o wystarczające przerwy w pracy znajduje się X' itp. Jeśli chcesz coś wypnktować, używaj formatowania LaTex, czasem możesz dostać tabele w markdown, żeby opisać coś więcej co w niej widzisz. W odpowiedzi dawaj tylko tekst, bez prób dawania mi tablel."
    }

}

bool_col = ['Występowanie bólu',
            'Dodatkowa praca',
            'Udogodnienia (w miejscu pracy)',
            'Czy przerwy są wystarczające? (opinia)',
            'Czy środowisko pracy jest zdrowe? (opinia)',
            'Czy praca jest wyczerpująca fizycznie? (opinia)',
            'Czy praca jest wyczerpująca psychicznie? (opinia)',
            'Obowiązki domowe podczas bólu (czy jest w stanie)',
            'Praca zawodowa podczas bólu (czy jest w stanie)',
            'Czy unika akt. fiz. z obawy przed bólem',
            'Problemy ze snem podczas wyst. bólu',
            'Czy ból uniemożliwiał spotkania towarzyskie',
            'Czy ból powodował obniżenie nastroju',
            'Czy ból pogarsza jakość życia? (opinia)']


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

multiple_data = [
    "Aktywności poza pracą",
    "Utrudnienia w ruchu podczas bólu w czynnościach:",
    "Rodzaj aktywności fizycznej",
    "Charakter bólu",
    "Kiedy ból mija",
]

nominal_data = [
    "Płeć",
    "Kategoria wiekowa",
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

type_dict = {
    "n" : nominal_data,
    "o" : ordinal_data,
    "q" : quantitative_data,
    'multi' : multiple_data,
}

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


def corr_tab(cr):
    try:
        cr = cr.pivot_table(index='group', columns='value', values=['corr', 'p'])
    except:
        print('Failed to gen corr')
        return pd.DataFrame()
    finally:
        return cr.stack(0).unstack(1)


def tests_tab(ddf):
    tests = list(ddf.value_counts('tname').index)
    groups = list(ddf.value_counts('groups').index)
    tables = []
    for test in tests:
        for group in groups:
            try:
                df = ddf[(ddf['tname'] == test) & (ddf['groups'] == group)].reset_index()
                cols = df['fixed_col'].iloc[0]
                v = [df['values'].to_list()] + list(np.array(df['headers'].to_list()).T)
                gr = ['grupy'] + df['data'].iloc[0]
                d1 = ', '.join(df['data'].iloc[0][:2])
                d2 = ', '.join(df['data'].iloc[0][-3:])

                tab = pd.DataFrame(dict(zip(gr, v)))
                caption = "Test {} dla grupy {}. {} to kolejno mediana oraz rozstęp międzykwartylowy, {} - Wartość statystyki, p-value oraz wskaźnik siły efektu".format(
                    test, group, d1, d2)
                tables.append(tab)
            except:
                print('failed to gen stats {} {}'.format(test, group))

    return tables


def structure(comm : T, df, make_stat, power):
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

    xr = "reload"       # choice randomly from database
    xu = "uniqe"        # always regenerate description
    xg = "global"       # use global setting
    xs = "static"       # AI support disabled, using default values
    xp = "paraphrase"   # paraphrase existing description

    tex_structure = {
        "Wstęp" :
            {
                comm.register(ff, de, "doc.tex", mode=xr),
            },
        "Metodyka Badań" : {
            "Pytania badawcze" : [
                comm.register(ff, de, "methods.tex", loc='pre'),
                comm.register(ff, de, "questions.tex"),
            ],
            "Metoda statystyczna" : [
                comm.register(ff, de, "stats.tex"),  # TODO SUMMARY STAT
                comm.register(gg, 'powertable', "None", alias='powertab', mode=xr),  # TODO SUMMARY STAT
                comm.register(gd, de, "powertab", alias='powertabD'),
                comm.register(gg, 'powerplot', "None", mode=xr),  # TODO SUMMARY STAT
                comm.register(ss, de, '\\newpage'),
            ],
                },
        "Dane metryczne" : {
            "Metryka" : {
                "Płeć" : [
                    comm.register(ff, de, "metric.tex", loc='pre'),
                    comm.register(gg, det, metric_col, loc='pre', alias='metricN', mode=xr),
                    comm.register(gd, de, "metricN", loc='pre', alias='metricND'),

                    comm.register(ss, de, '\\newpage'),
                    comm.register(gd, de, "Plec", alias='PlecD'),
                    comm.register(gg, cot, "Płeć", alias='Plec', mode=xr),
                ],
                "Wiek" : [
                    comm.register(gg, pl, ["Wiek"], alias='Wiek', plot={'hue': "Płeć"}, mode=xr),
                    comm.register(ss, de, 'Na potrzeby analizy, ankieterzy podzieleni zostali na kilka grup wiekowych (co 10 lat):'),
                    comm.register(gg, cot, "Kategoria wiekowa", alias='CAge', mode=xr),
                    comm.register(ss, de, '\\newpage'),
                    comm.register(gd, de, "CAge", alias='CAgeD'),
                ],
                "BMI i wzrost" : [
                    comm.register(gg, det, ['Wzrost [cm]'], alias='WzrostN', silent=True, mode=xr),
                    comm.register(gd, de, "WzrostN", alias='WzrostND'),
                    comm.register(gg, pl, ["Płeć", "Wzrost [cm]"], alias='plec-wzrost', mode=xr),
                    # comm.register(gg, pl, ["Kategoria wiekowa", "Wzrost [cm]"], alias='wiek-wzrost'),
                    comm.register(gg, pl, ["Masa ciała [kg]", "Wzrost [cm]"], alias='wzrost-waga', mode=xr),
                    comm.register(gd, de, "CBMI", alias='CBMID'),
                    comm.register(gg, cot, "BMI", alias='CBMI', mode=xr),
                    comm.register(gg, pl, ["Wartość BMI", "Wzrost [cm]"], alias='wzrost-bmi', mode=xr),
                    comm.register(ss, de, '\\newpage'),
                ],
            },
            "Warunki socjodemograficzne" : {
                "Miejsce zamieszkania" : [
                    comm.register(gg, cot, "Miejsce zamieszkania", alias='zamieszkanie', mode=xr),
                    comm.register(gd, de, "zamieszkanie", alias='zamieszkanieD'),
                    comm.register(gg, pl, ["Płeć"], alias='miejscezamieszkaniaplot', plot={'hue': 'Miejsce zamieszkania'}, mode=xr),
                    comm.register(ss, de, '\\newpage'),
                ],
                "Stan cywilny" : [
                    comm.register(gg, cot, "Stan cywilny", alias='stanc, mode=xr'),
                    comm.register(gd, de, "stanc", alias='stancD'),
                    comm.register(gg, pl, ["Stan cywilny"], alias='stancywilnypolot', plot={'hue': 'Płeć'}, mode=xr),
                    comm.register(ss, de, '\\newpage'),
                ],
            },
            "Aktywność fizyczna" : [
                comm.register(gg, cot, "Aktywność fizyczna", alias='aktf', mode=xr),
                comm.register(gd, de, "aktf", alias='aktfD'),
                comm.register(gg, pl, ["Aktywność fizyczna"], alias='aktfplot', plot={'hue': 'Płeć'}, mode=xr),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Ile minut aktywności fiz. w tyg.", alias='aktfm', mode=xr),
                comm.register(gd, de, "aktfm", alias='aktfmD'),
                comm.register(gg, pl, ["Aktywność fizyczna", 'Wartość BMI'], alias='aktfplot', mode=xr),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, ext, "Rodzaj aktywności fizycznej", alias='aktfrm', mode=xr),
                comm.register(gd, de, "aktfrm", alias='aktfrD'),
                comm.register(ss, de, '\\newpage'),
            ],
                },
        "Przegląd wyników ankiety" : {
            "Zatrudnienie i warunki pracy" : [
                comm.register(gg, cot, "Staż pracy", alias='stazp', mode=xr),
                comm.register(gd, de, "stazp", alias='stazpD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Oddział", alias='odd', mode=xr),
                comm.register(gd, de, "odd", alias='oddD'),
                comm.register(ss, de, 'Na potrzeby analizy przynależność do oddziałów została przegrupowana na mniejsze kategorie przy założeniu, że w każdej grupie powinno znajdować się co najmniej 5 osób. Rodzaje oddziałów przedstawione zostały w poniższej tabeli.'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Rodzaj oddziału", alias='oddR', mode=xr),
                comm.register(gd, de, "oddR", alias='oddRD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Godziny przepracowane w tygodniu", alias='godzt', mode=xr),
                comm.register(gd, de, "godzt", alias='godztD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Prawidłowa postawa ciała w pracy", alias='postawa', mode=xr),
                comm.register(gd, de, "postawa", alias='postawaD'),
                comm.register(gg, pl, ["Prawidłowa postawa ciała w pracy"], alias='postawaplot', plot={"hue": "Płeć"}, mode=xr),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Możliwość planowania przerw", alias='planowanieprzerw', mode=xr),
                comm.register(gd, de, "planowanieprzerw", alias='planowanieprzerwD'),
                comm.register(ss, de, '\\newpage'),


                comm.register(gg, cot, "Praca pod presją czasu", alias='presja', mode=xr),
                comm.register(gd, de, "presja", alias='presjaD'),
                comm.register(ss, de, '\\newpage'),


                comm.register(gg, cot, tmp1, alias='tmp1', mode=xr),
                comm.register(gd, de, "tmp1", alias='tmp1D'),
                comm.register(ss, de, '\\newpage'),


                comm.register(gg, ext, "Aktywności poza pracą", alias='aktywnoscpoza', mode=xr),
                comm.register(gd, de, "aktywnoscpoza", alias='aktywnoscpozaD'),
                comm.register(ss, de, '\\newpage'),
            ],
            "Występowanie bólu kręgosłupa" : [
                comm.register(gg, cot, "Od jak dawna wyst. epizody bólowe", alias='boldawno', mode=xr),
                comm.register(gd, de, "boldawno", alias='boldawnoD'),
                comm.register(gg, pl, ["Płeć"], alias='odjakdawnaplot', plot={'hue': 'Od jak dawna wyst. epizody bólowe'}, mode=xr),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, "Częstotliwość bólu", alias='bolF', mode=xr),
                comm.register(gd, de, "bolF", alias='bolFD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(ss, de, 'Poniższa para histogramów przedstawia rozkład ocen bólu w skali VAS w korelacji z wiekiem ankietowanego. '),
                comm.register(gg, pl, ["Ból VAS", "Wiek"], alias='vaswiekplot', mode=xr),
                comm.register(gg, pl, ["Ból VAS"], alias='VAS', mode=xr),
                comm.register(gg, det, ['Ból VAS'], alias='vasN', silent=True, mode=xr),
                comm.register(gd, de, "vasN", alias='vasND'),
                # acomm.register(ss, de, ''),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, ext, "Charakter bólu", alias='bolcharakter', mode=xr),
                comm.register(gd, de, "bolcharakter", alias='bolcharakterD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, ext, "Kiedy ból mija", alias='kiedymija', mode=xr),
                comm.register(gd, de, "kiedymija", alias='kiedymijaD'),
                comm.register(ss, de, '\\newpage'),
            ],
            "Wpływ bólu na fizyczne i psychiczne aspekty życia" : [
                comm.register(gg, ext, "Utrudnienia w ruchu podczas bólu w czynnościach:", alias='utrudnieniaruchu', mode=xr),
                comm.register(gd, de, "utrudnieniaruchu", alias='utrudnieniaruchuD'),
                comm.register(ss, de, '\\newpage'),

                comm.register(gg, cot, tmp2, alias='tmp2', mode=xr),
                comm.register(gd, de, "tmp2", alias='tmp2D'),
                comm.register(ss, de, '\\newpage'),

            ],
                },
        "Analiza danych" : {
            "Związek występowania bólu kręgosłupa z wskaźnikami antropometrycznymi" : {
                "Charakterystyka bólu" : [
                    comm.register(ff, de, "analysis.tex", loc='pre'),
                    comm.register(ss, de, '\\newpage'),
                ]
                + make_stat(comm, df, metric_col, pain_col, power, xg),
                'Wpływ na funkcje fizyczne i psychiczne': [
                    comm.register(ss, de, '\\newpage'),
                ]
                + make_stat(comm, df, metric_col, inpact_col, power, xg),
            },
            "Znaczenie uwarunkowań socjo-demograficznych" : {
                'Warunki socjalne a ból' : [
                    comm.register(ss, de, '\\newpage'),
                ]
                + make_stat(comm, df, socjo_col, pain_col + inpact_col, power, xg),
                'Znaczenie zatrudnienia' : [
                    comm.register(ss, de, '\\newpage'),
                ]
                + make_stat(comm, df, job_col, pain_col + inpact_col, power, xg),
            },
            "Wpływ bólu kręgosłupa na upośledzenie funkcji fizycznych i psychicznych" : [
                comm.register(ss, de, '\\newpage'),
            ]
                + make_stat(comm, df, pain_col, inpact_col, power, xg),
            "Rola aktywności fizycznej" : [
                comm.register(ss, de, '\\newpage'),
            ]
                + make_stat(comm, df, activity_col, pain_col + inpact_col, power, xg),
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
    for col in multiple_data:
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
