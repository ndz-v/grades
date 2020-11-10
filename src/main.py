from src.auth_service import AuthService
from src.data_service import DataService
from src.page_service import PageService
from src.presentation_service import PresentationService
import click


@click.command()
@click.option('--passed', '-p', is_flag=True, required=False, help='Zeigt nur bestandene Fächer an (Note >= 4,0).')
@click.option('--credentials', '-c', is_flag=True, required=False, help='Benutzername und Passwort erneut eingeben.')
@click.option('--statistic', '-s', is_flag=True, required=False, help='Gibt die Notenstatistik zu einzelnem Fach an.')
@click.argument('search_string', nargs=-1, required=False)
def main(passed,  search_string, statistic, credentials):

    auth = AuthService(credentials)

    user_name = auth.get_user_name()
    password = auth.get_password()
    graduation = auth.get_graduation()
    subject = auth.get_subject()
    page_service = PageService(user_name, password, graduation, subject)
    grades_overview_page = page_service.get_grades_overview_page()

    data_service = DataService()
    subject_list = data_service.get_subject_list(grades_overview_page, passed, search_string)
    average_grade = data_service.calculate_average_grade()
    gained_points = data_service.calculate_gained_points()

    presentation_service = PresentationService()
    presentation_service.print_average_grade(average_grade)
    presentation_service.print_gained_points(gained_points)
    presentation_service.print_subject_table(subject_list)

    if statistic and len(subject_list) == 1 and len(search_string) > 0:
        subject = subject_list[0]
        link = subject[-1]
        exam_statistics_page = page_service.get_statistics_page(link)
        exam_data = data_service.get_exam_statistics_data(exam_statistics_page)
        presentation_service.print_exam_statistics(exam_data)


if __name__ == "__main__":
    main()
