from manager import Session
from conf import tex_config

if __name__ == "__main__":
    analysis = Session(tex_config)
    analysis.create_table_of_content()

    #df = data_loader("data/data.xlsx")
    #data = generate_metric(df)
