import pandas as pd
import pymysql
def save(sourcetxt, targettxt):
    idx = len(pd.read_csv("database.csv"))
    new_df = pd.DataFrame({"source":sourcetxt, "target":targettxt}, index = [idx])
    new_df.to_csv("database.csv",mode = "a", header = False)


    return None

def load_result():
    result_list=[]
    df = pd.read_csv("database.csv")
    result_list.append(df.iloc[-1].tolist())

    return result_list[0]


if __name__ =="__main__":
    show_result()