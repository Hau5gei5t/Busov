import generate_files
import print_table

while True:
    option = input("Вакансии или Статистика: ")
    dev = "not bug"
    if option == "Статистика":
        params = generate_files.InputConnect()
        vacs = generate_files.DataSet(params.file_name).vacancies_objects
        generate_files.Report(params.print_data(vacs, params.filter_dict)).generate_image()
        break
    elif option == "Вакансии":
        params = print_table.InputConnect()
        vacancies = print_table.DataSet(params.file_name)
        params.print_vacancy(vacancies.vacancies_objects)
        break
    else:
        print("Повторите ввод")

