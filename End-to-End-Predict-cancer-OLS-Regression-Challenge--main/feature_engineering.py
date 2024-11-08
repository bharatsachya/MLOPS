import pandas as pd 
from sklearn.preprocessing import OneHotEncoder

def bin_to_num(data):
    binnedinc = []
    for i in data["binnedinc"]:
        # Remove the parenthesis and brackets 
        i = i.strip("()[]")
        print(i)
        # Split the string into a list after splitting by comma 
        i = i.split(",")
        print(i)
        # Convert the list to tuple 
        i = tuple(i)
        print(i)
        # Convert individual elements to float 
        i = tuple(map(float, i))
        print(i)
        # Convert the tuple to list 
        i = list(i)
        print(i)
        # Append the list to binnedinc list 
        binnedinc.append(i)
    data["binnedinc"] = binnedinc

    # Make a new column lower and upper bound 
    data["lower_bound"] = [i[0] for i in data["binnedinc"]] # Lower bound 
    data["upper_bound"] = [i[1] for i in data["binnedinc"]] # Upper bound 
    # and also median point 
    data["median"] = (data["lower_bound"] + data["upper_bound"]) / 2 
    # drop the binnedinc column 
    data.drop("binnedinc", axis = 1, inplace = True)
    return data 

def cat_to_col(data):
    # Make a new column by Splitting the geography column 
    data["county"] = [i.split(",")[0] for i in data["geography"]] 
    data["state"] = [i.split(",")[1] for i in data["geography"]]
    # Drop the geography column 
    return data 

def one_hot_encoding(X):
    # Select categorical Columns 
    categorical_columns = X.select_dtypes(include = ["object"]).columns
    # One hot encode categorical columns
    one_hot_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
    one_hot_encoded = one_hot_encoder.fit_transform(X[categorical_columns])
    # Convert the one hot encoded array to a dataframe 
    one_hot_encoded = pd.DataFrame(
        one_hot_encoded, columns=one_hot_encoder.get_feature_names_out(categorical_columns)
    )
    # Drop the categorical columns from the original dataframe 
    X = X.drop(categorical_columns, axis = 1)
    # Concatenate the one hot encoded dataframe into the original dataframe 
    X = pd.concat([X, one_hot_encoded], axis = 1)
    return X