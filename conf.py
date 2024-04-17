import seaborn as sns

sns.set_theme(style="whitegrid", rc={'figure.figsize': (14, 8), 'axes.labelsize': 15})
sns_api = {'height': 6, 'aspect': 1.75}
pic_path = "report/assets"
pic_ext = "pdf"
tab_path = "report/tabs"
pval = 0.05


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
    'Stan cywilny',
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
    'Stan cywilny',
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
