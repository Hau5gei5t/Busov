from generate_files import InputConnect, DataSet, Report


params = InputConnect()
vacs = DataSet(params.file_name).vacancies_objects
Report(params.print_data(vacs, params.filter_dict)).generate_pdf()