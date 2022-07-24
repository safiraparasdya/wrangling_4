#1.D. Persentase nilai null
persentase_null_values = cars_data.isna().sum()/len(cars_data)*100
persentase_null_values

cars_data.rename(columns = {'dateCreated':'ad_created', 'dateCrawled':'date_crawled','fuelType':'fuel_type',
                            'lastSeen':'last_seen','onthOfRegistration':'registration_month',
                           'notRepairedDamage':"unrepaired_damage", "nrOfPictures": "num_of_pictures",
                            "offerType": "offer_type","postalCode": "postal_code","powerPS": "power_ps",
                            "vehicleType": "vehicle_type","yearOfRegistration": "registration_year"},
                             inplace = True)
cars_data.head(10)

#mengubah tipe data ke datetime64
cars_data['ad_created'] = pd.to_datetime(cars_data['ad_created'])
cars_data['date_crawled'] = pd.to_datetime(cars_data['date_crawled'])
cars_data['last_seen'] = pd.to_datetime(cars_data['last_seen'])

#penyeragaman penulisan value pada kolom price dan odometer sehingga hanya menampilkan integer

import re
cars_data['price'] =  [re.sub('[^0-9 \n\.]','', str(x)) for x in cars_data['price']]
cars_data['odometer'] =  [re.sub('[^0-9 \n\.]','', str(x)) for x in cars_data['odometer']]

#mengubah tipe data untuk kolom price dan odometer ke numeric

cars_data['price'] = pd.to_numeric(cars_data['price'])
cars_data['odometer'] = pd.to_numeric(cars_data['odometer'])

#5.A. pengecekan jumlah data unik pada kolom bertipe string
columnstring = cars_data.select_dtypes(include = ['object'], exclude=['int64'])
for col in columnstring:
    a = cars_data[col].value_counts()
    print(a)
    
#mendapatkan row untuk data berjumlah sedikit di kolom seller
kolomseller = cars_data.index[cars_data['seller'] == 'gewerblich'].to_list()
kolomseller

#mendapatkan row untuk data berjumlah sedikit di kolom offertype
kolomoffer = cars_data.index[cars_data['offer_type'] == 'Gesuch'].to_list()
kolomoffer

#mendapatkan data berjumlah sedikit di kolom model (<10)
kolommodel = cars_data['model'].value_counts()<10
cobs = kolommodel.to_frame()
modeldibawah10 = cobs.loc[cobs['model'] == True].index
listkosong = []
for x in modeldibawah10:
    y = str(x)
    listkosong.append(y)
print(listkosong)

#mendapatkan row dari data berjumlah sedikit di kolom model (<10)
xxs = []
for isi in listkosong:
    kolommodel = cars_data.index[cars_data['model'] == isi].to_list()
    xxs.append(kolommodel)
print(xxs)

#melakukan flattening pada data list xxs
flat_list = [x for xs in xxs for x in xs]
flat_list

#mendapatkan seluruh row yang perlu dihapus
kolomdrop = kolomseller+kolomoffer+flat_list
kolomdrop_nonduplicate = set(kolomdrop)
kolomdrop2 = list(kolomdrop_nonduplicate)
kolomdrop2

#drop seluruh row yang telah diidentifikasi
cars_data.drop(kolomdrop2,inplace= True)

#5.B. Untuk kolom numeric, drop kolom yang tidak berisi informasi apapun (hanya berisi angka 0) kecuali postal code

#cari kolom apa saja yang bertipe int
column_int = cars_data.select_dtypes(include = ['int64'])
for col in column_int:
    print(col)
    
kolomprice = cars_data.index[cars_data['price'] == 0].to_list()
kolomreg = cars_data.index[cars_data['registration_year'] == 0].to_list()
kolompower = cars_data.index[cars_data['power_ps'] == 0].to_list()
kolomodo = cars_data.index[cars_data['odometer'] == 0].to_list()
kolommonth = cars_data.index[cars_data['monthOfRegistration'] == 0].to_list()
rowdrop_dari = kolomprice+kolomreg+kolompower+kolomodo+kolommonth
rowdrop_dari

cars_data.drop(rowdrop_dari,inplace= True)

#6.A. histogram skewed menandakan banyaknya outlier.

fig,ax = plt.subplots (nrows = 1, ncols = 1,figsize = (20,5))

saleprice = cars_data['price']
sns.distplot(saleprice, axlabel=saleprice.name)

#6.B. Untuk memudahkan pemrosesan, ditentukan nilai dari kolom price berkisar 500 sampai 40000.
#Hapus data yang nilai pricenya tidak masuk dalam rentang tersebut.

kolomprice_under = cars_data.index[cars_data['price'] < 500].to_list()
kolomprice_over = cars_data.index[cars_data['price'] > 40000].to_list()
kolomprice_outlier = kolomprice_under+kolomprice_over
kolomprice_outlier

#menghapus row outlier dari price
cars_data.drop(kolomprice_outlier,inplace= True)
cars_data

data_dengan_nan = ['vehicle_type','gearbox','model','fuel_type','unrepaired_damage']
for x in data_dengan_nan:
    x_mode = cars_data[x].mode()
    b = x_mode[0]
    cars_data[x] = cars_data[x].fillna(b)
    
