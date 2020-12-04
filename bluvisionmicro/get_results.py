


def get_hyphae_area(destination_path, file_results_name):
    file_results = open(file_results_name, 'a')
    #file_results.write('slide_name' + ';' + 'region' + ';' + 'area' + ';' + 'predict' + '\n')
    for subdir, dirs, files in os.walk(destination_path):
        for file in files:
            if os.path.join(subdir, file).endswith('.png'):
                file_name = os.path.join(subdir, file).split('\\')
                slide_name = file_name[-3]
                region = file_name[-2]
                area = file_name[-1].split('_')[1]
                prediction =  file_name[-1].split('_')[0]

                file_results.write(str(slide_name) + ';' + str(region) + ';' + str(area) + ';' + str(prediction) + '\n')
    file_results.close()




def calculate_avg_hyphae_area(destination_path, file_results_name, file_results_hyphae_avg_name):
    """Calculate the mean and std for hyphae per slide."""
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    # file_results_hyphae_avg = open(file_results_hyphae_avg_name, 'w')
    # file_results_hyphae_avg.write('slide_name' + ';' + 'area' + ';' + 'predict' + '\n')
    # file_results_hyphae_avg.close()

    data = pd.read_csv(file_results_name, sep=";", header=0)


    #data = data.iloc[:, :-2]


    data.columns = ["slide", "region", "pred", "area"]
    data["area"] = pd.to_numeric(data["area"])

    ax = data['area'].hist(by=data['slide'], bins=[0, 2000, 4000, 8000, 15000])

    #with PdfPages(r'Charts.pdf') as export_pdf:
    #plt.xlabel('colony area')
    #plt.ylabel('number of colonies')
        #export_pdf.savefig()

    #plt.show()

    result = data.groupby(['slide', 'region'], as_index=False).agg({'area': ['mean', 'std', 'count']})

    result.columns = result.columns.droplevel()
    result.columns = ["slide_name", "slide_region", "mean_area", "std_area", "nr_of_colonies"]

    #print (result)




    result.to_csv(file_results_hyphae_avg_name, encoding='utf-8', sep=';')