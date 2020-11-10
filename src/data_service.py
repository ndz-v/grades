from typing import List
from bs4 import BeautifulSoup


class DataService:

    data: list

    def get_subject_list(self, page: BeautifulSoup,  passed_option: bool, search_string: str) -> list:
        data: list = self.get_raw_subject_data(page)
        self.data = data

        if passed_option or len(search_string) > 0:
            data = self.get_filtered_subject_data(data, passed_option, search_string)
            return data
        else:
            return data

    def get_filtered_subject_data(self, data: list, passed_option: bool, search_string: str):
        text = ' '.join(search_string).lower()

        filtered_data = []

        for row in data:
            is_passing = row[3] != '5,0' and row[5] != '0'
            found_sub_string = [element for element in row[:-1] if text in element.lower()]
            if passed_option and len(search_string) == 0:
                if is_passing:
                    filtered_data.append(row)
            elif passed_option and len(search_string) >= 0:
                if is_passing and found_sub_string:
                    filtered_data.append(row)
            elif len(search_string) >= 0 and found_sub_string:
                filtered_data.append(row)

        return filtered_data

    def get_raw_subject_data(self, page: BeautifulSoup):
        tables: BeautifulSoup = page.find_all('table')
        tables = tables.pop(1)
        table_rows = tables.find_all('tr')
        table_rows.pop(0)
        table_rows.pop(0)

        data = []

        for row in table_rows:
            row: BeautifulSoup
            row_data = []
            columns = row.find_all('td')
            link = row.find('a')

            for column in columns:
                column: BeautifulSoup
                row_data.append(column.get_text().strip())

            row_data.append(link)
            data.append(row_data)
        return data

    def get_exam_statistics_data(self, exam_statistic_page: BeautifulSoup):
        tables = exam_statistic_page.find_all('table')
        table = tables[2]
        table = table.find_all('td')
        elements = []
        sbuject_row = tables[1].find_all('tr')
        sbuject_row = sbuject_row[1].find_all('td')
        subject_name = ' '.join(sbuject_row[1].get_text().replace('\n', '').replace('\t', '').split())
        for row in table[4:]:
            cleaned_row = '  '.join(row.get_text().replace('\n', '').replace('\t', '').split())
            elements.append(cleaned_row)
        elements.append(subject_name)
        return elements

    def calculate_average_grade(self) -> float:
        points_sum = 0
        weighted_grades_sum = 0

        for row in self.data:
            grade = row[3].replace(',', '.')
            points = row[5].replace(',', '.')

            points_sum += float(points)
            weighted_grades_sum += float(points)*float(grade)

        return weighted_grades_sum/points_sum

    def calculate_gained_points(self) -> float:
        points_sum = 0

        for row in self.data:
            points = row[5].replace(',', '.')

            points_sum += float(points)

        return points_sum
