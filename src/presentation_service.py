import click
import os


class PresentationService:
    window_width = 0
    small_ratio = 0
    big_ratio = 0

    def __init__(self):
        window_size = os.popen('stty size', 'r').read().split()
        self.window_width = float(window_size[1])
        self.small_ratio = int(self.window_width*0.08)
        self.big_ratio = int(self.window_width*0.3)

    def print_subject_table(self, subject_list: list):
        self.print_table_header()
        for subject_row in subject_list:
            self.print_subject(subject_row)
        click.echo()

    def print_table_header(self):
        click.secho(f'{"":-^{self.window_width}}', fg='white', bold=True)
        click.secho(f'{"Modul"[:self.small_ratio]:<{self.small_ratio}} | ', bold=True, nl=False)
        click.secho(f'{"Fach"[:self.big_ratio]:<{self.big_ratio}} | ', bold=True, nl=False)
        click.secho(f'{"Note"[:self.small_ratio]:<{self.small_ratio}} | ', bold=True, nl=False)
        click.secho(f'{"LP"[:self.small_ratio]:<{self.small_ratio}} | ', bold=True, nl=False)
        click.secho(f'{"Versuch"[:self.small_ratio]:<{self.small_ratio}} | ', bold=True, nl=False)
        click.secho(f'{"Datum"[:self.small_ratio]:<{self.small_ratio}} | ', bold=True, nl=False)
        click.secho(f'{"Semester"[:self.small_ratio]:<{self.small_ratio}}', bold=True)
        click.secho(f'{"":-^{self.window_width}}', fg='white', bold=True)

    def print_subject(self, subject_row: list):
        module = subject_row[0]
        subject = subject_row[1]
        semester = subject_row[2]
        grade = subject_row[3]
        points = subject_row[5]
        attempt = subject_row[8]
        date = subject_row[9]

        converted_grade = float(grade.replace(',', '.'))
        color = self.select_color(converted_grade)

        click.secho(f'{module[:self.small_ratio]:<{self.small_ratio}}', fg='white', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{subject[:self.big_ratio]:<{self.big_ratio}}', fg=color, nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{grade[:self.small_ratio]:<{self.small_ratio}}', fg=color, nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{points[:self.small_ratio]:<{self.small_ratio}}', fg=color, nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{attempt[:self.small_ratio]:<{self.small_ratio}}', fg='white', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{date[:self.small_ratio]:<{self.small_ratio}}', fg='white', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{semester[:self.big_ratio]:<{self.small_ratio}}')

    def select_color(self, grade):
        if 1 <= grade <= 1.5:
            return 'bright_green'
        elif 1.5 < grade <= 2.5:
            return 'green'
        elif 2.5 < grade <= 3.5:
            return 'white'
        elif 3.5 < grade <= 4.0:
            return 'bright_yellow'
        else:
            return 'red'

    def print_average_grade(self, grade: float):
        grade_text = str(grade).replace('.', ',')
        click.echo()
        click.secho(f'{"Durchschnittsnote":<10} {grade_text}', fg=self.select_color(grade))

    def print_gained_points(self, points: float):
        click.secho(f'{"Erreichte LP":<10} {int(points)}')
        click.echo()

    def print_exam_statistics(self, exam_data: list):
        subject_name = exam_data[14]
        click.echo()
        click.echo(f'{"NOTENSPIEGEL"} {subject_name}')
        click.secho(f'{"":-^65}', fg='white', bold=True)
        click.echo(f'{"Notenbereich":<31} | Anzahl')
        click.secho(f'{"":-^65}', fg='white', bold=True)
        very_well_amount = exam_data[1]
        good_amount = exam_data[3]
        satisfying_amount = exam_data[5]
        sufficient_amount = exam_data[7]
        deficient_amount = exam_data[9]

        attendees_amount = exam_data[11]
        average_grade = exam_data[13]

        table_width = self.window_width/4

        click.secho(f'{"Sehr gut":<15} {"(1,0 - 1,5)":<15}', fg='bright_green', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{very_well_amount}', fg='bright_green')

        click.secho(f'{"Gut":<15} {"(1,6 - 2,5)":<15}', fg='green', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{good_amount}', fg='green')

        click.secho(f'{"Befriedigend":<15} {"(2,6 - 3,5)":<15}', fg='white', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{satisfying_amount}', fg='white')

        click.secho(f'{"Ausreichend":<15} {"(3,6 - 4,0)":<15}', fg='bright_yellow', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{sufficient_amount}', fg='bright_yellow')

        click.secho(f'{"Mangelhaft":<15} {"(4,1 - 5,0)":<15}', fg='bright_red', nl=False)
        click.secho(' | ', nl=False)
        click.secho(f'{deficient_amount}', fg='red')

        click.secho(f'{"":-^65}', fg='white', bold=True)
        click.secho(f'{"Teilnehmer":<31} | {attendees_amount}', fg='white')
        click.secho(f'{"Durchschnittsnote":<31} | {average_grade}', fg='white')
        click.secho(f'{"":-^65}', fg='white', bold=True)
        click.echo()
