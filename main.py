import generate_files
import print_table
import cProfile



def main():
    while True:
        option = input("Вакансии или Статистика: ")

        if option == "Статистика":
            params = generate_files.InputConnect()
            vacancies = generate_files.DataSet(params.file_name).vacancies_objects
            generate_files.Report(params.print_data(vacancies, params.filter_dict)).generate_pdf()
            break
        elif option == "Вакансии":
            params = print_table.InputConnect()
            vacancies = print_table.DataSet(params.file_name)
            params.print_vacancy(vacancies.vacancies_objects)
            break
        else:
            print("Повторите ввод")


if __name__ == '__main__':
    main()
    # cProfile.run("main()", sort="cumtime")

