from sklearn.preprocessing import normalize

column_inte = cars_data.select_dtypes(include = ['int64'])
bb = column_inte.columns
col_to_norm = bb.to_list()
col_to_norm.remove('price')
col_to_norm

cars_data[col_to_norm] = normalize(X=cars_data[col_to_norm], norm="l2", axis=1)
cars_data.head()

# Inputkan Kode disini
#nominal = tidak ada perbedaan
#ordinal = ada perbedaan
columnstring = cars_data.select_dtypes(include = ['object'], exclude=['int64'])
columnstring.value_counts()

#eksplorasi cek data jenisnya nominal atau ordinal. dari semua data, bentuknya merupakan nominal.
columnstring = cars_data.select_dtypes(include = ['object'], exclude=['int64'])
for col in columnstring:
    a = cars_data[col].value_counts()
    print(a)
    
columnstring = cars_data.select_dtypes(include = ['object'], exclude=['int64'])
col_str = columnstring.columns
col_str

oh_enc = preprocessing.OneHotEncoder()
jenis_ohe = pd.DataFrame(oh_enc.fit_transform(cars_data[col_str]).toarray())
cars_data = cars_data.join(jenis_ohe)
cars_data


