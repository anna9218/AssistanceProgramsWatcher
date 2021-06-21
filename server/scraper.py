import requests
from bs4 import BeautifulSoup
from db_access import DBAccess


def populate_database():
    # if populated -> no need to fetch again, update just in case
    if DBAccess.getInstance().isPopulated is True:
        return update_database()

    # otherwise, fetch programs and populate
    URL = "https://www.healthwellfoundation.org/disease-funds/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='main')
    program_elems = results.find_all('ul', class_='funds')

    programs = []
    program_count = 5
    # access five <li> in funds <ul>
    for li_tag in program_elems[0].findAll('li'):
        if program_count == 0:
            break
        program_count -= 1

        name = li_tag.text
        link = li_tag.a.get('href')

        # get program info from link
        program_page = requests.get(link)
        soup = BeautifulSoup(program_page.content, 'html.parser')
        results = soup.find(id='fund-details')

        # add program's info
        program = {"disease_funds": name,
                   "treatments_covered": get_treatments_covered(results),
                   "status": get_program_status(results),
                   "max_award_level": get_program_award(results)}
        programs.append(program)
    # write to DB
    DBAccess.getInstance().insert_programs(programs)


def get_treatments_covered(results):
    """
    :param results: soup object of id='fund-details'
    :return: all program's covered treatments as a string
    """
    program_elems = results.find_all('div', class_='treatments')
    treatments = program_elems[0].text.replace('\n', ' ').strip().replace(' ', ', ')
    return treatments


def get_program_status(results):
    """
    :param results: soup object of id='fund-details'
    :return: program's status as string
    """
    program_elems = results.find_all('div', class_='row clearfix')
    status_str = program_elems[0].contents[1].contents[2].replace('\n', "").replace('\t', "").strip()
    return status_str


def get_program_award(results):
    """
    :param results: soup object of id='fund-details'
    :return: program's max award as string
    """
    program_elems = results.find_all('div', class_='row clearfix')
    award_str = program_elems[1].contents[1].contents[2].replace('\n', "").replace('\t', "").strip()
    return award_str


def update_database():
    fetched_programs = DBAccess.getInstance().fetch_programs()
    URL = "https://www.healthwellfoundation.org/disease-funds/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='main')
    program_elems = results.find_all('ul', class_='funds')

    # 5 programs
    isUpdated = False
    for program in fetched_programs:
        program_name = program['disease_funds']
        for li_tag in program_elems[0].findAll('li'):
            tag_name = li_tag.text
            if tag_name == program_name:
                tag_link = li_tag.a.get('href')

                # get program info from link
                program_page = requests.get(tag_link)
                soup = BeautifulSoup(program_page.content, 'html.parser')
                results = soup.find(id='fund-details')

                treatments_covered = get_treatments_covered(results)
                status = get_program_status(results)
                max_award_level = get_program_award(results)

                if treatments_covered == program['treatments_covered'] and status == program[
                    'status'] and max_award_level == program['max_award_level']:
                    break  # no need to update


                # update DB
                DBAccess.getInstance().update_program({'disease_funds': program_name},
                                                      {"treatments_covered": treatments_covered,
                                                       "status": status,
                                                       "max_award_level": max_award_level})
                isUpdated = True

    if isUpdated:
        return True
    return False

# update_database()
# populate_database()
