import pandas
from SQL import jobreload_from_db
from quickstart import update_copy_parametr_google_sheets


async def static_parametr(base, idM, group):
    base['Группа'][idM] = group
    await jobreload_from_db("Unit", 'Группа', base['user_ID'][idM], str(group))
    # await update_parametr_google_sheets("Unit", idM+2, 2,  str(group))
    # Копирует статичные столбцы для нового человека

    base['Блок: Начало'][idM] = base['Блок: Начало'][0]
    await jobreload_from_db("Unit", 'Блок: Начало', base['user_ID'][idM], base['Блок: Начало'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 3, base['Блок: Начало'][0])

    base['Дата'][idM] = base['Дата'][0]
    await jobreload_from_db("Unit", 'Дата', base['user_ID'][idM], base['Дата'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 5, base['Дата'][0])

    base['Видео'][idM] = base['Видео'][0]
    await jobreload_from_db("Unit", 'Видео', base['user_ID'][idM], base['Видео'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 6, base['Видео'][0])

    base['Продолжительность (мин)'][idM] = base['Продолжительность (мин)'][0]
    await jobreload_from_db("Unit", 'Продолжительность (мин)', base['user_ID'][idM], base['Продолжительность (мин)'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 7, base['Продолжительность (мин)'][0])

    base['Тест 1'][idM] = base['Тест 1'][0]
    await jobreload_from_db("Unit", 'Тест 1', base['user_ID'][idM], base['Тест 1'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 9, base['Тест 1'][0])

    base['Ответ 1'][idM] = base['Ответ 1'][0]
    await jobreload_from_db("Unit", 'Ответ 1', base['user_ID'][idM], base['Ответ 1'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 10, base['Ответ 1'][0])

    base['Тест 2'][idM] = base['Тест 2'][0]
    await jobreload_from_db("Unit", 'Тест 2', base['user_ID'][idM], base['Тест 2'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 11, base['Тест 2'][0])

    base['Ответ 2'][idM] = base['Ответ 2'][0]
    await jobreload_from_db("Unit", 'Ответ 2', base['user_ID'][idM], base['Ответ 2'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 12, base['Ответ 2'][0])

    base['Тест 3'][idM] = base['Тест 3'][0]
    await jobreload_from_db("Unit", 'Тест 3', base['user_ID'][idM], base['Тест 3'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 13, base['Тест 3'][0])

    base['Ответ 3'][idM] = base['Ответ 3'][0]
    await jobreload_from_db("Unit", 'Ответ 3', base['user_ID'][idM], base['Ответ 3'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 14, base['Ответ 3'][0])

    base['Дата домашнего задания'][idM] = base['Дата домашнего задания'][0]
    await jobreload_from_db("Unit", 'Дата домашнего задания', base['user_ID'][idM], base['Дата домашнего задания'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 17, base['Дата домашнего задания'][0])

    base['Домашнее задание'][idM] = base['Домашнее задание'][0]
    await jobreload_from_db("Unit", 'Домашнее задание', base['user_ID'][idM], base['Домашнее задание'][0])
    # await update_parametr_google_sheets("Unit", idM+2, 18, base['Домашнее задание'][0])

    await update_copy_parametr_google_sheets('Unit', base, idM, group)

    return base