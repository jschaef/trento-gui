import helpers.handle_support_file as hsf

if __name__ == "__main__":
    df, support_file = hsf.load_support_file("jschaef")
    print(df)
    print(hsf.get_projects("jschaef"))
    