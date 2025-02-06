def get_user(row: list) -> dict:
    return (
        {
            "id": row[0],
            "name": row[1],
            "pass": row[2],
            "role": row[3],
            "institution": row[4],
        }
        if row
        else {}
    )


def get_users(rows: list) -> list[dict]:
    return [get_user(row) for row in rows] if rows else []


def get_role(row: list) -> dict:
    return {"title": row[0]}


def get_roles(rows: list) -> list[dict]:
    return [get_role(row) for row in rows] if rows else []


def get_institution(row: list) -> dict:
    return {"name": row[0], "short_name": row[1]}


def get_institutions(rows: list) -> list[dict]:
    return [get_institution(row) for row in rows] if rows else []


def get_question(row: list) -> dict:
    return {"id": row[0], "title": row[1]}


def get_answer(row: list) -> dict:
    return {"id": row[2], "title": row[3]}


def get_questions(rows: list) -> list[dict]:
    questions = []
    question = {**get_question(rows[0]), "answers": [get_answer(rows[0])]}
    rows.pop(0)
    for row in rows:
        if row[0] != question["id"]:
            questions.append(question)
            question = {**get_question(row), "answers": [get_answer(row)]}
        else:
            question["answers"].append(get_answer(row))
    if question:
        questions.append(question)

    return questions


def get_answers(rows: list) -> list[dict]:
    return [get_answer(row) for row in rows] if rows else []


def get_q(row: list) -> dict:
    return {"id": row[0], "title": row[1], "answer": get_answer(row)}


def get_questionnaire(row: list) -> dict:
    questionnaire = {
        "id": row[0],
        "professor": get_user(row[4:9]),
        "resident": get_user(row[9:14]),
        "questions_answereds": [get_q(row[17:])],
    }

    return questionnaire


def get_questionnaires(rows: list) -> list[dict]:
    questionnaires = []
    questionnaire = {
        "id": rows[0][0],
        "professor": get_user(rows[0][4:9]),
        "resident": get_user(rows[0][9:14]),
        "questions_answereds": [get_q(rows[0][17:])],
    }
    rows.pop(0)
    for row in rows:
        if row[0] != questionnaire["id"]:
            questionnaires.append(questionnaire)

            questionnaire = {
                "id": row[0],
                "professor": get_user(row[4:9]),
                "resident": get_user(row[9:14]),
                "questions_answereds": [get_q(row[17:])],
            }
        else:
            questionnaire["questions_answereds"].append(get_q(row[17:]))
    if questionnaire:
        questionnaires.append(questionnaire)
    return questionnaires


"""
MVC
Organização Orientada a Domínios
"""
